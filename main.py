from fastapi import FastAPI
from src.common.response_schema import ResponseModel
from src.model.chat_schema import ChatSchema, LoginSchema, UserSchema
from src.service.chat_service import chat_bot, get_book
import src.service.auth_service as Userservice
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/chatbot/")
async def chat(input: ChatSchema):
    response = chat_bot(unit=input.unit, prompt=input.prompt)
    return {"code": 200, "answer": response}


@app.get("/book")
async def chat():
    response = get_book()
    return {"code": 200, "books": response}


@app.post("/login")
async def login(input: LoginSchema):
    response = Userservice.authen(username=input.username, password=input.password)
    if response == None:
        return ResponseModel(
            status_code=409,
            message="Login Field!",
            data=None,
        )
    return ResponseModel(
        status_code=200,
        message="Login Successsfuly!",
        data={
            "name": response[0],
            "token": response[1],
        },
    )


@app.post("/register")
async def register(input: UserSchema):
    data = Userservice.register(
        name=input.name, username=input.username, password=input.password
    )
    if data == None:
        return ResponseModel(
            status_code=False,
            message="Register Field!",
            data={None},
        )
    return ResponseModel(
        status_code=200,
        message="Register Successsfuly!",
        data={
            "name": data[0],
            "token": data[1],
        },
    )


@app.post("/loginLucate")
async def register(input: LoginSchema):
    data = Userservice.loginLucete(username=input.username, password=input.password)
    if data == None:
        return ResponseModel(
            status_code=404,
            message="Login By Lucete Feild!",
            data={None},
        )
    return ResponseModel(
        status_code=200,
        message="Login By Lucete Successsfuly!",
        data={
            "name": data[0],
            "token": data[1],
        },
    )


# tai lam gap qua nen khong taoj base kip
