# app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import JSONResponse
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

# Инициализация клиента Telegram
async def create_telegram_client():
    client = TelegramClient(
        StringSession(os.getenv('SESSION_STRING')),
        int(os.getenv('API_ID')),
        os.getenv('API_HASH')
    )
    await client.start()
    return client

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Старт приложения
    app.state.telegram_client = await create_telegram_client()
    yield
    # Завершение работы приложения
    await app.state.telegram_client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/api/message")
async def send_message(
    key: str = Query(..., description="Секретный ключ для доступа"),
    user: str = Query(..., description="Имя пользователя или chat_id получателя"),
    message: str = Query(..., description="Текст сообщения для отправки")
):
    # Проверка секретного ключа
    if key != os.getenv('SECRET_KEY'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid security key"
        )

    try:
        # Отправка сообщения
        await app.state.telegram_client.send_message(user, message)
        return JSONResponse(
            content={"status": "success"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)