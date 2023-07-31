
from sqlalchemy import create_engine

engine = create_engine('sqlite:///Buildings_Database.sqlite', echo=True)
connection = engine.connect()

print(engine.table_names())
# 2021-03-29 06:52:34,731 INFO sqlalchemy.engine.base.Engine SELECT name FROM sqlite_master
# WHERE type='table' ORDER BY name
# 2021-03-29 06:52:34,734 INFO sqlalchemy.engine.base.Engine ()
# ['Buildings']