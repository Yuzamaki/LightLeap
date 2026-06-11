from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import ai, auth, dashboard, exercises, meals, water, weight


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(meals.router, prefix="/api/v1/meals", tags=["饮食记录"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["运动记录"])
app.include_router(water.router, prefix="/api/v1/water", tags=["喝水追踪"])
app.include_router(weight.router, prefix="/api/v1/weight", tags=["体重趋势"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["仪表盘"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])


@app.get("/")
async def root():
    return {"message": "LightLeap API is running"}
