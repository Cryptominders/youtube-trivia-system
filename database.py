import sqlite3
import json
from datetime import datetime

class TriviaDatabase:
    def __init__(self, db_path='trivia.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializar base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                wrong_answers TEXT NOT NULL,
                category TEXT,
                difficulty TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                current_question_id INTEGER,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                user_answer TEXT NOT NULL,
                is_correct BOOLEAN,
                response_time REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                session_id TEXT NOT NULL,
                user_name TEXT NOT NULL,
                total_points INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                total_answers INTEGER DEFAULT 0,
                PRIMARY KEY (session_id, user_name)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.insert_sample_questions()
    
    def insert_sample_questions(self):
        """Insertar preguntas de ejemplo sobre Bitcoin Cash"""
        sample_questions = [
            {
                "question": "En que ano se creo Bitcoin Cash?",
                "correct_answer": "2017",
                "wrong_answers": ["2016", "2018", "2015"],
                "category": "BCH History",
                "difficulty": "easy"
            },
            {
                "question": "Cual es el tamano maximo de bloque de BCH?",
                "correct_answer": "32MB",
                "wrong_answers": ["1MB", "8MB", "16MB"],
                "category": "BCH Technical",
                "difficulty": "medium"
            },
            {
                "question": "Que significa BCH?",
                "correct_answer": "Bitcoin Cash",
                "wrong_answers": ["Bitcoin Chain", "Blockchain Cash", "Bitcoin Core"],
                "category": "BCH Basics",
                "difficulty": "easy"
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for q in sample_questions:
            cursor.execute('SELECT id FROM questions WHERE question = ?', (q['question'],))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO questions (question, correct_answer, wrong_answers, category, difficulty)
                    VALUES (?, ?, ?, ?, ?)
                ''', (q['question'], q['correct_answer'], json.dumps(q['wrong_answers']), 
                      q['category'], q['difficulty']))
        
        conn.commit()
        conn.close()
    
    def get_random_question(self):
        """Obtener una pregunta aleatoria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
        question = cursor.fetchone()
        conn.close()
        
        if question:
            return {
                'id': question[0],
                'question': question[1],
                'correct_answer': question[2],
                'wrong_answers': json.loads(question[3]),
                'category': question[4],
                'difficulty': question[5]
            }
        return None
    
    def save_answer(self, session_id, question_id, user_name, user_answer, is_correct, response_time):
        """Guardar respuesta de usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO answers (session_id, question_id, user_name, user_answer, is_correct, response_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, question_id, user_name, user_answer, is_correct, response_time))
        
        points = 100 if is_correct else 0
        correct_add = 1 if is_correct else 0
        
        cursor.execute('''
            INSERT INTO leaderboard (session_id, user_name, total_points, correct_answers, total_answers)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(session_id, user_name) DO UPDATE SET
                total_points = total_points + ?,
                correct_answers = correct_answers + ?,
                total_answers = total_answers + 1
        ''', (session_id, user_name, points, correct_add, points, correct_add))
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self, session_id, limit=10):
        """Obtener leaderboard de sesion actual"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_name, total_points, correct_answers, total_answers
            FROM leaderboard
            WHERE session_id = ?
            ORDER BY total_points DESC, correct_answers DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'rank': idx + 1,
                'user_name': row[0],
                'points': row[1],
                'correct': row[2],
                'total': row[3]
            }
            for idx, row in enumerate(results)
        ]
