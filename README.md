# 🎮 YouTube Trivia System

Sistema interactivo de trivias en vivo para YouTube Live con preguntas sobre Bitcoin Cash y criptomonedas.

![Status](https://img.shields.io/badge/status-MVP-success)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Características

- ✅ **Sistema de trivias en tiempo real** para YouTube Live
- ✅ **Leaderboard dinámico** con puntuación automática
- ✅ **Overlay visual** para OBS Studio
- ✅ **Panel de control web** para gestionar trivias
- ✅ **Base de datos SQLite** con preguntas personalizables
- ✅ **Modo simulado** para testing sin YouTube
- ✅ **Preguntas sobre BCH y crypto** incluidas

## 📋 Requisitos

- Python 3.8+
- YouTube Data API v3 (con OAuth2 para producción)
- OBS Studio (para el overlay)
- Ubuntu/Debian Linux (recomendado)

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/Cryptominders/youtube-trivia-system.git
cd youtube-trivia-system
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env`:
```env
YOUTUBE_API_KEY=tu_api_key_aqui
YOUTUBE_CHANNEL_ID=

FLASK_ENV=development
SECRET_KEY=tu-clave-secreta

HOST=0.0.0.0
PORT=7500
```

## 🎯 Uso

### Modo Simulado (Testing)

Para probar sin YouTube Live activo:
```bash
python app.py
```

Abre en tu navegador:
- Panel de control: `http://localhost:7500`
- Overlay: `http://localhost:7500/overlay`

### Flujo de trabajo:

1. **Nueva Sesión**: Inicia una nueva sesión de trivia
2. **Cargar Pregunta**: Muestra una pregunta en el overlay
3. Los viewers responden en el chat de YouTube
4. **Finalizar Pregunta**: Muestra resultados y leaderboard

## 🎨 Configurar OBS

1. Agregar fuente → **Browser**
2. URL: `http://tu-servidor:7500/overlay`
3. Ancho: **1920**
4. Alto: **1080**
5. FPS: **30**

## 📊 Estructura del Proyecto
```
youtube-trivia-system/
├── app.py                    # Aplicación Flask principal
├── database.py              # Gestión de base de datos
├── trivia_engine.py         # Lógica de trivias
├── youtube_client.py        # Cliente YouTube API
├── simulated_youtube.py     # Simulador para testing
├── requirements.txt         # Dependencias
└── .env                     # Configuración (no incluido)
```

## 🔧 Modo Producción con YouTube Real

Para conectar con YouTube Live real, necesitas configurar OAuth2:

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar YouTube Data API v3
3. Crear credenciales OAuth2
4. Descargar `client_secrets.json`
5. Modificar `youtube_client.py` para usar OAuth2

*Documentación detallada próximamente*

## 📝 Agregar Preguntas

Edita `database.py` y agrega preguntas en el método `insert_sample_questions()`:
```python
{
    "question": "Tu pregunta aquí?",
    "correct_answer": "Respuesta correcta",
    "wrong_answers": ["Opción 2", "Opción 3", "Opción 4"],
    "category": "BCH",
    "difficulty": "easy"
}
```

## 🛣️ Roadmap

### v1.0 (Actual - MVP)
- [x] Sistema básico de trivias
- [x] Modo simulado
- [x] Overlay visual
- [x] Leaderboard

### v1.1 (Próximo)
- [ ] OAuth2 para YouTube real
- [ ] Sistema de puntos por velocidad
- [ ] Sonidos y animaciones
- [ ] Panel admin mejorado

### v2.0 (Futuro)
- [ ] WebSockets para actualizaciones instantáneas
- [ ] Multi-idioma
- [ ] Sistema de premios/donaciones
- [ ] Integración con Twitch

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- **CryptoMinders** - [YouTube Channel](https://youtube.com/@cryptominders)
- Desarrollado con la asistencia de **Claude AI**

## 🙏 Agradecimientos

- Comunidad Bitcoin Cash
- Monero Community
- OBS Studio Project
- Flask Framework

## 📞 Soporte

Para preguntas o soporte:
- Email: cryptomindersyt@gmail.com
- Issues: [GitHub Issues](https://github.com/Cryptominders/youtube-trivia-system/issues)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
