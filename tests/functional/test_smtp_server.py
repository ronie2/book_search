import pytest
from conf import conf_smtp

def test_0001_smtp_reachable():
    import smtplib
    server_ssl = smtplib.SMTP_SSL(conf_smtp["smtp_host"],
                                  conf_smtp["smtp_port"])
    assert smtplib.SMTP_SSL == type(server_ssl)


def test_0002_smtp_login():
    import smtplib

    server_ssl = smtplib.SMTP_SSL(conf_smtp["smtp_host"],
                                  conf_smtp["smtp_port"])
    server_ssl.ehlo()
    assert "235" in str(server_ssl.login(conf_smtp["login"],
                                         conf_smtp["password"]))


pytest.main("-v --html=test_report_smtp_server.html")
