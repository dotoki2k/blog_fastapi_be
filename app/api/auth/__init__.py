import logging

from fastapi import APIRouter, Body, HTTPException, status, Depends, security
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    read_data,
    write_data,
)
from app.deps import get_current_user

router = APIRouter()
logger = logging.getLogger("blog_fastapi")


@router.post("/healthcheck")
async def get():
    return {"message": "Health check success"}


@router.post("/signup")
def sign_up(
    username: str = Body(title="username"), password: str = Body(title="password")
):
    """Sign up new user."""
    try:
        users = read_data()
        user = users.get(username)
        if user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": f"Username already exists"},
            )

        new_user_id = len(users) + 1
        new_user = {
            "username": username,
            "password": get_hashed_password(password),
            "user_id": new_user_id,
        }
        users[username] = new_user
        write_data(users)
        return {"message": f"User {username} registered successfully"}
    except Exception as e:
        logger.exception("An error occurred while sign up new user!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while sign up new user",
        )


@router.post("/login", summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = read_data().get(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    hashed_pass = user["password"]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"]),
    }


@router.get("/me", summary="Get details of currently logged in user")
async def get_me(user=Depends(get_current_user)):
    return user
