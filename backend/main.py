from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import whiteboard_router
import uvicorn

app = FastAPI(
    title="Collaborative Realtime Whiteboard API",
    description="WebSocket streaming canvas coordination, event dispatching, and stroke synchronization.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(whiteboard_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "collaborative-realtime-whiteboard"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
