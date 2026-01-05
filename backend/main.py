import uvicorn
from fastapi import FastAPI
import backend.routes.regionRoutes as regionRoutes
import backend.routes.routingRoutes as routingRoutes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running..."}

app.include_router(regionRoutes.router, tags=["region"])
app.include_router(routingRoutes.router, tags=["routing"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)