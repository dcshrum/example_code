from collections import defaultdict

def map_tags_to_records(records, tag_sources, skip_if_test=True):
    """
    Maps tags to records based on specified tag sources.

    Parameters:
    - records: List of dictionaries (e.g. grades, users, assessments, etc.)
    - tag_sources: List of dicts with keys:
        - 'tag_name' (e.g. 'ufl_section_tags')
        - 'tags': the list of tag dicts
        - 'tag_key': key in tag dict (e.g. 'd2l_OrgUnitId')
        - 'record_key': key in record dict to join on (e.g. 'OrgUnitId')
    - skip_if_test: Whether to skip records that have a tag_name == 'test'

    Returns:
    - Filtered and tagged list of records
    """

    tag_maps = {}
    test_tagged_ids = defaultdict(set)

    for source in tag_sources:
        tag_map = defaultdict(list)
        for tag in source['tags']:
            raw_tag_name = tag.get('tag_name')
            if raw_tag_name is None:
                continue 
            
            clean_name = raw_tag_name.strip().lower()

            tag_key_value = tag.get(source['tag_key'])
            if tag_key_value is None:
                continue  # Prevent using None as a map key

            tag_map[tag_key_value].append({
                'tag_value': tag.get('tag_value'),
                'tag_name': raw_tag_name
            })

            if skip_if_test and clean_name == 'test':
                test_tagged_ids[source['tag_name']].add(tag_key_value)
        
        tag_maps[source['tag_name']] = tag_map

    output = []
    for record in records:
        skip = False
        for source in tag_sources:
            tag_name = source['tag_name']
            tag_map = tag_maps[tag_name]
            record_id = record.get(source['record_key'])

            if skip_if_test and record_id in test_tagged_ids[tag_name]:
                skip = True
                break

            record[tag_name] = tag_map.get(record_id, [])

        if not skip:
            output.append(record)

    return output
