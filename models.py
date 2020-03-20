from app import db

class NewsItem(db.Model):
    __tablename__ = 'newsitems'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String())
    publisher_name = db.Column(db.String())
    publisher_icon_url = db.Column(db.String())
    content = db.Column(db.String())
    link_url = db.Column(db.String())
    published = db.Column(db.DateTime(timezone=True))
    fetched = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<id {}>'.format(self.id)