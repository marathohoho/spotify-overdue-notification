import smtplib, ssl
import textVariables

names = {
	# NAMES OF YOUR USERS - optional
}

def send_email_notification(user, email, amount_overdue_or_credited) :
	port = 587  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "YOUR EMAIL CONNECTED WITH ALL THE AUTOMATION STUFF"
	cc = "CC EMAIL, USUALLY MY SECOND EMAIL - optional"
	receiver_email = [email] + [cc]
	password = "YOUR PASSWORD"

	if amount_overdue_or_credited <= 0 :
		message = textVariables.overduePayment.format(name = names[user], amount = -1 * amount_overdue_or_credited)
	elif amount_overdue_or_credited > 0 :
		message = textVariables.moneyCreditedOnAccount.format(name = names[user], amount = amount_overdue_or_credited)

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		server.ehlo()  # Can be omitted
		server.starttls(context=context)
		server.ehlo()  # Can be omitted
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.encode('utf-8').strip())
	print("Sent notification to a user")
	return


def send_telegram_notification():
	return
