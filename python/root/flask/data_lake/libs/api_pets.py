from flask import request, jsonify
import sys, json, sys, re

from root.libs.cached_core_libs import ufl_pet_enrollments_dict, ufl_pet_section_tags
from root.flask.data_lake.libs import filter_by_tags, tag_mapper, paginator
from root.libs import redis_cache_wrapper

from . import return_messages

def get_pets(run_id = ''):
    
    SEGMENT_KEY = ufl_pet_enrollments_dict.SEGMENT_NAME

    # Headers
    userFirstName  = request.headers.get('userFirstName')
    userLastName  = request.headers.get('userLastName')
    tagPets = request.headers.get('tagPets')
    page = request.headers.get('page', 1)
    segment = request.headers.get('segment')

    # Segment validation
    if not segment:
        return jsonify({
            **return_messages.missing_segment,
            SEGMENT_KEY: [s.decode() for s in redis_cache_wrapper.redis_client.smembers(SEGMENT_KEY)]
        }), 400

    if not redis_cache_wrapper.redis_client.sismember(SEGMENT_KEY, segment):
        return jsonify(return_messages.segment_not_found(segment)), 404
    
    # Bring in cached query
    all_pets = ufl_pet_enrollments_dict.cache_pet_enrollments_by_segment(segment)    

    # Get all tags from the cache
    all_pet_tags = ufl_pet_section_tags.map_pet_section_tags()

    # Define tag sources and mapping
    tag_sources = [
    {
        'tag_name': 'tagPets',
        'tags': all_pet_tags,
        'tag_key': 'pet_sectionId',
        'record_key': 'sectionId'
    }
    ]

    # Final query with tags as a list of dictionaries
    all_pets = tag_mapper.map_tags_to_records(all_pets, tag_sources)

    # Parameters for endpoint

    # userFirstName              
    if userFirstName is not None:
        print(run_id + ':Filter userFirstName on ' + userFirstName, flush=True)
        all_pets = list(filter(lambda entry: re.search(userFirstName, entry['userFirstName'], re.IGNORECASE), all_pets.copy()))
        
    # userLastName              
    if userLastName is not None:
        print(run_id + ':Filter userLastName on ' + userLastName, flush=True)
        all_pets = list(filter(lambda entry: re.search(userLastName, entry['userLastName'], re.IGNORECASE), all_pets.copy()))

    # Tag pets - tag name and tag value 
    if tagPets is not None:

        print("Filter pet tags on " + tagPets, flush=True)

        try:
            tagPets = json.loads(tagPets)

        except json.JSONDecodeError:
            return return_messages.bad_json
        
        all_pets = filter_by_tags.tag_sort(all_pets,tagPets,tag_field='tagPets')
        
    # Pagination
    try:
        print(run_id + ':Filter page on ' + str(page), flush=True)
        all_pets = paginator.paginate(all_pets,page,per_page=3)
    except Exception as error:
        print(run_id + ":An exception occurred:", type(error).__name__, "–", error, flush=True)
        return jsonify(return_messages.bad_int), 400
    
    sys.stderr.flush()            
    return all_pets
