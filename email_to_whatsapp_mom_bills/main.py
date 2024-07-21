import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from PyPDF2 import PdfReader, PdfWriter


load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
PDF_PASSWORD = os.getenv('PDF_PASSWORD')


def get_invoive() -> None:
    mailbox = MailBox('imap.gmail.com').login(EMAIL_USER, EMAIL_PASSWORD)

    for email in mailbox.fetch(AND(from_='faturabradescard@infobradesco.com.br', seen=False)):
        if len(email.attachments) > 0:
            for attachment in email.attachments:
                if 'FATURA MENSAL' in attachment.filename:
                    attachment_info = attachment.payload
                    with open('email_to_whatsapp_mom_bills/raw_data/encrypted_invoice.pdf', 'wb') as file:
                        file.write(attachment_info)


def unlock_pdf() -> None:
    encrypted_pdf = PdfReader('email_to_whatsapp_mom_bills/raw_data/encrypted_invoice.pdf')
    writer = PdfWriter()

    if encrypted_pdf.is_encrypted:
        encrypted_pdf.decrypt(PDF_PASSWORD)

    for page in encrypted_pdf.pages:
        writer.add_page(page)

    with open('email_to_whatsapp_mom_bills/refined_data/invoice.pdf', 'wb') as file:
        writer.write(file)




if __name__ == '__main__':
    get_invoive()
    print('Invoice saved from email!')
    unlock_pdf()
    print('PDF decrypted!')
