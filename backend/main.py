import uvicorn
from fastapi import FastAPI
import backend.routes.regionRoutes as regionRoutes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running..."}

app.include_router(regionRoutes.router, tags=["region"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)