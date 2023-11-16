from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.middleware.authen import get_current_user
from src.common.response_schema import ResponseModel
from src.model.chat_schema import ChatSchema, LoginSchema, UserSchema
from src.service.chat_service import chat_bot, get_topic
import src.service.auth_service as Userservice
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel, constr
import src.api.routerUser as userRouter
import src.api.chat as chatRouter


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        error_message = {"msg": error["msg"]}
        error_messages.append(error_message)

    return JSONResponse(
        status_code=409,
        content={"status_code": 409, "message": error["loc"][1] + " " + error["msg"]},
    )


app.include_router(router=userRouter.router)
app.include_router(router=chatRouter.router)

# @app.post("/ingest", response_model=ResponseModel)
# def ingest(input: ChatSchema):
#     result = ingest_data(
#         unit_id=input.unit_id
#     )
#     if result:
#         return ResponseModel(
#             status_code=200,
#             message="Successfully, now you can chat with bot",
#             data=None
#         )
#     else:
#         return ResponseModel(
#             status_code=False,
#             message="Something went wrong",
#             data=None
#         )


# tai lam gap qua nen khong taoj base kip
