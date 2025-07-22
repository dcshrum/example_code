import math

def paginate(data, page=1, per_page=25):
    """
    Efficiently paginates a list of records.

    Args:
        data (list): Full list of items to paginate.
        page (int): Current page number (1-based).
        per_page (int): Number of items per page.

    Returns:
        dict: {
            'data': paginated subset,
            'total_count': total number of records in endpoint,
            'total_pages': total number of pages in endpoint,
            'current_page': the current page number being displayed,
            'per_page': the number of records being displayed per page
        }
    """
    
    page = int(page)

    total = len(data)
    total_pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    paginated_data = data[start:end]

    return {
        'data': paginated_data,
        'total_count': total,
        'total_pages': total_pages,
        'current_page': page,
        'per_page': per_page
    }
