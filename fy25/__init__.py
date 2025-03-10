import json
from aiohttp import FormData
from sanic import Blueprint, HTTPResponse, Request, text
from sanic_ext import render

from utils import fetch_file, fetch_json

yr = "25new"
bp = Blueprint("fy25", url_prefix="/25")


@bp.get("/")
async def index(request: Request):
    return text("Hello World!")


@bp.get("/project/<project_id:str>")
async def project(request: Request, project_id):
    result = await fetch_json(f"https://apps.dvrpc.org/ords/workprogram{yr}/workprogram/projects?proid={project_id}")
    if not result:
        return text(f"Project {project_id} database request failed")
    if result["items"] == []:
        return text(f"Project {project_id} not found")
    csstemplate = await render("fy26/styles.css", context={"pageno": 1})
    resultcss = result.copy()
    resultcss["css"] = csstemplate.body.decode()
    pretemplate = await render("fy26/pre.html", context=resultcss)
    template = ""
    for item in result["items"]:
        item["funding_details"] = json.loads(
            item["funding_details"])
        item["lrpimages"] = json.loads(
            item["lrpimages"]) if item["lrpimages"] else []
        template += (await render("fy26/project.html", context=item)).body.decode()
    posttemplate = await render("fy26/post.html", context=result)
    submission = await fetch_file("https://cloud.dvrpc.org/api/pdf_gen/pdf", method="POST", data=FormData({"html": pretemplate.body.decode() + template + posttemplate.body.decode(), "css": csstemplate.body.decode()}))
    return HTTPResponse(body=submission, content_type="application/pdf")


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
