from project.api import marshmallow


class SQLAlchemyBaseSchema(marshmallow.SQLAlchemySchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
