import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="attendance.db"):
        # The database file will be stored in the root folder of the project
        # which is one level up from the database/ directory.
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", db_name))
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_default_admin()

    def create_tables(self):
        # Admins table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                year TEXT NOT NULL,
                encoding BLOB
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                name TEXT,
                date TEXT,
                time TEXT,
                status TEXT,
                confidence REAL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id)
            )
        ''')
        self.conn.commit()

    def seed_default_admin(self):
        # Seed default admin if table is empty
        self.cursor.execute("SELECT COUNT(*) FROM Admins")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                "INSERT INTO Admins (username, password) VALUES (?, ?)",
                ("admin", "admin123")
            )
            self.conn.commit()

    # Admin Auth
    def validate_admin(self, username, password):
        self.cursor.execute(
            "SELECT * FROM Admins WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone() is not None

    # Student Management
    def add_student(self, student_id, name, department, year, encoding_blob=None):
        try:
            self.cursor.execute(
                "INSERT INTO Students (student_id, name, department, year, encoding) VALUES (?, ?, ?, ?, ?)",
                (student_id, name, department, year, encoding_blob)
            )
            self.conn.commit()
            return True, "Student registered successfully."
        except sqlite3.IntegrityError:
            return False, f"Student ID {student_id} already exists."
        except Exception as e:
            return False, str(e)

    def update_student_encoding(self, student_id, encoding_blob):
        try:
            self.cursor.execute(
                "UPDATE Students SET encoding = ? WHERE student_id = ?",
                (encoding_blob, student_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            return False

    def get_all_students(self):
        self.cursor.execute("SELECT student_id, name, department, year, encoding FROM Students")
        return self.cursor.fetchall()

    def get_student_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM Students")
        return self.cursor.fetchone()[0]

    # Attendance Management
    def mark_attendance(self, student_id, name, confidence, status="Present"):
        date_today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # Check if already marked today
        self.cursor.execute(
            "SELECT * FROM Attendance WHERE student_id = ? AND date = ?",
            (student_id, date_today)
        )
        if self.cursor.fetchone():
            return False, "Already marked today."
        
        try:
            self.cursor.execute(
                "INSERT INTO Attendance (student_id, name, date, time, status, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                (student_id, name, date_today, time_now, status, confidence)
            )
            self.conn.commit()
            return True, f"Attendance marked for {name}."
        except Exception as e:
            return False, str(e)

    def get_attendance_records(self, date_filter=None, student_id=None, department=None):
        query = "SELECT student_id, name, date, time, status, confidence FROM Attendance WHERE 1=1"
        params = []
        if date_filter:
            query += " AND date = ?"
            params.append(date_filter)
        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        if department:
            # We need to join with Students to filter by department
            query = """
                SELECT a.student_id, a.name, a.date, a.time, a.status, a.confidence 
                FROM Attendance a
                JOIN Students s ON a.student_id = s.student_id
                WHERE 1=1
            """
            if date_filter:
                query += " AND a.date = ?"
            if student_id:
                query += " AND a.student_id = ?"
            query += " AND s.department = ?"
            params.append(department)

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def get_today_attendance_count(self):
        date_today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT COUNT(DISTINCT student_id) FROM Attendance WHERE date = ?", (date_today,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialised.")
