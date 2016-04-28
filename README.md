# This is book_search app!
1. You can seach Leo Tolstoys "Anna Karenina" book (english edition) and get search results to your e-mail in following format:
```
Hi dear customer!
You have submitted search request for term:
Anna

Here are your results:
In line #: 2 -> ﻿      The Project Gutenberg EBook of Anna Karenina, by Leo Tolstoy
In line #: 12 -> Title: Anna Karenina
In line #: 37 ->                              Anna Karenina
In line #: 232 -> "Matvey, my sister Anna Arkadyevna will be here tomorrow," he said,
...
...
...
```
2. App writes ```log.log``` file with time spend for search
3. App implements SOME Functional and User Acceptance tests
4. App uses e-mail message queue
5. App uses gmail.com SMTP server


## 0. Observer docs:
[Basic app diagram](https://github.com/ronie2/book_search/blob/master/testing_docs/scheme.pdf) 
[Risk analyze plan](https://github.com/ronie2/book_search/blob/master/testing_docs/risks.pdf)

## A. Configure SERVER and DB:

1. Install Redis 
2. Install Python 3.5
3. Clone git repo: ```$ git clone https://github.com/ronie2/book_search.git```
4. Change dir: ```$ cd book_search/```
5. Install requirements: ```$ pip install -r requirements.txt``` or ```$ pip3 install -r requirements.txt``` (depending on your env)
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

## C. Configure Functional test (specify IP ADRESS (```"url"```) and full PATH TO ANNA KARENINA DB (```"path"```)):
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

## F. Observe test reports and try service:
1. Test reports are located in ```tests``` folder
2. Service is available on specified server url (```http://172.17.0.4:5000/``` in this example)