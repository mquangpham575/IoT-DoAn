from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings


router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Render dashboard page.

    The current dashboard.html can be improved later in phase 3.
    """
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )
