from config.conf import cfg
from config.conf import message
import smtplib
from email.mime.text import MIMEText

def send_email(results, receiver, request):
    msg = MIMEText(message.format(request=request, result=results))
    msg["Subject"] = "Book Search Service Results"
    msg["From"] = cfg["service"]["email"]["login"]
    msg["To"] = receiver

    server_ssl = smtplib.SMTP_SSL(cfg["service"]["email"]["smtp_host"],
                                  cfg["service"]["email"]["smtp_port"])
    server_ssl.ehlo()

    server_ssl.login(cfg["service"]["email"]["login"],
                     cfg["service"]["email"]["password"])

    return server_ssl.send_message(msg)
