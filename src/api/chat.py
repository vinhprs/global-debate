from src.model.chat_schema import ChatSchema
from src.common.response_schema import ResponseModel
from fastapi import APIRouter
from src.service.chat_service import chat_bot, get_topic

router = APIRouter(prefix="/api/v1/gpt", tags=["gpt"], dependencies=[])

@router.get("/")
async def chat():
    return {"message": "hello"}


@router.get("/topic", response_model=ResponseModel)
async def chat():
    response = get_topic()
    return ResponseModel(status_code=200, message="Get successfully", data=response)


@router.post("/chatbot/")
async def chat(input: ChatSchema):
    response = chat_bot(
        topic_id=input.topic_id, unit_id=input.unit_id, prompt=input.prompt
    )
    return ResponseModel(
        status_code=200,
        message="Chatbot return successfully",
        data={"answer": response},
    )
