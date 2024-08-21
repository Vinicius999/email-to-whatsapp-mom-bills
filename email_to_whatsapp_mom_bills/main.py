import os
import re
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from PyPDF2 import PdfReader, PdfWriter
import pywhatkit as kit


load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
PDF_PASSWORD = os.getenv('PDF_PASSWORD')
MOTHER_PHONE_NUMBER = os.getenv('MOTHER_PHONE_NUMBER')


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


def extract_bar_code(pdf_file_path) -> str:
    with open(pdf_file_path, 'rb') as file:
        pdf = PdfReader(file)
        num_pages = len(pdf.pages)

        # Extraindo texto de todas as páginas do PDF
        extracted_text = ''
        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            extracted_text += page.extract_text()

    # Padrão para encontrar a linha digitável (exemplo básico para 47 dígitos)
    pattern = r'\b\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d{1}\s\d{14}\b'

    # Procurando a linha digitável no texto extraído
    match = re.search(pattern, extracted_text)
    if match:
        digitable_bar_code = match.group(0)
        return digitable_bar_code
        # print(f"Linha Digitável encontrada: {bar_code}")
    return




if __name__ == '__main__':
    # get_invoive()
    # print('Invoice saved from email!')
    # unlock_pdf()
    # print('PDF decrypted!')
    path = 'email_to_whatsapp_mom_bills/refined_data/invoice.pdf'
    digitable_bar_code = extract_bar_code(path)

    if extract_bar_code(path):
        print(f'Linha Digitável encontrada: {digitable_bar_code}')

        kit.sendwhatmsg(
            phone_no=MOTHER_PHONE_NUMBER,
            message=f'Linha digitável do boleto: \n{digitable_bar_code}',
            time_hour=10,
            time_min=13,
            wait_time=20,
            tab_close=True
        )
        
    else:
        print(f'Linha Digitável não encontrada.')
        
        
        
        




