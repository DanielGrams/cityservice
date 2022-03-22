from sqlalchemy import func

from project import db
from project.models import Place, RecyclingStreet


def get_place_query(keyword=None):
    query = Place.query

    if keyword:
        like_keyword = "%" + keyword + "%"
        keyword_filter = Place.name.ilike(like_keyword)
        query = query.filter(keyword_filter)

    return query.order_by(func.lower(Place.name))


def get_place_recycling_streets_query(place_id: int, keyword=None):
    query = RecyclingStreet.query.filter(RecyclingStreet.place_id == place_id)

    if keyword:
        like_keyword = "%" + keyword + "%"
        keyword_filter = RecyclingStreet.name.ilike(like_keyword)
        query = query.filter(keyword_filter)

    query = query.order_by(
        db.case(((RecyclingStreet.name.ilike("Ortsteil%"), 0),), else_=1),
        db.case(((RecyclingStreet.name.ilike("Stadtteil%"), 0),), else_=1),
        func.lower(RecyclingStreet.name),
    )

    return query
