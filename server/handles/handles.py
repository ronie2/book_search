import aiohttp_jinja2
from config.conf import cfg
from sender import send_email
from mongo_search import mongo_search

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
            write_log(status="BEGIN")
            result = "\n".join(list(find_phrase(job["searchinput"])))
            if len(result) == 0:
                result = "Phrase was not found!"
            enqueue_email(result, job["email"], job["searchinput"])
            write_log(status="END")
            return {
                "message": "Search started for this request: " + str(job["searchinput"]) + "<br>" +
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

def find_phrase(search_term):
    for result in mongo_search(search_term):
        sub_mail = """
        In book: {book_name}
        In part: {part_name}
        In chapter: {chapter_name}
        In paragraph #: {paragraph_num}
        Text:
        {paragraph_text}
        """.format(book_name=result["result"]["book"],
                   part_name=result["result"]["part"],
                   chapter_name=result["result"]["chapter"],
                   paragraph_num=result["result"]["paragraph"],
                   paragraph_text=result["result"]["text"]
                   )
        yield sub_mail

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