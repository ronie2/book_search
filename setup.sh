#!/bin/bash          
git clone https://github.com/ronie2/book_search.git
sudo docker build -t ronie2/book_search book_search/
sudo docker run -t -i --rm ronie2/book_search