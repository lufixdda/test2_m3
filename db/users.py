from db.database import get_db
from db.queries import INSERT_USER


async def register_user(username: str, telegram_id: int):
    conn = get_db()
    conn.execute(INSERT_USER, (username, telegram_id))
    conn.commit()
    conn.close()