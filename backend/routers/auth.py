from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.db import get_db

from database.crud import (
    create_user,
    get_user_by_email
)

from utils.security import (
    hash_password,
    verify_password
)

from auth.jwt_handler import create_access_token

from schemas.auth import (
    UserRegister,
    UserLogin,
    LoginResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = create_user(
        db=db,
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    return {
        "message": "User registered successfully.",
        "user_id": new_user.id
    }

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = get_user_by_email(
        db,
        user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id)
        }
    )

    return LoginResponse(
        access_token=access_token
    )