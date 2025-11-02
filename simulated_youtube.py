import time
import random

class SimulatedYouTubeClient:
    """Cliente simulado para testing sin YouTube"""
    def __init__(self):
        self.live_chat_id = "simulated-chat-123"
        self.message_counter = 0
        self.simulated_users = ["Juan", "Maria", "Carlos", "Ana", "Pedro", "Sofia"]
        
    def get_live_chat_id(self):
        print("Modo SIMULADO activado")
        return self.live_chat_id
    
    def get_chat_messages(self):
        """Genera respuestas aleatorias simuladas"""
        messages = []
        
        # Simular 2-3 respuestas aleatorias
        num_responses = random.randint(2, 3)
        
        for i in range(num_responses):
            self.message_counter += 1
            user = random.choice(self.simulated_users)
            
            # Generar respuesta aleatoria
            possible_answers = ["2017", "32MB", "Bitcoin Cash", "2016", "1MB"]
            answer = random.choice(possible_answers)
            
            messages.append({
                'id': f'sim-msg-{self.message_counter}',
                'author': user,
                'message': answer,
                'timestamp': time.time()
            })
        
        return messages
