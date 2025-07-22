import pandas as pd

def tag_sort(all_records, tag_filters=None, tag_field='ufl_tags'):
    """
    Filters a list of records based on matching tag_name and/or tag_value pairs
    provided in tag_filters. Supports partial matching (only tag_name or only tag_value).

    Parameters:
        all_records (list): A list of dicts, each representing a record.
            Each record must contain a tag field (e.g. 'ufl_section_tags') which is a list of dicts.
        tag_filters (list): A list of dicts, each optionally containing:
            - 'tag_name' (str): the name of the tag to match
            - 'tag_value' (str): the value of the tag to match
        tag_field (str): The key in each record that holds the list of tags to filter on.

    Returns:
        list: Filtered list of records that match at least one tag filter condition.
    """
    
    if not isinstance(tag_field, str):
        raise ValueError("tag_field must be a string representing the key holding tag data.")

    df = pd.DataFrame(all_records)

    if tag_filters is None or not isinstance(tag_filters, list):
        raise ValueError("tag_filters must be a list of dicts with optional 'tag_name' and/or 'tag_value'.")

    for tag in tag_filters:
        if not isinstance(tag, dict):
            raise ValueError("Each tag filter must be a dict with optional 'tag_name' and/or 'tag_value'.")
        if 'tag_name' not in tag and 'tag_value' not in tag:
            raise ValueError("Each tag filter must have at least 'tag_name' or 'tag_value'.")

    if tag_field not in df.columns:
        raise KeyError(f"'{tag_field}' not found in records.")

    df_exploded = df.explode(tag_field)
    df_exploded = df_exploded[df_exploded[tag_field].notnull()]

    df_exploded['tag_name'] = df_exploded[tag_field].apply(lambda x: x.get('tag_name').lower() if isinstance(x, dict) and x.get('tag_name') else None)
    df_exploded['tag_value'] = df_exploded[tag_field].apply(lambda x: x.get('tag_value').lower() if isinstance(x, dict) and x.get('tag_value') else None)

    filter_condition = pd.Series(False, index=df_exploded.index)

    for tag in tag_filters:
        condition = pd.Series(True, index=df_exploded.index)
        tag_name = tag.get('tag_name')
        tag_value = tag.get('tag_value')

        if tag_name:
            condition &= (df_exploded['tag_name'] == tag_name.lower())
        if tag_value:
            condition &= (df_exploded['tag_value'] == tag_value.lower())

        filter_condition |= condition

    matched_indexes = df_exploded[filter_condition].index.unique()
    result = df.loc[matched_indexes]
    result = result.replace({float('nan'): None})
    return result.to_dict(orient='records')