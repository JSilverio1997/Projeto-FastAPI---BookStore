from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Home")
async def home():
    return {"message": "Welcome to my bookstore"}
