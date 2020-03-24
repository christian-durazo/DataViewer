from flask_mail import Mail, Message
from app import app

mail = Mail(app)

MAIL_SERVER = 'mail.christiandurazo.com'  # smtp server
MAIL_PORT = 587  # smtp port
MAIL_USE_TLS = True

file = open("app/mailconfig.txt")  # file with username and password newline delineated
MAIL_USERNAME = file.readline()
MAIL_PASSWORD = file.readline()
file.close()


def send_email(name, to_email, from_email, subject, message):
	# Create message container
	msg = Message("Notification: New contact from christiandurazo.com", sender=from_email, recipients=to_email)
	msg.subject = subject
	msg.body = message
	try:
		mail.send(msg)
		print("Successfully sent email")
	except Exception as e:
		print(str(e))
		print("Error: unable to send email")
