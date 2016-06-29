cfg = {
    "service": {
        "home": {
            "host": None,  # Host will be assigned automatically
            "port": 5001,
        },
        "email": {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 465,
            "login": "book.search.app.test@gmail.com",
            "password": "book.search.app.test111",

        }
    },
    "server": {
        "search": {
            "config": {
                "method": "*",
                "endpoint": "/",
                "handle": "search_handle",
                "timeout": 0,
                "log_file": "search_handle.log",
                "jinja2": {
                    "title": "Welcome to book search!",
                    "legend": "Book Search Service"
                }
            },

        },
        "result": {
            "config": {
                "method": "*",
                "endpoint": "/result",
                "handle": "result_handle",
                "timeout": 0,
                "log_file": "result_handle.log",
                "jinja2": {
                    "title": "Thank you! Search started!"
                }
            },
        },
        "app_log": {
            "config": {
                "method": "*",
                "endpoint": "/log/app",
                "handle": "log_app",
                "timeout": 0,
                "log_file": "app.log",
            }
        }
    }
}

logger_msg = {
    "app_start": "Book Search server START...",
    "app_stop": "Book Search server STOP...",
    "invalid_request": "[{uid}] Got invalid search request",
    "invalid_email": "[{uid}] Got invalid search request - e-mail ({e_mail}) is not valid",
    "valid_request": "[{uid}] Got valid search request to find: '{term}' and send results to e-mail: {e_mail}",
    "search_started": "[{uid}] Search results preparation started at: {time}",
    "search_finished": "[{uid}] Full search results preparation finished at: {time} and took: {delta}",
}

message = """
Hi dear customer!
You have submitted search request for term:
{request}

Here are your results:
{result}
"""
sub_message = """
        In book: {book_name}
        In part: {part_name}
        In chapter: {chapter_name}
        In paragraph #: {paragraph_num}
        Text:
        {paragraph_text}
        """
