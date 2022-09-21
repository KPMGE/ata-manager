import smtplib
import email.message
from dotenv import load_dotenv
import os

load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")

def get_body(student_name, writer_name, ata_link):
    body = f"""
    <h3>Boa tarde, {student_name}!</h3> 
    <h4>O(a) responsável pela ATA de hoje é {writer_name}!</h4>
    <a href="{ata_link}"><h4>ATA de hoje</h4></a>
    """
    body_ata_writer = f"""
    <h3>Boa tarde, {writer_name}!</h3> 
    <h4>Você é responsável pela ATA de hoje!</h4>
    <a href="{ata_link}"><h4>ATA de hoje</h4></a>
    """
    if student_name == writer_name:
        return body_ata_writer
    return body


def send_email(body, sender, receiver):  
    
    msg = email.message.Message()
    msg['Subject'] = "Ata - Reunião Pet EngComp"
    msg['From'] = sender
    msg['To'] = receiver
    password = APP_PASSWORD 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print(f'Email enviado para {receiver}')


def send_emails(students, writer_name, ata_link, sender):
    for student in students:
        body = get_body(student['name'], writer_name, ata_link)
        send_email(body, sender, student['email'])
