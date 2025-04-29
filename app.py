# app.py
from quart import Quart, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

app = Quart(__name__)

# Конфигурация из переменных окружения
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret')

# Инициализация клиента Telegram
client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

@app.route('/api/message', methods=['GET'])
async def send_message():
    # Проверка секретного ключа
    if request.args.get('key') != SECRET_KEY:
        return jsonify({"status": "error", "message": "Invalid key"}), 403
    
    # Получение параметров
    user = request.args.get('user')
    message = request.args.get('message')
    
    if not user or not message:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    
    try:
        # Отправка сообщения
        await client.send_message(user, message)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.before_serving
async def startup():
    await client.start()

@app.after_serving
async def shutdown():
    await client.disconnect()

if __name__ == '__main__':
    app.run()