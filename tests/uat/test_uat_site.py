from selenium import webdriver
import pytest
from conf_user import conf_uat

@pytest.fixture(params=conf_uat)
def browser(request):
    """This fixture prepares browser."""
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(request.param["url"])

    def final():
        """Closes web browser as tests are done."""

        driver.close()
        return

    request.addfinalizer(final)

    return {"driver": driver,
            "param": request.param}


def test_0001_uat_site_title(browser):
    assert browser["param"]["title_ER"] in browser["driver"].title


def test_0002_uat_site_page_name(browser):
    assert browser["param"]["page_name_ER"] == \
           browser["driver"].find_element_by_id("page-name").text


def test_0003_uat_site_form_search_phrase(browser):
    if browser["param"]["url"] == "http://127.0.0.1:5000/":
        assert browser["param"]["serch_help_text_ER"] == \
            browser["driver"].find_element_by_id("serch-help").text
    else:
        pass

pytest.main("-v --html=test_report_uat_site.html")