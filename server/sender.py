from config.conf import cfg
from config.conf import message
from email.mime.text import MIMEText
import smtplib

def send_email(results, receiver, request):
    msg = MIMEText(message.format(request=request, result=str(results)))

    msg["Subject"] = "Book Search Service Results"
    msg["From"] = cfg["service"]["email"]["login"]
    msg["To"] = receiver

    # Three operations in this order
    server_ssl = smtplib.SMTP_SSL(cfg["service"]["email"]["smtp_host"],
                                  cfg["service"]["email"]["smtp_port"])
    server_ssl.ehlo()
    server_ssl.login(cfg["service"]["email"]["login"],
                     cfg["service"]["email"]["password"])

    return server_ssl.send_message(msg)
