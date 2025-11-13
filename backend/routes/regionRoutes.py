from fastapi import APIRouter, Request
import backend.regionFunctions.regionController as regionController

router = APIRouter()

@router.post("/region", tags=["region"])
async def create_region(request: Request):
    return regionController.add_region(request)