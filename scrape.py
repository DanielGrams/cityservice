from app import app, db
from models import NewsItem

def scrape():
    item = NewsItem(content='Hello', publisher_name='Katermann')

    db.session.add(item)
    db.session.commit()

if __name__ == '__main__':
    scrape()