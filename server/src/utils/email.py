#from __main__ import mail_server
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email_address, subject, body):
	message = MIMEMultipart()
	message['From'] = EMAIL_ADDRESS
	message['To'] = to_email_address
	message['Subject'] = subject
	message.attach(MIMEText(body, 'plain'))
	mail_server.send_message(message)
