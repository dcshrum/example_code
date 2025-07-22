def json_to_table(json_data, table_name, drop_create_table = True, load_data=True, unique_key = None, run_on_integrations = False):   
    
    from root import common_params
    import logging, csv, os, sys, time
    from root.libs import localMySQLDB_connection, create_table_from_JSON, JSON_fill_in_the_blanks, exec_sql, check_lock_status
    from pprint import pprint
    
    create_table, headers = create_table_from_JSON.get_create_table(json_data, table_name)

    filePath = common_params.INTERNAL_TEMP_FOLDER + '/' + table_name
    if os.path.exists(filePath): os.remove(filePath)
    genius_filehandle = open(filePath, 'w+', encoding='UTF8', newline='')
    genius_writer = csv.writer(genius_filehandle, delimiter=',', quoting=csv.QUOTE_MINIMAL, escapechar='\\')

    genius_writer.writerow(headers)
    
    for this in json_data:
        genius_writer.writerow(JSON_fill_in_the_blanks.get_good_row(this, headers))
    
        # Code to use if we see a column going overt he 4gb limit for lontext
        # Why would anyone do that?
        # for column in this:
        #     if isinstance(this[column], str):
        #         if len(this[column]) > 50:
        #             this[column] = this[column][0:50]

    genius_filehandle.flush()
    genius_filehandle.close()

    if drop_create_table:
        exec_sql.exec_sql('DROP TABLE IF EXISTS ' + table_name, run_on_integrations)
        # while True:
        #     if check_lock_status.is_table_locked(table_name):
        #         logging.debug('Sleep 10 and check again for table locks')
        #         time.sleep(10)
        #     else:
        #         exec_sql.exec_sql('DROP TABLE IF EXISTS ' + table_name, run_on_integrations)
        #         break
    
    exec_sql.exec_sql(create_table, run_on_integrations)
    if unique_key is not None:
        logging.debug('unique key defined in json_to_table')
        local_connection = localMySQLDB_connection.LocalDBConnection().connect()
        cursor = local_connection.cursor()
        index_name = table_name + '_UC_' + unique_key
        sql_cmd = """SELECT COUNT(1) IndexIsThere FROM INFORMATION_SCHEMA.STATISTICS WHERE table_schema='"""+common_params.LOCAL_SCHEMA_NAME+"' AND TABLE_NAME = '"+table_name+"' AND index_name='"+index_name+"';"
        logging.debug(sql_cmd)
        cursor.execute(sql_cmd)
        records = cursor.fetchall()
        for row in records:
            if row[0] < 1:
                exec_sql.exec_sql("ALTER TABLE "+table_name+" ADD CONSTRAINT "+index_name+" UNIQUE ("+unique_key+");", run_on_integrations)
            else:
                logging.debug('index exists')
        
    if load_data:
        load_statement = "LOAD DATA LOCAL INFILE '" + filePath + "' REPLACE INTO TABLE " + table_name
        load_statement += """ FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\r\\n'  IGNORE 1 ROWS ( """
        comma=''
        for this_col in headers:
            load_statement += comma + '`' + this_col + '`'
            comma = ','
        load_statement += ' ) '
        exec_sql.exec_sql(load_statement, run_on_integrations)
