import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting {settings.PROJECT_NAME} Backend on http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Interactive Swagger API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
