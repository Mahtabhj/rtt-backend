import logging
from django.contrib.auth import get_user_model
from django.conf import settings

from rttcore.services.email_service import send_mail_via_mailjet_template
from rttdocumentManagement.services.doc_management_collaborator_services import DocManagementCollaboratorService
from rttdocumentManagement.services.email_notification_services import EmailNotificationServices

from rtt import celery_app

logger = logging.getLogger(__name__)
User = get_user_model()
CELERY_DEFAULT_QUEUE = settings.CELERY_DEFAULT_QUEUE


@celery_app.task(queue=CELERY_DEFAULT_QUEUE)
def doc_management_update_email_notification(old_data, new_data, editor_id, change_in_attachment_document=False):
    doc_management_id = old_data.get('id', None)
    email_to = DocManagementCollaboratorService().get_doc_management_email_notification_receiver(doc_management_id,
                                                                                                editor_id)
    if len(email_to) == 0:
        return
    subject = f'Document Management updated notification'
    base_url = settings.SITE_BASE_URL
    variables_dict = {
        'has_name_diff': False, # flag for check name diff
        'has_description_diff': False, # flag for check description diff
        'has_regulatory_frameworks_diff': False, # flag for check regulatory_frameworks diff
        'has_regulations_diff': False, # flag for check regulations diff
        'has_products_diff': False, # flag for check products diff
        'has_substances_diff': False, # flag for check substances diff
        'has_news_diff': False, # flag for check news diff
        'has_attachment_document_diff': False, # flag for check attachment_document
        'doc_link': f"{base_url}documents/document/{doc_management_id}",
    }
    email_notification_services = EmailNotificationServices()

    # doc_management name filed process
    old_name, new_name = old_data.get('name', ''), new_data.get('name', '')
    has_name_diff, name = email_notification_services.name_field_process(old_name, new_name)
    if has_name_diff:
        variables_dict['has_name_diff'] = True
        variables_dict['name'] = name

    # doc_management description field process
    old_description, new_description = old_data.get('description', ''), new_data.get('description', '')
    has_description_diff, description = email_notification_services.description_field_process(old_description,
                                                                                              new_description)
    if has_description_diff:
        variables_dict['has_description_diff'] = True
        variables_dict['description'] = description

    # doc_management regulatory_frameworks field process
    old_frameworks, new_frameworks = old_data.get('regulatory_frameworks', []), new_data.get('regulatory_frameworks', [])
    has_regulatory_frameworks_diff, regulatory_frameworks = email_notification_services.\
        regulatory_frameworks_field_process(old_frameworks, new_frameworks)

    if has_regulatory_frameworks_diff:
        variables_dict['has_regulatory_frameworks_diff'] = True
        variables_dict['regulatory_frameworks'] = regulatory_frameworks

    # doc_management regulations field process
    old_regulations, new_regulations = old_data.get('regulations', []), new_data.get('regulations', [])
    has_regulations_diff, regulations = email_notification_services.regulations_field_process(old_regulations,
                                                                                              new_regulations)

    if has_regulations_diff:
        variables_dict['has_regulations_diff'] = True
        variables_dict['regulations'] = regulations

    # doc_management products field process
    old_products, new_products = old_data.get('products', []), new_data.get('products', [])
    has_products_diff, products = email_notification_services.products_field_process(old_products, new_products)

    if has_products_diff:
        variables_dict['has_products_diff'] = True
        variables_dict['products'] = products

    # doc_management substances field process
    old_substances, new_substances = old_data.get('substances', []), new_data.get('substances', [])
    has_substances_diff, substances = email_notification_services.substances_field_process(old_substances, new_substances)

    if has_substances_diff:
        variables_dict['has_substances_diff'] = True
        variables_dict['substances'] = substances

    # doc_management news field process
    old_news, new_news = old_data.get('news', []), new_data.get('news', [])
    has_news_diff, news = email_notification_services.news_field_process(old_news, new_news)

    if has_news_diff:
        variables_dict['has_news_diff'] = True
        variables_dict['news'] = news

    # doc_management attachment_document field process
    if change_in_attachment_document:
        variables_dict['has_attachment_document_diff'] = True
        user_obj = User.objects.filter(id=editor_id).first()
        variables_dict['attachment_document'] = f"The Attachment Document is changed by {user_obj.username}"

    # email will be sent when at least one filed has changes
    if variables_dict['has_name_diff'] or variables_dict['has_description_diff'] or variables_dict[
        'has_regulatory_frameworks_diff'] or variables_dict['has_regulations_diff'] or variables_dict[
        'has_products_diff'] or variables_dict['has_substances_diff'] or variables_dict[
        'has_news_diff'] or variables_dict['has_attachment_document_diff']:

        template_id = settings.MAILJET_DOC_MANAGEMENT_NOTIFICATION_TEMPLATE_ID
        send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)


@celery_app.task(queue=CELERY_DEFAULT_QUEUE)
def doc_management_comment_email_notification(doc_management, editor_id, old_doc_comment=None, new_doc_comment=None):
    email_to = DocManagementCollaboratorService().get_doc_management_email_notification_receiver(doc_management['id'],
                                                                                                 editor_id)
    if len(email_to) == 0:
        return

    base_url = settings.SITE_BASE_URL
    variables_dict = {
        'has_doc_comment_diff': False, # flag for add_or_edit comment
        'doc_link': f"{base_url}documents/document/{doc_management['id']}",
    }
    if not old_doc_comment:
        variables_dict['has_doc_comment_diff'] = True
        variables_dict['doc_comment'] = new_doc_comment
        subject = f'New comment added notification for document'
        variables_dict['action'] = f"New comment added on {doc_management['name']}"
    else:
        subject = f'Comment updated notification for document'
        variables_dict['action'] = f"Comment updated on {doc_management['name']}"
        email_notification_services = EmailNotificationServices()
        # doc_management doc_comment field process
        has_doc_comment_diff, doc_comment = email_notification_services.doc_comment_add_process(old_doc_comment,
                                                                                                new_doc_comment)
        if has_doc_comment_diff:
            variables_dict['has_doc_comment_diff'] = True
            variables_dict['doc_comment'] = doc_comment
        else:
            return
    if variables_dict['has_doc_comment_diff']:
        template_id = settings.MAILJET_DOC_COMMENT_NOTIFICATION_TEMPLATE_ID
        send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)
