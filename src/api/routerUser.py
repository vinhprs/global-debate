from src.middleware.authen import get_current_user
from src.common.response_schema import ResponseModel
from src.model.chat_schema import LoginSchema, UserSchema
import src.service.auth_service as Userservice
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/api/v1/user", tags=["user"], dependencies=[])


@router.post("/login")
async def login(input: LoginSchema):
    input_dict = input.dict()

    response = Userservice.authen(username=input.username, password=input.password)

    if response is None:
        return ResponseModel(
            status_code=409, message="Username or password incorrect!", data=None
        )

    return ResponseModel(
        status_code=200,
        message="Login Successfully!",
        data={"email": response[0], "token": response[1], "name": response[2]},
    )


@router.post("/loginLucete")
async def register(input: LoginSchema):
    data = Userservice.loginLucete(username=input.username, password=input.password)
    if data == None:
        return ResponseModel(
            status_code=404,
            message="Username or password incorrect!",
            data=None,
        )
    return ResponseModel(
        status_code=200,
        message="Login By Lucete Successsfuly!",
        data={"mail": None, "token": data[1], "name": data[0]},
    )


@router.post("/register")
async def register(input: UserSchema):
    data = Userservice.register(
        email=input.email, username=input.username, password=input.password
    )
    if data == None:
        return ResponseModel(
            status_code=409,
            message="User name or email already exists!",
            data=None,
        )
    return ResponseModel(
        status_code=200,
        message="Register Successfully!",
        data={
            "email": data[0],
            "token": data[1],
            "name": data[2],
        },
    )


@router.get("/currentUser")
async def read_users_me(current_user: tuple = Depends(get_current_user)):
    return ResponseModel(
        status_code=200,
        message="Login Successfully!",
        data={
            "email": current_user[2],
            "token": current_user[1],
            "name": current_user[0],
        },
    )
