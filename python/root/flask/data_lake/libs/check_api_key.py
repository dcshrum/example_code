from root.libs.cached_core_libs import api_keys
import json
def validate_key(endpoint = None, my_key = None, session_id = None):
    
    print(session_id + ':' + endpoint + ':Checking Key:', flush=True)

    # {'api_key': '7e1ddfc85ae45a95330209c0834c59876011aa587be693354cbd1f40bf637fcd', 'description': 'Power BI', 'expiration_date': None, 'end_points': None}
    my_keys = api_keys.get_api_keys()
    for this_key in my_keys:
        if my_key == this_key['api_key']:
            print(session_id + ':Valid Key in use:', flush=True)
            if this_key['end_points'] is not None:
                for this_allowed in json.loads(this_key['end_points']):
                    if this_allowed.lower() == 'all' or this_allowed.lower() == endpoint:
                        print(session_id + ':ACCESSOK:', flush=True)
                        return this_key
            print(session_id + ':NOACCESS:', flush=True)
            return False
                
    print(session_id + ':No Valid Key in use:', flush=True)
    return False
