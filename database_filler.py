from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Beer, Review

engine = create_engine('sqlite:///data.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

beer = Beer(name="Beer1", ibu=60, calories=120, abv=4.5, style="Style1", brewery_location="Location1")
session.add(beer)

beer = Beer(name="Beer2", ibu=60, calories=120, abv=4.5, style="Style2", brewery_location="Location2")
session.add(beer)

beer = Beer(name="Beer3", ibu=60, calories=120, abv=4.5, style="Style3", brewery_location="Location3")
session.add(beer)

beer = Beer(name="Beer4", ibu=60, calories=120, abv=4.5, style="Style4", brewery_location="Location4")
session.add(beer)

beer = Beer(name="Beer5", ibu=60, calories=120, abv=4.5, style="Style5", brewery_location="Location5")
session.add(beer)

session.commit()
