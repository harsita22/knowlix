"""FastAPI application factory for Knowlix."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.connection import init_db
from database.seed_data import seed_all
from server.routes import auth_routes, student_routes, teacher_routes, agent_routes

app = FastAPI(
    title="Knowlix AI Educational Platform",
    description="Adaptive Learning & Personalized Pedagogy Platform powered by ReAct multi-agent coordination.",
    version="1.0.0"
)

# Enable CORS for React frontend (default Vite port 5173 / React port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(teacher_routes.router)
app.include_router(agent_routes.router)


@app.on_event("startup")
def on_startup():
    init_db()
    seed_all()


@app.get("/health")
def health_check():
    return {"status": "healthy", "platform": "Knowlix", "version": "1.0.0"}


# Serve built React frontend if dist directory exists
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

