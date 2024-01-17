from django.core.mail import EmailMessage
from mailjet_rest import Client
from django.conf import settings


def mail_send(email_to, subject, message):
    try:
        email = EmailMessage()
        email.subject = subject
        email.body = message
        email.from_email = 'rtttestemail@gmail.com'
        email.to = [email_to, ]
        email.content_subtype = 'html'
        email.send()
        # logger.info("Email send")
        return True
    except Exception as e:
        print(e) # todo: add logger
        # logger.error("Error: ", e)
        return False


def send_mail_via_mailjet(email_to, subject, text_part_message=None, html_part_message=None):
    try:
        api_key = settings.MAILJET_API_KEY
        api_secret = settings.MAILJET_API_SECRET
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": settings.MAILJET_FROM_EMAIL,
                        "Name": settings.MAILJET_FROM_EMAIL_NAME
                    },
                    "To": [
                        {
                            "Email": email_to
                        }
                    ],
                    "Subject": subject,
                    "TextPart": text_part_message,
                    "HTMLPart": html_part_message
                }
            ]
        }
        result = mailjet.send.create(data=data)
        # result.status_code)
        # print(result.json())
        return True
    except Exception as e:
        print(e)
        return False


def send_mail_via_mailjet_template(email_to, template_id, subject=None, variables_dict=None):
    send_email_list = []
    if isinstance(email_to, str):
        send_email_list = [{
            "Email": email_to
        }]
    else:
        for email in email_to:
            send_email_list.append({
                "Email": email
            })
    if variables_dict is None:
        variables_dict = {}
    try:
        api_key = settings.MAILJET_API_KEY
        api_secret = settings.MAILJET_API_SECRET
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "To": send_email_list,
                    "Variables": variables_dict,
                    "TemplateID": template_id,
                    "TemplateLanguage": True,
                    "Subject": subject
                }
            ]
        }
        result = mailjet.send.create(data=data)
        # print(result.status_code)
        # print(result.json())
        return True
    except Exception as e:
        print(e)
        return False
