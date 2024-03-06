import asyncpg
from dbs_assignment.database_url import DATABASE_URL


async def connect_to_database():
    return await asyncpg.connect(DATABASE_URL)

async def get_database_version(app):
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)

async def fetch_database_version():
    connection = await connect_to_database()  # Clearly calling the coroutine
    try:
        version = await connection.fetchval("SELECT version();")
        return version
    finally:
        await connection.close()  # Closing the connection after use




