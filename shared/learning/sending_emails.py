import json
import smtplib
from email.mime.text import MIMEText

mail = smtplib.SMTP("smtp.gmail.com",587)
mail.ehlo()
mail.starttls()
with open("creds.json","r") as f:
	creds = json.load(f)
mail.login(creds["email"],creds["pass"])
message = "What would you like to say: "
msg = MIMEText(message)
sender = creds["email"]
recipients = [creds["email"]]
msg["Subject"] = "testing smtplib"
msg["From"] = sender
msg["To"] = ", ".join(recipients)

result = mail.sendmail(sender,recipients,msg.as_string())
mail.quit()
print(result)

