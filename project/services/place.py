from sqlalchemy import func

from project.models import Place


def get_place_query(keyword=None):
    query = Place.query

    if keyword:
        like_keyword = "%" + keyword + "%"
        keyword_filter = Place.name.ilike(like_keyword)
        query = query.filter(keyword_filter)

    return query.order_by(func.lower(Place.name))
