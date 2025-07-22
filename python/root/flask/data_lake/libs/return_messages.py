noway = {'error': 'No way Jose'}
bad_json = {'error': 'improperly formatted JSON in header'}
bad_int = {'error': 'An int field does not have a valid int value'}
missing_segment = {'error': 'Missing required header: segment'}
segment_not_found = lambda segment: {'error': f'Segment "{segment}" not found in cache'}