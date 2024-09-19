import uvicorn
from src.loader import app
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.APP_BASE_HOST,
        port=settings.APP_BASE_PORT,
        reload=True,
    )
