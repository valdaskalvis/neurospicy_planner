import pathlib
import sqlite3

# database path
DATABASE_PATH = pathlib.Path(__file__).parent / "planner.db"
# database class
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.c = self.conn.cursor()
        self.create_table()
# task database table creation if the table does not exist
    def create_table(self):
        # Create table if it does not exist: task ID, task name,
        # creation date, deadline, completion status, if it's a work task,
        # and task regularity
        self.c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                created datetime DEFAULT(getdate()),
                deadline datetime DEFAULT(getdate()+1),
                completed INTEGER,
                work INTEGER,
                )""")
# method for querying database
    def query_db(self, query, *query_args):
        result = self.c.execute(query, [*query_args])
        self.conn.commit()
        return result
# method for adding task with default values
    def add_task(self, task):
        self.query_db(
            "INSERT INTO planner VALUES (NULL, ?, DEFAULT, DEFAULT, 0, 0);",
            task,
        )
# marking task as completed:
    def mark_as_done(self, id):
        self.query_db(
            "UPDATE planner SET done=1 WHERE id=?;",
            id,
        )
# deleting task:
    def delete_task(self, id):
        self.query_db(
            "UPDATE planner SET completed=1 WHERE id=?;",
            id,
        )
# getting all personal tasks (non-work):
    def get_personal(self):
        result = self.query_db("SELECT * FROM planner WHERE work=0 AND COMPLETED=0;")
        return result.fetchall()

# getting all completed personal tasks (non-work):
    def get_completed(self):
        result = self.query_db("SELECT * FROM planner WHERE work=0 AND COMPLETED=1;")
        return result.fetchall()

# method for adding work task with default values
    def add_work_task(self, task):
        self.query_db(
            "INSERT INTO planner VALUES (NULL, ?, DEFAULT, DEFAULT, 0, 1);",
            task,
        )
# getting all work tasks:
    def get_work(self):
        result = self.query_db("SELECT * FROM planner WHERE work=1;")
        return result.fetchall()

# rescheduling the task for tomorrow - TBD
    def reschedule(self, task):
        pass

