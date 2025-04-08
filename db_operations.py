import pathlib
import sqlite3

# database path
DATABASE_PATH = pathlib.Path(__file__).parent / "planner.db"
# database class
class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.create_table()
# task database table creation if the table does not exist
    def create_table(self):
        # Create table if it does not exist: task ID, task name,
        # creation date, deadline, completion status, if it's a work task,
        # and task regularity
        query = """CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                created TEXT,
                deadline TEXT,
                completed INTEGER,
                work INTEGER
                );"""
        self.query_db(query)

# Method for querying the database.
    def query_db(self, query, *query_args):
        result = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return result


# Method for adding a new task with default values.
    def add_task(self, task):
        self.query_db(
            "INSERT INTO tasks VALUES (NULL, ?, NULL, NULL, 0, 0);",
            task,
        )


# Method for marking a task as completed.
    def mark_as_done(self, id):
        self.query_db(
            "UPDATE tasks SET completed=1 WHERE id=?;",
            id,
        )


# Method for deleting a task.
    def delete_task(self, id):
        self.query_db(
            "UPDATE tasks SET completed=1 WHERE id=?;",
            id,
        )


# Method for getting all personal (non-work) tasks.
    def get_personal(self):
        result = self.query_db("SELECT id, task, completed FROM tasks WHERE work=0 AND completed=0;")
        return result.fetchall()


# Method for getting all completed personal (non-work) tasks.
    def get_completed(self):
        result = self.query_db("SELECT * FROM tasks WHERE work=0 AND COMPLETED=1;")
        return result.fetchall()


# Method for adding a new work task with default values.
    def add_work_task(self, task):
        self.query_db(
            "INSERT INTO tasks VALUES (NULL, ?, DEFAULT, DEFAULT, 0, 1);",
            task,
        )


# Method for getting all work tasks.
    def get_work(self):
        result = self.query_db("SELECT * FROM tasks WHERE work=1;")
        return result.fetchall()


# Method for rescheduling a task for tomorrow - TBD
    def reschedule(self, task):
        pass

