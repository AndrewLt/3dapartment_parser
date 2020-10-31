import os
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine

meta = MetaData()
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
conn = engine.connect()

apartment_items = Table(
    "apartment_items", meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('address', String(128), unique=True),
    Column('price', String(12)),
    Column('beds', String(6)),
    Column('baths', String(6)),
    Column('nearest_subway_stations_count', String(12)),
    Column('is_active', Boolean),
)
#meta.create_all(engine)


def save_item_on_db(address, price, beds, baths, nearest_count, is_active):
    s = apartment_items.select().where(apartment_items.c.address == address)
    result = conn.execute(s).fetchone()
    if result is None:
        try:
            new_time = apartment_items.insert().values(id=None, address=address, price=price, beds=beds,
                                                       baths=baths, nearest_subway_stations_count=nearest_count,
                                                       is_active=is_active)
            conn.execute(new_time)
            return 'OK'
        except:
            return 'Error'
    else:
        try:
            new_time = apartment_items.update().where(apartment_items.c.address == address).values(
                id=result[0], address=address, price=price, beds=beds,
                baths=baths, nearest_subway_stations_count=nearest_count,
                is_active=is_active
            )
            conn.execute(new_time)
            return 'OK'
        except:
            return 'Error'
