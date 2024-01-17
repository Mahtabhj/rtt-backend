import datetime

from rttcore.services.email_service import send_mail_via_mailjet_template
from rttnotification.models import NotificationAlert, NotificationAlertLog
from rttnotification.servives.notification_service import NotificationService
from django.conf import settings
from rtt import celery_app

CELERY_DEFAULT_QUEUE = settings.CELERY_DEFAULT_QUEUE


@celery_app.task(bind=False, queue=CELERY_DEFAULT_QUEUE)
def daily_email_notification_task():
    today = datetime.date.today()
    one_day_ago = today - datetime.timedelta(days=1)

    notification_list = NotificationAlert.objects.filter(active=True, frequency='daily')
    notification_serialized_list = []
    for notification in notification_list:
        try:
            send_email_notification.delay(notification.id, one_day_ago, one_day_ago)
            notification_serialized_list.append({
                'notification_id': notification.id,
                'user_id': notification.user_id
            })
        except:
            pass
    return {
        'total_notification': notification_list.count(),
        'notifications': notification_serialized_list
    }


@celery_app.task(bind=False, queue=CELERY_DEFAULT_QUEUE)
def weekly_email_notification_task():
    today = datetime.date.today()
    one_day_ago = today - datetime.timedelta(days=1)
    week_ago = today - datetime.timedelta(days=7)

    notification_list = NotificationAlert.objects.filter(active=True, frequency='weekly')
    notification_serialized_list = []
    for notification in notification_list:
        try:
            send_email_notification.delay(notification.id, week_ago, one_day_ago)
            notification_serialized_list.append({
                'notification_id': notification.id,
                'user_id': notification.user_id
            })
        except:
            pass
    return {
        'total_notification': notification_list.count(),
        'notifications': notification_serialized_list
    }


@celery_app.task(bind=False, queue=CELERY_DEFAULT_QUEUE)
def monthly_email_notification_task():
    today = datetime.date.today()
    one_day_ago = today - datetime.timedelta(days=1)
    month_ago = today - datetime.timedelta(days=30)

    notification_list = NotificationAlert.objects.filter(active=True, frequency='monthly')
    notification_serialized_list = []
    for notification in notification_list:
        try:
            send_email_notification.delay(notification.id, month_ago, one_day_ago)
            notification_serialized_list.append({
                'notification_id': notification.id,
                'user_id': notification.user_id
            })
        except:
            pass
    return {
        'total_notification': notification_list.count(),
        'notifications': notification_serialized_list
    }


@celery_app.task(queue=CELERY_DEFAULT_QUEUE)
def send_email_notification(notification_id, from_date, to_date):
    notification_obj: NotificationAlert = NotificationAlert.objects.get(id=notification_id)
    if not notification_obj.user.is_active:
        return
    notification_service = NotificationService()
    user = notification_obj.user
    email_frequency_info = ''

    material_category_ids = list(notification_obj.material_categories.all().values_list('id', flat=True))
    product_category_ids = list(notification_obj.product_categories.all().values_list('id', flat=True))
    topic_ids = list(notification_obj.topics.all().values_list('id', flat=True))
    region_ids = list(notification_obj.regions.all().values_list('id', flat=True))
    regulatory_framework_ids = list(notification_obj.regulatory_frameworks.all().values_list('id', flat=True))

    filters = {
        'topics': topic_ids,
        'regions': region_ids,
        'product_categories': product_category_ids,
        'material_categories': material_category_ids,
        'related_frameworks': regulatory_framework_ids,
        'from_date': from_date,
        'to_date': to_date,
    }

    # notification_log = NotificationAlertLog.objects.create(notification_alert_id=notification_id,
    #                                                        user_id=user.id,
    #                                                        status='in-progress',
    #                                                        filter_criteria=filters)

    notification_list = []
    template_id = None
    send_email = False
    message = ''

    if notification_obj.content.lower() == 'news':
        notification_list = notification_service.get_news_notification_list(filters, user.organization_id)
        template_id = settings.MAILJET_NEWS_EMAIL_NOTIFICATION_TEMPLATE_ID

    elif notification_obj.content.lower() == 'regulatory_updates':
        notification_list = notification_service.get_regulatory_updates_notification_list(filters, user.organization_id)
        template_id = settings.MAILJET_REGULATORY_UPDATES_EMAIL_NOTIFICATION_TEMPLATE_ID

    elif notification_obj.content.lower() == 'assessments':
        notification_list = notification_service.get_assessments_notification_list(filters, user.organization_id)
        template_id = settings.MAILJET_ASSESSMENTS_EMAIL_NOTIFICATION_TEMPLATE_ID

    elif notification_obj.content.lower() == 'limits':
        notification_list = notification_service.get_limit_notification_list(filters, user.organization_id)
        template_id = settings.MAILJET_LIMIT_EMAIL_NOTIFICATION_TEMPLATE_ID
        email_frequency_info = f"Changes to {notification_obj.content} data for framework/regulation, relevant to " \
                               f"your organization in the time period: {str(from_date[:10])} to " \
                               f"{str(datetime.date.today())}"

    elif notification_obj.content.lower() == 'substances':
        notification_list = notification_service.get_substance_notification_list(
            filters, user.organization_id)
        template_id = settings.MAILJET_SUBSTANCE_REGULATION_EMAIL_NOTIFICATION_TEMPLATE_ID
        email_frequency_info = f"{notification_obj.content.capitalize()} update in the time period: " \
                               f"{str(from_date[:10])} to {str(datetime.date.today())}"
    '''
    check notification_list and Send email
    '''
    if notification_list and template_id:
        variables_dict = {
            "username": user.username,
            "alert_name": notification_obj.name,
            "notification_list": notification_list,
            "email_frequency_info": email_frequency_info,
        }
        send_email = send_mail_via_mailjet_template(user.email, template_id, variables_dict=variables_dict)
    else:
        message = 'No notification data found!'

    print(send_email)

    return {
        'send_email': send_email,
        'notification_list': len(notification_list),
        'message': message,
    }
