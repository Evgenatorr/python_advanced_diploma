from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from config import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)
router = APIRouter(tags=['GET'])


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
