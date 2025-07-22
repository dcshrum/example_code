from root.libs import redis_cache_wrapper
from root.libs import localMySQLDB_connection

def map_pet_section_tags():

    @redis_cache_wrapper.redis_cache(43200)
    def cache_pet_section_tags():
        db_connection = localMySQLDB_connection.LocalDBConnection().connect()
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("""
            select * from ufl_pet_section_tags
            left join ufl_pet_tag_values on ufl_pet_section_tags.tag_entry_id = ufl_pet_tag_values.tag_entry_id
            left join ufl_pet_tags on ufl_pet_tag_values.tag_id = ufl_pet_tags.tag_id;""")
        records = cursor.fetchall()
        cursor.close()
        return records
    
    result = cache_pet_section_tags()
    return result