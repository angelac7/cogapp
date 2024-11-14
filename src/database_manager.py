import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('cognicore.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        tables = {
            'exercise_results': '''
                CREATE TABLE IF NOT EXISTS exercise_results (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    difficulty TEXT,
                    score INTEGER,
                    completion_time REAL,
                    date TEXT,
                    correct INTEGER
                )''',
            'user_profile': '''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    current_streak INTEGER,
                    total_exercises INTEGER,
                    average_score REAL
                )''',
            'goals': '''
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    target_score INTEGER,
                    deadline TEXT,
                    completed INTEGER
                )'''
        }
        [self.cursor.execute(query) for query in tables.values()]
        self.conn.commit()

    def save_result(self, category, difficulty, score, completion_time, correct):
        self.cursor.execute(
            'INSERT INTO exercise_results (category, difficulty, score, completion_time, date, correct) VALUES (?, ?, ?, ?, ?, ?)',
            (category, difficulty, score, completion_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1 if correct else 0)
        )
        self.conn.commit()

    def get_progress_data(self, category=None, limit=30):
        return self.cursor.execute(
            'SELECT * FROM exercise_results WHERE ' + ('category = ? AND ' if category else '') + 'date IS NOT NULL ORDER BY date DESC LIMIT ?',
            ((category, limit) if category else (limit,))
        ).fetchall()

    def get_statistics(self):
        return self.cursor.execute('''
            SELECT COUNT(*), AVG(score), SUM(correct), AVG(completion_time) 
            FROM exercise_results
        ''').fetchone()

    def get_category_stats(self):
        return self.cursor.execute('''
            SELECT category, COUNT(*), AVG(score), MAX(score)
            FROM exercise_results GROUP BY category
        ''').fetchall()

    def save_goal(self, category, target_score, deadline):
        self.cursor.execute(
            'INSERT INTO goals (category, target_score, deadline, completed) VALUES (?, ?, ?, 0)',
            (category, target_score, deadline)
        )
        self.conn.commit()

    def update_goal_progress(self, goal_id, completed):
        self.cursor.execute(
            'UPDATE goals SET completed = ? WHERE id = ?',
            (1 if completed else 0, goal_id)
        )
        self.conn.commit()

    def get_active_goals(self):
        return self.cursor.execute('''
            SELECT * FROM goals 
            WHERE completed = 0 AND deadline >= date('now') 
            ORDER BY deadline
        ''').fetchall()

    def reset_progress(self):
        try:
            [self.cursor.execute(f'DELETE FROM {table}') for table in ['exercise_results', 'goals']]
            self.cursor.execute('UPDATE user_profile SET current_streak = 0, total_exercises = 0, average_score = 0')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error resetting progress: {e}")

    def close(self):
        self.conn.close()