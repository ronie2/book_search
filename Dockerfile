FROM ubuntu
MAINTAINER roman.nzn@gmail.com

RUN apt-get update && apt-get install -yq apt-utils
RUN apt-get install -yq redis-server
RUN mkdir -p /data/db
RUN apt-get install -yq mongodb
RUN apt-get install -yq python3
RUN apt-get install -yq python3-pip
RUN apt-get install -yq git
RUN apt-get clean

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN git clone https://github.com/ronie2/book_search.git
RUN pip3 install -r /book_search/requirements.txt

CMD redis-server & mongod & cd /book_search/server && python3 /book_search/server/mongo_parser.py && /usr/local/bin/rq worker & python3 /book_search/server/server.py
