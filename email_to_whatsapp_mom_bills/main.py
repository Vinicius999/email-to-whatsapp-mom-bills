import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND


load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def get_invoive() -> None:
    mailbox = MailBox('imap.gmail.com').login(EMAIL_USER, EMAIL_PASSWORD)

    for email in mailbox.fetch(AND(from_='faturabradescard@infobradesco.com.br', seen=False)):
        if len(email.attachments) > 0:
            for attachment in email.attachments:
                if 'FATURA MENSAL' in attachment.filename:
                    attachment_info = attachment.payload
                    print('Writting the pdf file...')
                    with open('email_to_whatsapp_mom_bills/media/blocked_invoice.pdf', 'wb') as file:
                        file.write(attachment_info)


if __name__ == '__main__':
    get_invoive()
    print('Done!')
    