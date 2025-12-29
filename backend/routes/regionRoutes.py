from fastapi import APIRouter, Request
import backend.regionFunctions.regionController as regionController
from backend.regionFunctions.regionController import Region
router = APIRouter()

@router.post("/api/region", tags=["region"])
async def create_region(region: Region):
    return await regionController.add_region(region)

@router.get("/api/region", tags=["region"])
async def get_region(region: Region):
    return await regionController.get_region(region)
