from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.database.repository import (
    create_user,
    get_user_by_username,
    list_users,
    update_user_password,
)
from backend.security.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    is_password_change_required,
)

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
    role: str
    password_changed: bool
    change_required: bool


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str


class ChangePasswordRequest(BaseModel):
    new_password: str


class UserResponse(BaseModel):
    username: str
    role: str
    password_changed: bool


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        username=user.username,
        role=user.role,
    )

    password_changed = bool(getattr(user, "password_changed", False))
    change_required = is_password_change_required(user)

    return LoginResponse(
        token=token,
        username=user.username,
        role=user.role,
        password_changed=password_changed,
        change_required=change_required,
    )


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):

    return UserResponse(
        username=current_user["username"],
        role=current_user["role"],
        password_changed=current_user["password_changed"],
    )


@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_user),
):

    update_user_password(
        username=current_user["username"],
        password_hash=hash_password(request.new_password),
        password_changed=True,
    )

    return {
        "success": True,
        "message": "Password updated successfully",
    }


@router.get("/users", response_model=list[UserResponse])
def get_users(current_user=Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )

    return [
        UserResponse(
            username=user.username,
            role=user.role,
            password_changed=bool(getattr(user, "password_changed", False)),
        )
        for user in list_users()
    ]


@router.post("/users", response_model=UserResponse)
def create_new_user(
    request: CreateUserRequest,
    current_user=Depends(get_current_user),
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )

    if get_user_by_username(request.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    if request.role not in ["viewer", "operator", "admin"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = create_user(
        username=request.username,
        password_hash=hash_password(request.password),
        role=request.role,
        password_changed=True,
    )

    return UserResponse(
        username=user.username,
        role=user.role,
        password_changed=bool(getattr(user, "password_changed", False)),
    )
