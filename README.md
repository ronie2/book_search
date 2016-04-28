## A. Configure SERVER and DB:

1. Install Redis 
2. Install Python 3.5
3. Clone git repo: ```$ git clone https://github.com/ronie2/book_search.git```
4. Change dir: ```$ cd book_search/```
5. Install requirements: ```$ pip install -r requirements.txt``` or $ ```pip3 install -r requirements.txt``` (depending on your env)
6. Configure server (Specify IP ADDRESS, PORT and FULL PATH TO "anna_karenina.txt"):
```
$ vim server/config/conf.py
```
```
cfg = {
    "service": {
        "home": {
            "host": "172.17.0.4",
            "port": ":5000",
        },

...
...
...

db_path = "/book_search/server/db/anna_karenina.txt"
```
7. Change working dir to server: ```$ cd server/```

## B. Configure UAT test:
1. Edit /book_search/tests/uat/conf_user.py (specify ```"url"```):
```
$ vim /book_search/tests/uat/conf_user.py
```
```
conf_uat = [
    {
        "url": "http://172.17.0.4:5000/",
        "title_ER": "Welcome to book search!",
        "page_name_ER": "Book Search Service",
        "serch_help_text_ER": "Fill in search phrase"
    },
    {
        "url": "http://172.17.0.4:5000/result",
        "title_ER": "Thank you! Search started!",
        "page_name_ER": "Roman"
    }
]
```

## C. Configure Functional test (specify IP ADRESS (```"url"```) and full PATH TO DB (```"path"```)):
```
$ vim book_search/tests/functional/conf.py
```
```
conf_server = [
    {"url": "http://172.17.0.4:5000/"},
    {"url": "http://172.17.0.4:5000/result"}
]
conf_db = {
    "path": "/book_search/server/db/anna_karenina.txt",
    "text_ER": "Anna Karenina"
}

conf_log = {
    "path": "/book_search/server/log.log",
    "text_ER": ["BEGIN AT:", "END AT:", "\n"]
}

conf_smtp = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 465,
    "login": "book.search.app.test@gmail.com",
    "password": "book.search.app.test111",
}
```
## D. Start server:
1. Change working directory: ```$ cd /book_search/server```
2. Start RQ and Server: ```$ rq worker & python server.py```

## E. Start tests (Firefox web browser SHOULD be installed to perform UAT test):
1. Change working directory: ```$ cd /book_search/tests```
2. Run pytest: ```$ py.test```