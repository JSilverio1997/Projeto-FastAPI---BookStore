from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Home", description="Root endpoint that confirms the API is running")
async def home() -> dict[str, str]:
    return {"message": "Welcome to my repositories", "version": "1.0.0"}
