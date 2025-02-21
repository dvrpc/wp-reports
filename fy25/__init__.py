from sanic import Blueprint, Request, text

bp = Blueprint("fy25", url_prefix="/25")


@bp.get("/")
async def index(request: Request):
    return text("Hello World!")


@bp.get("/project/:project_id")
async def project(request: Request, project_id):
    return text(f"Project {project_id}")


@bp.get("/chapter/:chapter_id")
async def chapter(request: Request, chapter_id):
    return text(f"Chapter {chapter_id}")


@bp.get("/monthlyreport/:month")
async def monthlyreport(request: Request, month):
    return text(f"Monthly report for {month}")


@bp.get("/semiannualreport/")
async def semiannualreport(request: Request):
    return text(f"Semiannual report")


@bp.get("/annualreport/")
async def annualreport(request: Request):
    return text(f"Annual report")
