mongo_cfg = {
    "db_name": "book_search",
    "db_host": None,
    "db_port": None
}
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
        "book_parser": {
            "config": {
                "method": "*",
                "endpoint": "/book_parser",
                "handle": "book_parser_handle",
                "timeout": 0,
                "log_file": "book_parser.log",
                "jinja2": {
                    "title": "Welcome to Book Parser!",
                    "legend": "Book Search Parsing Service"
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
    "invalid_max_time": "[{uid}] Error in parsing time: {e}",
    "no_time_limit": "[{uid}] Searching without time limit",
    "valid_request": "[{uid}] Got valid search request to find: '{term}' and send results to e-mail: {e_mail}",
    "search_started": "[{uid}] Search results preparation started at: {time} with limit of: '{time_limit}' seconds",
    "search_finished": "[{uid}] Full search results preparation finished at: {time} and took: {delta}",
    "parser_got_job": "[{uid}] Received job to process file: '{filename}' and title: '{title}'",
    "parser_validator_pass": "[{uid}] Job passed validator",
    "parser_save_file": "[{uid}] File '{filename}' saved to folder '{foldername}'",
    "parser_folder_created": "[{uid}] Folder created: {foldername}",
    "parser_mongo_start": "[{uid}] Started parsing *.txt file and submitting to mongodb",
    "parser_mongo_finish": "[{uid}] Finished parsing. Record created in 'roots' collections: {root_id}",
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
