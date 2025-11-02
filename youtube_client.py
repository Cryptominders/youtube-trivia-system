from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
import time

load_dotenv()

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.live_chat_id = None
        self.last_check_time = None
    
    def get_live_chat_id(self):
        """Obtener el ID del chat en vivo actual"""
        try:
            request = self.youtube.liveBroadcasts().list(
                part='snippet',
                broadcastStatus='active',
                maxResults=1
            )
            response = request.execute()
            
            if response['items']:
                self.live_chat_id = response['items'][0]['snippet']['liveChatId']
                print(f"Chat ID encontrado: {self.live_chat_id}")
                return self.live_chat_id
            else:
                print("No hay transmisiones en vivo activas")
                return None
        except HttpError as e:
            print(f"Error obteniendo chat ID: {e}")
            return None
    
    def get_chat_messages(self):
        """Obtener mensajes del chat en vivo"""
        if not self.live_chat_id:
            if not self.get_live_chat_id():
                return []
        
        try:
            request = self.youtube.liveChatMessages().list(
                liveChatId=self.live_chat_id,
                part='snippet,authorDetails',
                maxResults=200
            )
            response = request.execute()
            
            messages = []
            for item in response['items']:
                message = {
                    'id': item['id'],
                    'author': item['authorDetails']['displayName'],
                    'message': item['snippet']['displayMessage'],
                    'timestamp': item['snippet']['publishedAt']
                }
                messages.append(message)
            
            self.last_check_time = response.get('pollingIntervalMillis', 5000)
            
            return messages
        
        except HttpError as e:
            print(f"Error obteniendo mensajes: {e}")
            return []
