import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django_scaffolding_tools._experimental.cover_letters.config import ConfigurationManager


def send_email(receiver_address, sender_address, password, body, subject, attachments, **kwargs):
    # The mail addresses and password

    # receiver_address = 'lberrocal@pancanal.com'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(body, 'plain'))
    for attachment in attachments:
        attach_file = open(attachment, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        # payload.add_header('Content-Decomposition', 'attachment', filename='invoices_20201101_1120.xlsx')
        fn = os.path.basename(attachment)
        payload.add_header(
            "Content-Disposition",
            f"attachment; filename= {fn}",
        )
        message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, password)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def send_cover_letter(receiver_email, context, attachments):
    config = ConfigurationManager().get_current()
    email = config['gmail']['email']
    token = config['gmail']['token']

    body = f"""Dear Hiring Manager:

    I would like to be considered for the position {context['position_name']} at {context["company_name"]}.

    Enclosed you'll find my cover letter and cv.

    Regards

    Luis
    """
    subject = f'Application for {context["position_name"]}.'
    send_email(receiver_email, email, token, body, subject, attachments)


if __name__ == '__main__':
    attachment_file = '/home/luiscberrocal/PycharmProjects/django_scaffolding_tools' \
                      '/output/20221107_cover_Jedi Order Council_Jedi Knight.pdf'
    to_email = 'laberrocalf@gmail.com'
    context = {'position_name': 'Jedi knight', 'company_name': 'Jedi council'}
    send_cover_letter(to_email, context, [attachment_file])
