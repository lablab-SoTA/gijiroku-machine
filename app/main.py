from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routers import transcribe


def create_app() -> FastAPI:
    app = FastAPI(
        title="ぎじろくさくせい API",
        version="0.1.0",
        description="GPT-4o Transcribe Diariz を利用して会議録を自動生成するバックエンド。",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["system"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    static_dir = Path(__file__).parent.parent / "frontend" / "dist"

    @app.get("/", include_in_schema=False)
    async def index():
        if static_dir.exists():
            return FileResponse(static_dir / "index.html")
        return JSONResponse({"message": "gijiroku-machine API is running"})

    if static_dir.exists():
        assets_dir = static_dir / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/{full_path:path}", include_in_schema=False)
        async def spa_routes(full_path: str):
            return FileResponse(static_dir / "index.html")

    app.include_router(transcribe.router)

    return app


app = create_app()
