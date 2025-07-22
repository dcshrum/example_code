
import logging
import sys
from root.libs import DataTypeMap_Python_MySQL

def get_create_table(json_data, table_name):
    from root.libs import localMySQLDB_connection
    from root import common_params
    from pprint import pprint
    
    local_connection = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = local_connection.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA. TABLES WHERE TABLE_SCHEMA = '"+common_params.LOCAL_SCHEMA_NAME+"' AND TABLE_NAME = '"+table_name+"';")
    records = cursor.fetchall()
    existing_columns = {}
    for row in records:
        logging.debug('get_create_table in create_table_from_JSON.  Generating a create table statement for a table that exists. Existing columns:')
        cmd = "SHOW COLUMNS FROM "+table_name+";"
        logging.debug(cmd)
        cursor.execute(cmd)
        innser_records = cursor.fetchall()
        for inner_row in innser_records:
            # 0 = field , 1 = type
            existing_columns[inner_row[0]] = inner_row[1]
    headers = []
    result = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('

    # SOME FUNKY CODE HERE - I updated the code to check to see if new columns are added to
    # an already existing table... so we have duplicate data in dicts but it's not THAT much memeory.
    # cut me a break.
    new_columns = {}
    
    columns = {}
    fatal_error = False
    for record in json_data:
        
        for element in record:
            
            if type(record[element]).__name__ == 'NoneType':
                # print('skipping a null value')
                continue
            try:
                # {'cc_emails': '`cc_emails` JSON',
                this_column = '`' + element + '` ' + DataTypeMap_Python_MySQL.datatype_map[type(record[element]).__name__]
            except:
                logging.debug('Looks like a data type is not defined in DataTypeMap_Python_MySQL.datatype_map')
                print("\n\nuser: ")
                print(record)
                print("\n\nuser[element]:")
                print(record[element])
                print("\n\ntype(user[element]):")
                print(type(record[element]))   
                print("\n\nuser[element].__name__")
                print(record[element].__name__)
  
                fatal_error = True
                
            if element in columns:
                if columns[element] != this_column:
                    logging.error('It looks like a column definition changed.  See create_table_from_JSON.py')
                    logging.error(element)
                    logging.error(columns[element])
                    logging.error(this_column)
                    fatal_error = True
            else:
                columns[element] = this_column
                headers.append(element)
                new_columns[element] = DataTypeMap_Python_MySQL.datatype_map[type(record[element]).__name__]
        
    if fatal_error:
        sys.exit(1)
    
    if len(existing_columns) > 0:
        for this_col in new_columns:
            if this_col not in existing_columns:
                logging.debug('Found a NEW column in the create_table_from_JSON lib for: ' + table_name)
                logging.debug('The table will be updated with the new column... but it is possible the table is being dropped and recreated anyway')
                local_connection = localMySQLDB_connection.LocalDBConnection().connect()
                cursor = local_connection.cursor()
                cmd = "ALTER TABLE " + table_name + " ADD `" + this_col + "` " + new_columns[this_col] 
                logging.debug(cmd)
                cursor.execute(cmd)
    comma = ''
    for column in columns:
        result += comma + columns[column]
        comma = ', '
    result += ') ENGINE = MYISAM;'

    return result, headers
