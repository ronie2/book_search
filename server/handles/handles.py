import logging
import aiohttp_jinja2
from aiohttp import web
from config.conf import cfg, sub_message, logger_msg
from sender import send_email
from mongo_search import mongo_search
from datetime import datetime
from handles.plugins import get_log
from uuid import uuid4


# 'Parser page'
@aiohttp_jinja2.template("parser.jinja2")
async def book_parser_handle(request):
    if request.method == "POST":
        data = await request.post()
        job = {
            "title": data["title"],
            "file": data["book"].file,
            "filename": data["book"].filename,
            "uid": uuid4(),
        }

        content = job["file"].read()

        with open(job["filename"], "wb") as f:
            f.write(content)
        return web.Response(body=content)

    # If request metod GET => render jinja form
    if request.method == "GET":
        return {
            "title": cfg["server"]["book_parser"]["config"]["jinja2"]["title"],
            "legend": cfg["server"]["book_parser"]["config"]["jinja2"]["legend"]
        }



# 'Search page' jinja2 template preparation
@aiohttp_jinja2.template('search.jinja2')
async def search_handle(request):
    if request.method == "GET":
        return {
            "title": cfg["server"]["search"]["config"]["jinja2"]["title"],
            "legend": cfg["server"]["search"]["config"]["jinja2"]["legend"]
        }


# 'Results page' jinja2 template preparation
@aiohttp_jinja2.template('result.jinja2')
async def result_handle(request):
    from validate_email import validate_email
    if request.method == "GET":

        # Awaiting request
        job = {
            "request": request.GET,
            "uid": uuid4(),
        }

        # If no search term info was given => show error notification
        if len(job["request"]) == 0:
            logging.info(logger_msg["invalid_search"])
            # Return data for 'Results page' to jinja2 template engine
            return {
                "message": "No info to process!<br>Please provide valid info to process!",
                "status_code": 0,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }

        # If given email is valid
        elif validate_email(job["request"]["email"], check_mx=True):
            logging.info(logger_msg["valid_request"].format(uid=job["uid"],
                                                            term=job["request"]["searchinput"],
                                                            e_mail=job["request"]["email"]))

            started_at = datetime.now()
            logging.info(logger_msg["search_started"].format(uid=job["uid"],
                                                             time=datetime.now()))

            # Get list of search results 'sub-emails'
            result = "\n".join(list(find_phrase(job["request"]["searchinput"])))

            finished_at = datetime.now()
            logging.info(logger_msg["search_finished"].format(uid=job["uid"],
                                                              time=finished_at,
                                                              delta=finished_at - started_at))

            # If list of 'sub-emails' is empty => send nothing was found message
            if len(result) == 0:
                result = "Phrase was not found!"

            # If validators pass => enqueue e-mail for sending by RQ
            enqueue_email(result, job["request"]["email"], job["request"]["searchinput"])

            # Return data for 'Results page' to jinja2 template engine
            return {
                "message": "Search started for this request: " + str(job["request"]["searchinput"]) + "<br>" +
                           "Results will be sent to this e-mail: " + str(job["request"]["email"]),
                "status_code": 1,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }

        # If given email is NOT valid
        else:
            logging.info(logger_msg["invalid_email"].format(uid=job["uid"],
                                                            e_mail=job["request"]["email"]))

            # Return data for 'Results page' to jinja2 template engine
            return {
                "message": "Wrong e-mail!<br>Please provide valid e-mail!",
                "status_code": 0,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }


async def log_app(request):
    if request.method == "GET":
        return web.Response(text=await get_log(log_file_name=cfg["server"]["app_log"]["config"]["log_file"]))


def find_phrase(search_term):
    for result in mongo_search(search_term):
        sub_mail = sub_message.format(
            book_name=result["result"]["book"],
            part_name=result["result"]["part"],
            chapter_name=result["result"]["chapter"],
            paragraph_num=result["result"]["paragraph"],
            paragraph_text=result["result"]["text"]
        )
        yield sub_mail


def enqueue_email(results, receiver, request):
    from rq import Queue
    from redis import Redis

    redis_conn = Redis()
    q = Queue(connection=redis_conn)
    q.enqueue(send_email, results, receiver, request)
