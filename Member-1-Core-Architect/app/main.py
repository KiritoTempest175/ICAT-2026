from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="AI Study Companion")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the endpoints defined by Member 1
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "online", "message": "Core Architecture is functional"}