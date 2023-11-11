from fastapi import FastAPI
from src.model.chat_schema import ChatSchema
from src.service.chat_service import chat_bot, get_book
app = FastAPI()

@app.post('/chatbot/')
async def chat(
    input: ChatSchema
):
    response = chat_bot(
        unit=input.unit,
        prompt=input.prompt
    )
    return {
        "code": 200,
        "answer": response
    }

@app.get('/book')
async def chat():
    response = get_book()
    return {
        "code": 200,
        "books": response
    }