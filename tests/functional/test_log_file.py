import pytest

from conf import conf_log

# conf_log = {
#     "path": "/home/kali/PycharmProjects/book_search/server/log.log",
#     "text_ER": ["BEGIN AT:", "END AT:", "\n"]
# }


def test_0001_log_is_readable():
    with open(conf_log["path"], "r") as f:
        for line in f:
            assert conf_log["text_ER"][0] in line or \
                   conf_log["text_ER"][1] in line or \
                   conf_log["text_ER"][2] in line

pytest.main("-v --html=test_report_log_file.html")