

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        telegram_id INTEGER NOT NULL UNIQUE
    )
"""

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id)
)
"""

INSERT_USER = 'INSERT OR IGNORE INTO users (username, telegram_id) VALUES (?, ?)'


INSERT_TASK = """
    INSERT INTO tasks (user_id, title, is_done) 
    VALUES (?, ?, 0)
"""

UPDATE_TASK_STATUS = """
UPDATE tasks SET is_done = 1 WHERE id = ? AND user_id = ?
"""

SELECT_USER_TASKS = """
    SELECT id, title, is_done 
    FROM tasks 
    WHERE user_id = ?
"""


SELECT_TASKS_STATS = """
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) as completed,
        SUM(CASE WHEN is_done = 0 THEN 1 ELSE 0 END) as uncompleted
    FROM tasks 
    WHERE user_id = ?
"""


DELETE_TASK_QUERY = """
DELETE FROM tasks WHERE id = ? AND user_id = ?
"""

