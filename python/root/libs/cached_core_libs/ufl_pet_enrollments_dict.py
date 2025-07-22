from root.libs import redis_cache_wrapper
from root.libs import localMySQLDB_connection

SEGMENT_NAME = 'valid_pet_segments'

# Cached function per segment
@redis_cache_wrapper.redis_cache(43200)
def cache_pet_enrollments_by_segment(segment_value):
    db_connection = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db_connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM ufl_pet_enrollments
        WHERE NOT EXISTS (
            SELECT 1
            FROM ufl_pet_section_tags
            LEFT JOIN ufl_pet_tag_values ON ufl_pet_section_tags.tag_entry_id = ufl_pet_tag_values.tag_entry_id
            LEFT JOIN ufl_pet_tags ON ufl_pet_tag_values.tag_id = ufl_pet_tags.tag_id
            WHERE ufl_pet_tags.tag_name = 'Test'
              AND ufl_pet_section_tags.pet_sectionId = ufl_pet_enrollments.sectionId
        )
        AND EXISTS (
            SELECT 1
            FROM ufl_pet_section_tags
            LEFT JOIN ufl_pet_tag_values ON ufl_pet_section_tags.tag_entry_id = ufl_pet_tag_values.tag_entry_id
            LEFT JOIN ufl_pet_tags ON ufl_pet_tag_values.tag_id = ufl_pet_tags.tag_id
            WHERE ufl_pet_tags.tag_name = 'Segment'
              AND ufl_pet_tag_values.tag_value = %s
              AND ufl_pet_section_tags.pet_sectionId = ufl_pet_enrollments.sectionId
        );
    """, (segment_value,))
    result = cursor.fetchall()
    cursor.close()
    return result

# Controller function (refreshes valid segments set, gets segments, populates cache)
def get_all_pet_enrollments():
    redis_cache_wrapper.redis_client.delete(SEGMENT_NAME) # Clear existing segment registry
    db_connection = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db_connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT ufl_pet_tag_values.tag_value
        FROM ufl_pet_section_tags
        LEFT JOIN ufl_pet_tag_values ON ufl_pet_section_tags.tag_entry_id = ufl_pet_tag_values.tag_entry_id
        LEFT JOIN ufl_pet_tags ON ufl_pet_tag_values.tag_id = ufl_pet_tags.tag_id
        WHERE ufl_pet_tags.tag_name = 'Segment'
          AND ufl_pet_tag_values.tag_value IS NOT NULL
    """)
    segment_values = [row['tag_value'] for row in cursor.fetchall()]
    cursor.close()

    results = []
    for segment in segment_values:
        segment_result = cache_pet_enrollments_by_segment(segment)
        redis_cache_wrapper.redis_client.sadd(SEGMENT_NAME, segment) # Register as a valid cached segment
        results.extend(segment_result)  # flatten into one list

    return results