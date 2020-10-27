from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

password = "Mie0xeeN15"
username = "1mmuhammadjanov@ps.kz"
smtphost = "mail.ps.kz"

server = smtplib.SMTP(smtphost)

server.starttls()


a = server.login(username, password)
print(a)

server.quit()
