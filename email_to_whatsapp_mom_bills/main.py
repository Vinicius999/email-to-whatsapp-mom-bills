import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND


load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Get date and subject of all emails from INBOX folder
with MailBox('imap.gmail.com').login(EMAIL_USER, EMAIL_PASSWORD) as mailbox:
    for msg in mailbox.fetch(AND(from_='faturabradescard@infobradesco.com.br', seen=False)):
        print(msg.date.strftime('%Y-%m-%d %H:%M'), msg.subject)
        
        