from datetime import datetime
import json
from aiohttp import FormData
from sanic import Blueprint, HTTPResponse, Request, text
from sanic_ext import render

from utils import fetch_file, fetch_json

yr = "27"
bp = Blueprint("fy27", url_prefix="/27")


@bp.get("/")
async def index(request: Request):
    return await render("fy26/index.html", context={"yr": yr})


@bp.get("/project/<project_id:str>")
async def project(request: Request, project_id):
    year = "27"
    result = await fetch_json(f"https://apps.dvrpc.org/ords/WORKPROGRAM27/workprogram/projects?proid={project_id}")
    if not result:
        return text(f"Project {project_id} database request failed")
    if result["items"] == []:
        return text(f"Project {project_id} not found")
    csstemplate = await render("fy26/styles.css", context={"pageno": 1})
    resultcss = result.copy()
    resultcss["css"] = csstemplate.body.decode(
    ) if csstemplate.body is not None else ""
    pretemplate = await render("fy26/pre.html", context=resultcss)
    template = ""
    for item in result["items"]:
        item["funding_details"] = json.loads(
            item["funding_details"])
        item["lrpimages"] = json.loads(
            item["lrpimages"]) if item["lrpimages"] else []
        item["yr"] = year
        rendered = await render("fy26/project.html", context=item)
        template += rendered.body.decode() if rendered.body is not None else ""
    posttemplate = await render("fy26/post.html", context=result)
    pretemp = pretemplate.body.decode() if pretemplate.body is not None else ""
    posttemp = posttemplate.body.decode() if posttemplate.body is not None else ""
    submission = await fetch_file("https://cloud.dvrpc.org/api/pdf_gen/pdf", method="POST", data=FormData({"html": pretemp + template + posttemp, "css": resultcss["css"]}))
    return HTTPResponse(body=submission, content_type="application/pdf")


@bp.get("/amendment/<amendment_id:str>")
async def amendment(request: Request, amendment_id):
    result = await fetch_json(f"https://apps.dvrpc.org/ords/WORKPROGRAM27/workprogram/draftamendment?amendmentID={amendment_id}")
    if not result:
        return text(f"Amendment {amendment_id} database request failed")
    if result["items"] == []:
        return text(f"Amendment {amendment_id} not found")
    csstemplate = await render("fy26/styles.css", context={"pageno": 1})
    resultcss = result.copy()
    resultcss["css"] = csstemplate.body.decode(
    ) if csstemplate.body is not None else ""
    pretemplate = await render("fy26/pre.html", context=resultcss)
    template = ""
    for item in result["items"]:
        item["funding_details"] = json.loads(
            item["funding_details"])
        item["lrpimages"] = json.loads(
            item["lrpimages"]) if item["lrpimages"] else []
        item["yr"] = yr
        rendered = await render("fy26/project.html", context=item)
        template += rendered.body.decode() if rendered.body is not None else ""
    posttemplate = await render("fy26/post.html", context=result)
    pretemp = pretemplate.body.decode() if pretemplate.body is not None else ""
    posttemp = posttemplate.body.decode() if posttemplate.body is not None else ""
    submission = await fetch_file("https://cloud.dvrpc.org/api/pdf_gen/pdf", method="POST", data=FormData({"html": pretemp + template + posttemp, "css": resultcss["css"]}))
    return HTTPResponse(body=submission, content_type="application/pdf")


@bp.get("/chapter/<chapter_id:str>")
async def chapter(request: Request, chapter_id):
    pageno = request.args.get("page", "1")
    chapter = {"2A": "DVRPC Program Area Descriptions",
               "2B": "DVRPC Project Descriptions",
               "3A": "PA Supportive Regional Highway Planning Program (SRHPP)",
               "3B": "NJ Supportive Regional Highway Planning Program (SRHPP)",
               "4A": "PA Transit Support Program (TSP)",
               "4B": "NJ Transit Support Program (TSP)",
               "5A": "Other Member Government Projects",
               "5B": "New Jersey CRRSAA-funded Projects",
               "6": "Continuing Projects",
               "": ""}[chapter_id.upper()]
    result = await fetch_json(f"https://apps.dvrpc.org/ords/WORKPROGRAM27/workprogram/projects?chapterno={chapter_id[0]}&subsection={chapter_id.ljust(2).upper()[1]}&showlive=T")
    if not result:
        return text(f"Chapter {chapter_id} not found")
    if result["items"] == []:
        return text(f"No projects found in chapter {chapter_id}")
    result["yr"] = yr
    result["chapter"] = chapter
    result["table"] = request.args.get("table")
    csstemplate = await render("fy26/styles.css", context={"pageno": pageno, "chapter": chapter})
    resultcss = result.copy()
    resultcss["css"] = csstemplate.body.decode(
    ) if csstemplate.body is not None else ""
    pretemplate = await render("fy26/pre.html", context=resultcss)
    toctemplate = await render("fy26/toc.html", context=result)
    template = ""
    for item in result["items"]:
        item["funding_details"] = json.loads(
            item["funding_details"])
        item["lrpimages"] = json.loads(
            item["lrpimages"]) if item["lrpimages"] else []
        rendered = await render("fy26/project.html", context=item)
        template += rendered.body.decode() if rendered.body is not None else ""
    posttemplate = await render("fy26/post.html", context=result)
    pretemp = pretemplate.body.decode() if pretemplate.body is not None else ""
    toctemp = toctemplate.body.decode() if toctemplate.body is not None else ""
    posttemp = posttemplate.body.decode() if posttemplate.body is not None else ""
    submission = await fetch_file("https://cloud.dvrpc.org/api/pdf_gen/pdf", method="POST", data=FormData({"html": pretemp + toctemp + template + posttemp, "css": resultcss["css"]}))
    return HTTPResponse(body=submission, content_type="application/pdf")


@bp.get("/monthlyreport/<mon:path>")
async def monthlyreport(request: Request, mon):
    pageno = request.args.get("page", "1")
    result = await fetch_json(f"https://apps.dvrpc.org/ords/WORKPROGRAM27/workprogram/monthlyReports?repMonth={mon}")
    if not result:
        return text(f"Monthly Report {mon} not found")
    if result["items"] == []:
        return text(f"No projects found in monthly report {mon}")
    month = datetime.strptime(mon, '%m/%d/%Y').strftime('%B')
    year = datetime.strptime(mon, '%m/%d/%Y').strftime('%Y')
    csstemplate = await render("fy26/styles.css", context={"pageno": pageno, "chapter": f"FY20{yr} {month} Progress Report"})
    result["month"] = month
    result["yr"] = year
    resultcss = result.copy()
    resultcss["css"] = csstemplate.body.decode(
    ) if csstemplate.body is not None else ""
    pretemplate = await render("fy26/pre.html", context=resultcss)
    toctemplate = await render("fy26/monthlyreport_cover.html", context=result)
    template = ""
    for item in result["items"]:
        item["month"] = month
        item["year"] = year
        rendered = await render("fy26/monthlyreport_project.html", context=item)
        template += rendered.body.decode() if rendered.body is not None else ""
    posttemplate = await render("fy26/post.html", context=result)
    pretemp = pretemplate.body.decode() if pretemplate.body is not None else ""
    toctemp = toctemplate.body.decode() if toctemplate.body is not None else ""
    posttemp = posttemplate.body.decode() if posttemplate.body is not None else ""
    submission = await fetch_file("https://cloud.dvrpc.org/api/pdf_gen/pdf", method="POST", data=FormData({"html": pretemp + toctemp + template + posttemp, "css": resultcss["css"]}))
    return HTTPResponse(body=submission, content_type="application/pdf")


@bp.get("/semiannualreport")
async def semiannualreport(request: Request):
    return text(f"Semiannual report")


@bp.get("/annualreport")
async def annualreport(request: Request):
    return text(f"Annual report")
