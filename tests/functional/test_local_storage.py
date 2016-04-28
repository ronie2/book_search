import pytest
from conf import conf_db

# conf_db = {
#     "path": "/home/kali/PycharmProjects/book_search/db/anna_karenina.txt",
#     "text_ER": "Anna Karenina"
# }


def test_0001_db_is_readable():
    import _io
    f = open(conf_db["path"], "r")
    assert _io.TextIOWrapper == type(f)


def test_0002_db_is_anna_karenina():
    anna = False
    with open(conf_db["path"], "r") as f:
        for line in f:
            if conf_db["text_ER"] in line:
                anna = True
                break
    assert True == anna

pytest.main("-v --html=test_report_local_storage.html")