from db.database import get_db
from db.queries import INSERT_TASK, UPDATE_TASK_STATUS, SELECT_USER_TASKS, SELECT_TASKS_STATS, DELETE_TASK_QUERY

def create_task(user_id, title):
    conn = get_db() 
    conn.execute(INSERT_TASK, (user_id, title))
    conn.commit()
    conn.close()

def mark_task_as_done(task_id , user_id):
    conn = get_db()
    conn.execute(UPDATE_TASK_STATUS, (task_id, user_id))
    conn.commit()



def get_user_tasks(user_id):
    conn = get_db()
    cursor = conn.execute(SELECT_USER_TASKS, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_tasks_stats(user_id):
    conn = get_db()
    cursor = conn.execute(SELECT_tasks_stats if 'SELECT_tasks_stats' in globals() else SELECT_TASKS_STATS, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]



def delete_task(task_id, user_id):

    conn = get_db()
    conn.execute(DELETE_TASK_QUERY, (task_id, user_id))
    conn.commit() 