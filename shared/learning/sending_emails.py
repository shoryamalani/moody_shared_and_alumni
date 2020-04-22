import json
import smtplib
from email.mime.text import MIMEtext


mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
with open("emailcreds.json","r") as f:
    creds =json.load(f)
    
mail.login(creds["email"],creds["passwords"])

msg = MIMEText(to_send)
sender = 'shoryamal@gmail.com'
recipients = ['shoryamal@gmail.com','smalani@gmail.com','sarika.malani@gmail.com']
msg['Subject'] = "soccer game"
msg['From'] = sender
msg['To'] = ", ".join(recipients)

# mail.sendmail(sender,recipients,message.encode('utf-8'))
result = mail.sendmail(sender,recipients,msg.as_string())
mail.quit()
print(result)
