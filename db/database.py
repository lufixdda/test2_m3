import sqlite3
from db.queries import(
    CREATE_USER_TABLE,
    CREATE_TASKS_TABLE,
    INSERT_USER,
    INSERT_TASK,
    UPDATE_TASK_STATUS,
    SELECT_USER_TASKS
)

DB_NAME = 'tasks.db'



def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row      # строки возвращаются как словари
    return conn


def init_db():
    conn = get_db()
    conn.execute(CREATE_USER_TABLE)
    conn.execute(CREATE_TASKS_TABLE)
    conn.commit()
    conn.close()