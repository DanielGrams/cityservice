from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs

from project import db
from project.api import add_api_resource
from project.api.news_feed.schemas import (
    NewsFeedIdSchema,
    NewsFeedListRequestSchema,
    NewsFeedListResponseSchema,
    NewsFeedPatchRequestSchema,
    NewsFeedPostRequestSchema,
    NewsFeedSchema,
)
from project.api.resources import (
    BaseResource,
    login_api_user_or_401,
    require_api_access,
)
from project.models import NewsFeed


class NewsFeedListResource(BaseResource):
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

    @doc(
        summary="Add new news feed",
        tags=["News"],
        security=[{"oauth2": ["newsfeed:write"]}],
    )
    @use_kwargs(NewsFeedPostRequestSchema, location="json", apply=False)
    @marshal_with(NewsFeedIdSchema)
    @require_api_access("newsfeed:write")
    def post(self):
        login_api_user_or_401("admin")

        news_feed = self.create_instance(NewsFeedPostRequestSchema)
        db.session.add(news_feed)
        db.session.commit()

        return news_feed, 201


class NewsFeedResource(BaseResource):
    @doc(
        summary="Get news feed",
        tags=["News"],
        security=[{"oauth2": ["newsfeed:read"]}],
    )
    @marshal_with(NewsFeedSchema)
    @require_api_access("newsfeed:read")
    def get(self, id):
        login_api_user_or_401("admin")
        return NewsFeed.query.get_or_404(id)

    @doc(
        summary="Update news feed",
        tags=["News Feeds"],
        security=[{"oauth2": ["newsfeed:write"]}],
    )
    @use_kwargs(NewsFeedPostRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("newsfeed:write")
    def put(self, id):
        login_api_user_or_401("admin")
        newsfeed = NewsFeed.query.get_or_404(id)

        newsfeed = self.update_instance(NewsFeedPostRequestSchema, instance=newsfeed)
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Patch news feed",
        tags=["News Feeds"],
        security=[{"oauth2": ["newsfeed:write"]}],
    )
    @use_kwargs(NewsFeedPatchRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("newsfeed:write")
    def patch(self, id):
        login_api_user_or_401("admin")
        newsfeed = NewsFeed.query.get_or_404(id)

        newsfeed = self.update_instance(NewsFeedPatchRequestSchema, instance=newsfeed)
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Delete news feed",
        tags=["News Feeds"],
        security=[{"oauth2": ["newsfeed:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("newsfeed:write")
    def delete(self, id):
        login_api_user_or_401("admin")
        newsfeed = NewsFeed.query.get_or_404(id)

        db.session.delete(newsfeed)
        db.session.commit()

        return make_response("", 204)


add_api_resource(NewsFeedListResource, "/news-feeds", "api_news_feed_list")
add_api_resource(NewsFeedResource, "/news-feeds/<int:id>", "api_news_feed")
