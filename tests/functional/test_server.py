import pytest
from conf import conf_server


# conf_server = [
#     {"url": "http://127.0.0.1:5000/"},
#     {"url": "http://127.0.0.1:5000/result"}
# ]

@pytest.fixture(params=conf_server)
def response(request):
    import requests

    resp = requests.get(request.param["url"])

    return resp


def test_0001_server_200_OK(response):
    assert 200 == response.status_code

def test_0002_server_header(response):
    assert "text/html; charset=utf-8" == \
           response.headers["CONTENT-TYPE"] and \
           "DATE" in response.headers.keys() and \
           "SERVER" in response.headers.keys() and \
           "CONTENT-LENGTH" in response.headers.keys()

def test_0003_server_body_valid_(response):
    import json
    import requests

    head = {"Content-Type": "text/html; charset=utf-8"}
    validator_url = "https://validator.w3.org/nu/?out=json"

    resp = requests.post(validator_url, data=response.text, headers=head)
    validator_json = json.loads(resp.text)

    # Assert that len of error "messages" array is empty => no errors in HTML
    assert 0 == len(validator_json["messages"])

pytest.main("-v --html=test_report_log_file.html")