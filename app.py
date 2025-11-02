from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
from simulated_youtube import SimulatedYouTubeClient
from trivia_engine import TriviaEngine
from database import TriviaDatabase
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

db = TriviaDatabase()
youtube = SimulatedYouTubeClient()  # Modo SIMULADO
trivia = TriviaEngine(db, youtube)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>YouTube Trivia Control</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #1a1a1a; color: white; }
            button { padding: 15px 30px; margin: 10px; font-size: 18px; cursor: pointer; 
                     background: #4CAF50; color: white; border: none; border-radius: 5px; }
            button:hover { background: #45a049; }
            .status { background: #2a2a2a; padding: 20px; border-radius: 5px; margin: 15px 0; }
            h1 { color: #f59e0b; }
        </style>
    </head>
    <body>
        <h1>🎮 YouTube Trivia - Panel de Control</h1>
        <div class="status">
            <h2>Estado:</h2>
            <p id="status">Cargando...</p>
        </div>
        <div>
            <button onclick="startSession()">Nueva Sesion</button>
            <button onclick="loadQuestion()">Cargar Pregunta</button>
            <button onclick="endQuestion()">Finalizar Pregunta</button>
        </div>
        <div class="status">
            <h2>Overlay para OBS:</h2>
            <p><a href="/overlay" target="_blank" style="color: #4CAF50; font-size: 20px;">Abrir Overlay</a></p>
            <p style="color: #999;">URL: http://tu-vps-ip:7500/overlay</p>
        </div>
        
        <script>
            function updateStatus() {
                fetch('/api/state')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('status').innerHTML = 
                            'Estado: ' + data.status + '<br>Sesion: ' + (data.session_id || 'N/A');
                    });
            }
            
            function startSession() {
                fetch('/api/start-session', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => { alert('Sesion iniciada'); updateStatus(); });
            }
            
            function loadQuestion() {
                fetch('/api/load-question', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => { alert('Pregunta cargada'); updateStatus(); });
            }
            
            function endQuestion() {
                fetch('/api/end-question', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => { alert('Pregunta finalizada'); updateStatus(); });
            }
            
            setInterval(updateStatus, 2000);
            updateStatus();
        </script>
    </body>
    </html>
    '''

@app.route('/overlay')
def overlay():
    overlay_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { width: 1920px; height: 1080px; font-family: Arial; background: transparent; }
            
            #question-container { position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%);
                width: 1400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px; padding: 30px; display: none; }
            #question-text { color: white; font-size: 36px; font-weight: bold; text-align: center; }
            #options-container { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
            .option { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px;
                color: white; font-size: 24px; text-align: center; }
            
            #leaderboard { position: absolute; top: 50px; right: 50px; width: 350px;
                background: rgba(0,0,0,0.8); border-radius: 15px; padding: 20px; display: none; }
            #leaderboard h2 { color: #f59e0b; font-size: 28px; text-align: center; margin-bottom: 15px; }
            .leader-item { background: rgba(255,255,255,0.1); padding: 12px; margin: 8px 0;
                border-radius: 8px; display: flex; justify-content: space-between; color: white; }
            .leader-rank { font-size: 24px; font-weight: bold; color: #f59e0b; width: 40px; }
            .leader-name { flex: 1; font-size: 18px; }
            .leader-points { font-size: 20px; font-weight: bold; color: #10b981; }
        </style>
    </head>
    <body>
        <div id="question-container">
            <div id="question-text"></div>
            <div id="options-container"></div>
        </div>
        
        <div id="leaderboard">
            <h2>TOP PLAYERS</h2>
            <div id="leaders-list"></div>
        </div>

        <script>
            async function update() {
                try {
                    const res = await fetch('/api/state');
                    const data = await res.json();
                    
                    if (data.status === 'active' && data.question) {
                        showQuestion(data.question);
                    } else {
                        document.getElementById('question-container').style.display = 'none';
                    }
                    
                    if (data.leaderboard && data.leaderboard.length > 0) {
                        showLeaderboard(data.leaderboard);
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
            
            function showQuestion(q) {
                const container = document.getElementById('question-container');
                const text = document.getElementById('question-text');
                const opts = document.getElementById('options-container');
                
                text.textContent = q.text;
                opts.innerHTML = '';
                
                q.options.forEach(opt => {
                    const div = document.createElement('div');
                    div.className = 'option';
                    div.textContent = opt;
                    opts.appendChild(div);
                });
                
                container.style.display = 'block';
            }
            
            function showLeaderboard(leaders) {
                const list = document.getElementById('leaders-list');
                list.innerHTML = '';
                
                leaders.slice(0, 5).forEach(leader => {
                    const item = document.createElement('div');
                    item.className = 'leader-item';
                    item.innerHTML = 
                        '<span class="leader-rank">#' + leader.rank + '</span>' +
                        '<span class="leader-name">' + leader.user_name + '</span>' +
                        '<span class="leader-points">' + leader.points + '</span>';
                    list.appendChild(item);
                });
                
                document.getElementById('leaderboard').style.display = 'block';
            }
            
            setInterval(update, 500);
            update();
        </script>
    </body>
    </html>
    '''
    return render_template_string(overlay_html)

@app.route('/api/state')
def get_state():
    if trivia.state == 'active':
        trivia.process_answers()
    return jsonify(trivia.get_current_state())

@app.route('/api/start-session', methods=['POST'])
def start_session():
    session_id = trivia.start_new_session()
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/api/load-question', methods=['POST'])
def load_question():
    question = trivia.load_question()
    return jsonify({'success': True, 'question': question})

@app.route('/api/end-question', methods=['POST'])
def end_question():
    results = trivia.end_question()
    return jsonify({'success': True, 'results': results})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7500))
    app.run(host='0.0.0.0', port=port, debug=True)
