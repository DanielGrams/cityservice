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

class RecyclingStreet(db.Model):
    __tablename__ = 'recyclingstreets'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String())
    town_id = db.Column(db.String())
    name = db.Column(db.String())
    events = db.relationship('RecyclingEvent', backref='street', lazy=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class RecyclingEvent(db.Model):
    __tablename__ = 'recyclingevents'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String())
    category = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True))
    street_id = db.Column(db.Integer, db.ForeignKey('recyclingstreets.id'), nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)
