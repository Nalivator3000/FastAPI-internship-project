from databases import Database

database = Database('postgresql+psycopg2://postgres:root@localhost/postgres_db')

await database.connect()
