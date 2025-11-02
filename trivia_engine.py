import time
from datetime import datetime
import uuid
import re

class TriviaEngine:
    def __init__(self, database, youtube_client):
        self.db = database
        self.youtube = youtube_client
        self.current_session = None
        self.current_question = None
        self.question_start_time = None
        self.processed_messages = set()
        self.state = 'idle'
    
    def start_new_session(self):
        """Iniciar nueva sesion de trivia"""
        self.current_session = str(uuid.uuid4())
        self.state = 'idle'
        print(f"Nueva sesion iniciada: {self.current_session}")
        return self.current_session
    
    def load_question(self):
        """Cargar nueva pregunta"""
        self.current_question = self.db.get_random_question()
        self.question_start_time = time.time()
        self.state = 'active'
        self.processed_messages.clear()
        
        options = [self.current_question['correct_answer']] + self.current_question['wrong_answers']
        import random
        random.shuffle(options)
        self.current_question['shuffled_options'] = options
        
        print(f"Pregunta cargada: {self.current_question['question']}")
        return self.current_question
    
    def process_answers(self):
        """Procesar respuestas del chat"""
        if self.state != 'active':
            return []
        
        messages = self.youtube.get_chat_messages()
        new_answers = []
        
        for msg in messages:
            if msg['id'] in self.processed_messages:
                continue
            
            self.processed_messages.add(msg['id'])
            
            user_answer = msg['message'].strip().lower()
            correct_answer = self.current_question['correct_answer'].lower()
            
            is_correct = user_answer == correct_answer
            
            if not is_correct:
                user_clean = re.sub(r'[^\w\s]', '', user_answer)
                correct_clean = re.sub(r'[^\w\s]', '', correct_answer)
                is_correct = user_clean == correct_clean
            
            response_time = time.time() - self.question_start_time
            
            self.db.save_answer(
                self.current_session,
                self.current_question['id'],
                msg['author'],
                msg['message'],
                is_correct,
                response_time
            )
            
            new_answers.append({
                'user': msg['author'],
                'answer': msg['message'],
                'correct': is_correct,
                'time': response_time
            })
            
            if is_correct:
                print(f"Respuesta correcta de {msg['author']}: {msg['message']}")
        
        return new_answers
    
    def get_current_state(self):
        """Obtener estado actual para el overlay"""
        state = {
            'status': self.state,
            'session_id': self.current_session,
            'question': None,
            'leaderboard': []
        }
        
        if self.current_question and self.state == 'active':
            all_options = self.current_question.get('shuffled_options')
            if not all_options:
                all_options = [self.current_question['correct_answer']] + self.current_question['wrong_answers']
            
            state['question'] = {
                'text': self.current_question['question'],
                'options': all_options,
                'category': self.current_question['category'],
                'difficulty': self.current_question['difficulty'],
                'time_elapsed': time.time() - self.question_start_time if self.question_start_time else 0
            }
        
        if self.current_session:
            state['leaderboard'] = self.db.get_leaderboard(self.current_session, limit=5)
        
        return state
    
    def end_question(self):
        """Finalizar pregunta actual"""
        self.state = 'results'
        return {
            'correct_answer': self.current_question['correct_answer'],
            'leaderboard': self.db.get_leaderboard(self.current_session, limit=10)
        }
