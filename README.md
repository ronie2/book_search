# This is book_search app!

App address:
```
http://[IP]:[PORT]/
```
App endpoints:
```
'/' - Main search page
'/result' - Page with search results
'/book_parser' - New books parsing page
'/log/app' - Main application log
```

1. You can search books via web page ```http://[IP]:[PORT]/``` and get search results to your e-mail in following format:
```
Hi dear customer!
You have submitted search request for term:
SumMer

Here are your results:

        In book: Anna Karenina
        In part: SIX
        In chapter: 25
        In paragraph #: 1
        Text:
        Vronsky and Anna spent the whole summer and part of the winter in the country, living in just the
        same condition, and still taking no steps to obtain a divorce. It was an understood thing between
        them that they should not go away anywhere; but both felt, the longer they lived alone, especially
        in the autumn, without guests in the house, that they could not stand this existence, and that they
        would have to alter it.

        ...

        In book: Dracula
        In part: ONE
        In chapter: XIX
        In paragraph #: 21
        Text:
        With their going it seemed as if some evil presence had departed, for the dogs frisked about and barked
        merrily as they made sudden darts at their prostrate foes, and turned them over and over and tossed them
        in the air with vicious shakes. We all seemed to find our spirits rise. Whether it was the purifying of the
        deadly atmosphere by the opening of the chapel door, or the relief which we experienced by finding ourselves
        in the open I know not; but most certainly the shadow of dread seemed to slip from us like a robe, and the
        occasion of our coming lost something of its grim significance, though we did not slacken a whit in our
        resolution. We closed the outer door and barred and locked it, and bringing the dogs with us, began our
        search of the house. We found nothing throughout except dust in extraordinary proportions, and all untouched
        save for my own footsteps when I had made my first visit. Never once did the dogs exhibit any symptom of
        uneasiness, and even when we returned to the chapel they frisked about as though they had been rabbit-hunting
        in a summer wood
...
...
...
```
2. App uses mongodb for storing and searching texts. [Text index](https://docs.mongodb.com/manual/core/index-text/) is used.
3. You can set maximum search time limit in this format ```1.500001```. App will search for about 1.5 sec than stop search and send result to e-mail.
4. App is deployed with some books located in following folder: ```book_search/server/db/basic_data```
5. User can add additional books using web interface: ```http://[IP]:[PORT]/book_parser```. Requirements to files are following:
```
encoding: utf-8
book protocol:

[some_text]
'PART' NAME_1
'CHAPTER' or 'Chapter' NAME_1
[some_text]
...
'PART' NAME_N
'CHAPTER' or 'Chapter' NAME_N
[some_text]
```
6. App writes ```book_search/server/app.log``` file with time spend for search and other info. Web interface: ```http://[IP]:[PORT]/app/log```
7. App implements SOME Functional and User Acceptance tests
8. App uses e-mail message queue
9. App uses gmail.com SMTP server

## 0. Observe docs:
[Basic app diagram](https://github.com/ronie2/book_search/blob/master/testing_docs/scheme.pdf)
 
[Risk analyze plan](https://github.com/ronie2/book_search/blob/master/testing_docs/risks.pdf)

[Database diagram](https://github.com/ronie2/book_search/blob/master/testing_docs/book_search_mongodb.pdf)

## Install
### Using docker
0. The easiest way to install using docker is to download [setup script](https://github.com/ronie2/book_search/blob/master/setup.sh) and run it ```source setup.sh```
or use these commands:
1. Clone git repo: ```$ git clone https://github.com/ronie2/book_search.git```
2. Build docker container: ```$ sudo docker build -t ronie2/book_search book_search/```
3. Run container: ```$ sudo docker run -t -i --rm ronie2/book_search```

When server start you will see it's IP and port. Say: ```======== Running on http://172.17.0.16:5001/ ========```

### Manual installation
#### A. Configure SERVER and DB:

1. Install Redis
2. Install MongoDB
3. Install Python 3.5
4. Clone git repo: ```$ git clone https://github.com/ronie2/book_search.git```
5. Change dir: ```$ cd book_search/```
6. Install requirements: ```$ pip install -r requirements.txt``` or ```$ pip3 install -r requirements.txt``` (depending on your env)
7. You can configure server (but this is not really necessary):
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
```

#### D. Start server:
1. Change working directory: ```$ cd book_search/server```
2. Pre populate server MongoDB with default data ```python3 book_search/server/mongo_parser.py```
3. Start RQ and Server: ```$ rq worker & python server.py```

# Tests are not adapted to MongoDB version jet!
---
#### B. Configure UAT test:
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

#### C. Configure Functional test (specify IP ADRESS (```"url"```) and full PATH TO ANNA KARENINA DB (```"path"```)):
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
#### E. Start tests (Firefox web browser SHOULD be installed to perform UAT test):
1. Change working directory: ```$ cd /book_search/tests```
2. Run pytest: ```$ py.test```

#### F. Observe test reports and try service:
1. Test reports are located in ```tests``` folder
2. Service is available on specified server url (```http://172.17.0.4:5000/``` in this example)