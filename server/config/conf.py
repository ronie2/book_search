cfg = {
    "service": {
        "home": {
            "host": "127.0.0.1",
            "port": ":5000",
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
    }
}

db_path = "/home/kali/PycharmProjects/book_search/server/db/anna_karenina.txt"

message = """
Hi dear customer!
You have submitted search request for term:
{request}

Here are your results:
{result}
"""