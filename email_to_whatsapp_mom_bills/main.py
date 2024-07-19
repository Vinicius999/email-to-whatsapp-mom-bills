import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND


load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# my_email = MailBox('imap.gmail.com').login(EMAIL_USER, EMAIL_PASSWORD)
# print()

# Get date, subject and body len of all emails from INBOX folder
with MailBox('imap.gmail.com').login(EMAIL_USER, EMAIL_PASSWORD) as mailbox:
    for msg in mailbox.fetch():
        print(msg.date, msg.subject, len(msg.text or msg.html))