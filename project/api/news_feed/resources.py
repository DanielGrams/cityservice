from flask_apispec import doc, marshal_with, use_kwargs

from project.api import add_api_resource
from project.api.news_feed.schemas import (
    NewsFeedListRequestSchema,
    NewsFeedListResponseSchema,
)
from project.api.resources import (
    BaseResource,
    login_api_user_or_401,
    require_api_access,
)
from project.models import NewsFeed


class NewsFeedList(BaseResource):
    @doc(
        summary="List news feeds",
        tags=["News"],
        security=[{"oauth2": ["newsfeed:read"]}],
    )
    @use_kwargs(NewsFeedListRequestSchema, location=("query"))
    @marshal_with(NewsFeedListResponseSchema)
    @require_api_access("newsfeed:read")
    def get(self, **kwargs):
        login_api_user_or_401("admin")

        pagination = NewsFeed.query.paginate()
        return pagination


add_api_resource(NewsFeedList, "/news-feeds", "api_news_feed_list")
