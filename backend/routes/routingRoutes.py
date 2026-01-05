from fastapi import FastAPI, APIRouter
import backend.Controllers.routingController as routingController

router = APIRouter()

@router.get("/api/routing/calculate", tags=["routing"])
async def calculate_route(startLat: float, startLong: float, endLat: float, endLong: float, distance: float):
    return await routingController.calculate_route(startLat, startLong, endLat, endLong, distance)