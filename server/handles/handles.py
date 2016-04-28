from aiohttp import web
import aiohttp_jinja2
from config.conf import cfg, db_path
from sender import send_email

@aiohttp_jinja2.template('search.jinja2')
async def search_handle(request):
    if request.method == "GET":
        return {
            "name": "Roman",
            "title": cfg["server"]["search"]["config"]["jinja2"]["title"],
            "legend": cfg["server"]["search"]["config"]["jinja2"]["legend"]
        }

@aiohttp_jinja2.template('result.jinja2')
async def result_handle(request):
    from validate_email import validate_email
    if request.method == "GET":
        job = request.GET
        if len(job) == 0:
            return {
                "message": "No info to process!<br>Please provide valid info to process!",
                "status_code": 0,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }
        elif validate_email(job["email"], check_mx=True):

            result = find_phrase(job["searchinput"], db_path)

            enqueue_email(result, job["email"], job["searchinput"])
            return {
                "message": "Search started for this request: " + str(job["searchinput"]) + "<br>" + \
                           "Results will be sent to this e-mail: " + str(job["email"]),
                "status_code": 1,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }
        else:
            return {
                "message": "Wrong e-mail!<br>Please provide valid e-mail!",
                "status_code": 0,
                "title": cfg["server"]["result"]["config"]["jinja2"]["title"]
            }

def find_phrase(phrase, txt_file):
    write_log(status="BEGIN")
    phrase = str(phrase)
    if phrase[0] != " ":
        phrase = " " + phrase

    if phrase[-1] != " ":
        phrase = phrase + " "

    result = []

    try:
        with open(txt_file, "r+") as f:
            i = 1
            for line in f:
                i = i + 1
                if phrase in line:
                    result.append(("In line #: " + str(i) + " -> " + str(line.rstrip())))
    except Exception as e:
        return e
    if len(result) == 0:
        return "Phrase was not found!"
    write_log(status="END")
    return "\n".join(result)


def write_log(status, log_file_name="log.log"):
    import os
    # Check if file exists and create file if it doesn't
    if not os.path.isfile(log_file_name):
        with open(log_file_name, "w") as f:
            pass

    import datetime
    mode = "a+"
    with open(log_file_name, mode, encoding="utf-8") as log:
        if status == "BEGIN":
            log.write("BEGIN AT: " + str(datetime.datetime.now()) + "\n")
        elif status == "END":
            log.write("END AT: " + str(datetime.datetime.now())+ "\n\n")

def enqueue_email(results, receiver, request):
    from rq import Queue
    from redis import Redis

    redis_conn = Redis()
    q = Queue(connection=redis_conn)

    job = q.enqueue(send_email, results, receiver, request)

    return