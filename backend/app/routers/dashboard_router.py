from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings


router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, token: str | None = None):
    """
    Render dashboard page with token-based authentication.
    """
    if token != settings.DASHBOARD_TOKEN:
        return HTMLResponse(content="<h1>403 Forbidden</h1><p>Unauthorized access. Missing or invalid dashboard token.</p>", status_code=403)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )
