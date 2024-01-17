import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q

from rttcore.services.email_service import send_mail_via_mailjet_template
from rtttaskManagement.models import TaskEditor, TaskHistory
from rtttaskManagement.services.sequence_matcher_service import SequenceMatcherService

from rtt import celery_app

logger = logging.getLogger(__name__)
User = get_user_model()
CELERY_DEFAULT_QUEUE = settings.CELERY_DEFAULT_QUEUE


@celery_app.task(queue=CELERY_DEFAULT_QUEUE)
def task_management_update_email_notification(old_data, updated_data, editor_id):
    """
    doc: https://chemycal.atlassian.net/browse/RTT-758
    """
    print('task_management_update_email_notification____________START____________')
    try:
        base_url = settings.SITE_BASE_URL
        variables_dict = {
            'task_updated': '',
            'has_title_diff': False,
            'has_assignee_diff': False,
            'has_status_diff': False,
            'has_due_date_diff': False,
            'has_description_diff': False,
            'has_product_diff': False,
            'has_archive_diff': False,
            'view_task_url': f"{base_url}tasks/task/{old_data['id']}",
            'has_new_comment': False,
            'has_substance_diff': False,
        }
        task_history_obj_list = []
        new_title = updated_data.get('name', None)
        old_title = old_data['name']
        subject = f'Task update: {new_title}'
        editor_queryset = User.objects.filter(id=editor_id).first()
        today = timezone.now().date()
        if editor_queryset.first_name:
            name = editor_queryset.first_name
            if editor_queryset.last_name:
                name += ' ' + editor_queryset.last_name
        else:
            name = editor_queryset.username
        variables_dict['task_updated'] = f'{name} made an update ({today})'
        email_to = []
        # 3.e. (Task title) The email should include:
        if new_title != old_title:
            variables_dict['has_title_diff'] = True
            variables_dict['title'] = f'{old_title} → {new_title}'
            # storing tasks logs for name in Task model
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='name', prev_value=old_title, curr_value=new_title))

        # 2 When the Assignee is changed to another user or unassigned
        new_assignee = updated_data.get('assignee', None)
        if new_assignee:
            assignee = User.objects.filter(id=new_assignee['id']).first()
            if assignee.first_name:
                new_assignee_name = assignee.first_name
                if assignee.last_name:
                    new_assignee_name += ' ' + assignee.last_name
            else:
                new_assignee_name = assignee.username
            # we need to send notification to the assignee where assignee is not the current user
            if new_assignee['id'] != editor_id:
                email_to.append(assignee.email)
            if not old_data['assignee']:
                variables_dict['assignee'] = f'Unassigned → {new_assignee_name}'
                variables_dict['has_assignee_diff'] = True
                # storing tasks logs for assignee in Task model
                task_history_obj_list.append(
                    TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='assigned',
                                action_field='assignee', prev_value='Unassigned',
                                curr_value=new_assignee_name))
            if old_data['assignee'] and old_data['assignee']['id'] != new_assignee['id']:
                if old_data['assignee']['first_name']:
                    old_assignee_name = old_data['assignee']['first_name']
                    if old_data['assignee']['last_name']:
                        old_assignee_name += ' ' + old_data['assignee']['last_name']
                else:
                    old_assignee_name = old_data['assignee']['username']
                variables_dict['assignee'] = f'{old_assignee_name} → {new_assignee_name}'
                variables_dict['has_assignee_diff'] = True
                # storing tasks logs for assignee in Task model
                task_history_obj_list.append(
                    TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='assigned',
                                action_field='assignee', prev_value=old_assignee_name,
                                curr_value=new_assignee_name))
                # we need to send notification to the assignee who is unassigned
                if old_data['assignee']['id'] != editor_id:
                    email_to.append(old_data['assignee']['email'])
        if old_data['assignee'] and not new_assignee:
            if old_data['assignee']['first_name']:
                old_assignee_name = old_data['assignee']['first_name']
                if old_data['assignee']['last_name']:
                    old_assignee_name += ' ' + old_data['assignee']['last_name']
            else:
                old_assignee_name = old_data['assignee']['username']
            variables_dict['assignee'] = f'{old_assignee_name} → Unassigned'
            variables_dict['has_assignee_diff'] = True
            # storing tasks logs for assignee in Task model
            task_history_obj_list.append(
                TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='assigned',
                            action_field='assignee', curr_value='Unassigned', prev_value=old_assignee_name))
            # we need to send notification to the assignee who is unassigned
            if old_data['assignee']['id'] != editor_id:
                email_to.append(old_data['assignee']['email'])

        # 3.g. (Status) The email should include:
        new_status = updated_data.get('status', None)
        if old_data['status'] != new_status:
            variables_dict['status'] = f"{old_data['status'].capitalize()} → {new_status.capitalize()}"
            variables_dict['has_status_diff'] = True
            # storing tasks logs for status in Task model
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='status', prev_value=old_data['status'].capitalize(),
                                                     curr_value=new_status.capitalize()))

        # 3.d. (Due date) The email should include:
        new_due_date = updated_data.get('due_date', None)
        old_due_date = old_data.get('due_date', None)
        if new_due_date:
            new_due_date = new_due_date[:10]
            if old_due_date:
                old_due_date = old_data['due_date'][:10]
                if old_due_date != new_due_date:
                    variables_dict['due_date'] = f"{old_due_date} → {new_due_date}"
                    variables_dict['has_due_date_diff'] = True
            else:
                variables_dict['due_date'] = f"Not set → {new_due_date}"
                variables_dict['has_due_date_diff'] = True
        elif old_due_date:
            old_due_date = old_data['due_date'][:10]
            variables_dict['due_date'] = f"{old_due_date} → Not set"
            variables_dict['has_due_date_diff'] = True
        if variables_dict['has_due_date_diff']:
            # storing tasks logs for due_date in Task model
            new_due_date = new_due_date if new_due_date else 'Not set'
            old_due_date = old_due_date if old_due_date else 'Not set'
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='due_date', prev_value=old_due_date,
                                                     curr_value=new_due_date))

        # email notification for Task Archive, Un-archive:
        if old_data.get('is_archive') and not updated_data.get('is_archive'):
            variables_dict['is_archive'] = "The task has been Unarchived!"
            variables_dict['has_archive_diff'] = True
        elif not old_data.get('is_archive') and updated_data.get('is_archive'):
            variables_dict['is_archive'] = "The task has been Archived!"
            variables_dict['has_archive_diff'] = True
        # 3.f. (Description) The email should include:
        old_description = old_data.get('description', None)
        new_description = updated_data.get('description', None)
        has_description, description = SequenceMatcherService().get_highlighted_unified_diff_string(old_description,
                                                                                                    new_description)
        variables_dict['has_description_diff'] = has_description
        variables_dict['description'] = description
        if has_description:
            # storing tasks logs for due_date in Task model
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='description', prev_value=old_description,
                                                     curr_value=new_description))

        # 3.a. (Products) The email should include:
        old_product_list = old_data['products']
        new_product_list = updated_data.get('products', None)
        old_product_id_list = []
        new_product_id_list = []
        for product in new_product_list:
            new_product_id_list.append(product['id'])
        product_list = []
        for product in old_product_list:
            old_product_id_list.append(product['id'])
            if product['id'] not in new_product_id_list:
                product_list.append({
                    'id': product['id'],
                    'name': product['name'],
                    'status': 'removed'
                })
        for product in new_product_list:
            if product['id'] not in old_product_id_list:
                product_list.append({
                    'id': product['id'],
                    'name': product['name'],
                    'status': 'added'
                })
        if product_list:
            variables_dict['products'] = product_list
            variables_dict['has_product_diff'] = True
            # storing tasks logs for products in Task model
            old_product_id_list = ','.join([str(i) for i in old_product_id_list]) if old_product_id_list else ''
            new_product_id_list = ','.join([str(i) for i in new_product_id_list]) if new_product_id_list else ''
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='products', prev_value=old_product_id_list,
                                                     curr_value=new_product_id_list, extra=product_list))

        # Substances
        old_substance_list = old_data['substances']
        new_substance_list = updated_data.get('substances', None)
        old_substance_id_list = []
        new_substance_id_list = []
        for substance in new_substance_list:
            new_substance_id_list.append(substance['id'])
        substance_list = []
        for substance in old_substance_list:
            old_substance_id_list.append(substance['id'])
            if substance['id'] not in new_substance_id_list:
                substance_list.append({
                    'id': substance['id'],
                    'name_ec_no_cas_no': f"Name: {substance['name']}, "
                                         f"EC: {substance['ec_no'] if substance['ec_no'] else ''}, "
                                         f"CAS: {substance['cas_no'] if substance['cas_no'] else ''}",
                    'status': 'removed'
                })
        for substance in new_substance_list:
            if substance['id'] not in old_substance_id_list:
                substance_list.append({
                    'id': substance['id'],
                    'name_ec_no_cas_no': f"Name: {substance['name']}, "
                                         f"EC: {substance['ec_no'] if substance['ec_no'] else ''}, "
                                         f"CAS: {substance['cas_no'] if substance['cas_no'] else ''}",
                    'status': 'added'
                })
        if substance_list:
            variables_dict['substances'] = substance_list
            variables_dict['has_substance_diff'] = True
            # storing tasks logs for substances in Task model
            old_substance_id_list = ','.join([str(i) for i in old_substance_id_list]) if old_substance_id_list else ''
            new_substance_id_list = ','.join([str(i) for i in new_substance_id_list]) if new_substance_id_list else ''
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='substances', prev_value=old_substance_id_list,
                                                     curr_value=new_substance_id_list, extra=substance_list))


        # (regulations):
        old_reg_list = old_data['regulations']
        new_reg_list = updated_data.get('regulations', None)
        old_reg_id_list = []
        new_reg_id_list = []
        for reg in new_reg_list:
            new_reg_id_list.append(reg['id'])
        reg_list = []
        for reg in old_reg_list:
            old_reg_id_list.append(reg['id'])
            if reg['id'] not in new_reg_id_list:
                reg_list.append({
                    'id': reg['id'],
                    'name': reg['name'],
                    'status': 'removed'
                })
        for reg in new_reg_list:
            if reg['id'] not in old_reg_id_list:
                reg_list.append({
                    'id': reg['id'],
                    'name': reg['name'],
                    'status': 'added'
                })
        if reg_list:
            # storing tasks logs for regulation in Task model
            old_reg_id_list = ','.join([str(i) for i in old_reg_id_list]) if old_reg_id_list else ''
            new_reg_id_list = ','.join([str(i) for i in new_reg_id_list]) if new_reg_id_list else ''
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='regulations', prev_value=old_reg_id_list,
                                                     curr_value=new_reg_id_list, extra=reg_list))

        # (regulatory_frameworks):
        old_fw_list = old_data['regulatory_frameworks']
        new_fw_list = updated_data.get('regulatory_frameworks', None)
        old_fw_id_list = []
        new_fw_id_list = []
        for fw in new_fw_list:
            new_fw_id_list.append(fw['id'])
        fw_list = []
        for fw in old_fw_list:
            old_fw_id_list.append(fw['id'])
            if fw['id'] not in new_fw_id_list:
                fw_list.append({
                    'id': fw['id'],
                    'name': fw['name'],
                    'status': 'removed'
                })
        for fw in new_fw_list:
            if fw['id'] not in old_fw_id_list:
                fw_list.append({
                    'id': fw['id'],
                    'name': fw['name'],
                    'status': 'added'
                })
        if fw_list:
            # storing tasks logs for regulatory_frameworks in Task model
            old_fw_id_list = ','.join([str(i) for i in old_fw_id_list]) if old_fw_id_list else ''
            new_fw_id_list = ','.join([str(i) for i in new_fw_id_list]) if new_fw_id_list else ''
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='regulatory_frameworks', prev_value=old_fw_id_list,
                                                     curr_value=new_fw_id_list, extra=fw_list))
        # (news):
        old_news_list = old_data['news']
        new_news_list = updated_data.get('news', None)
        old_news_id_list = []
        new_news_id_list = []
        for news in new_news_list:
            new_news_id_list.append(news['id'])
        news_list = []
        for news in old_news_list:
            old_news_id_list.append(news['id'])
            if news['id'] not in new_news_id_list:
                news_list.append({
                    'id': news['id'],
                    'name': news['title'],
                    'status': 'removed'
                })
        for news in new_news_list:
            if news['id'] not in old_news_id_list:
                news_list.append({
                    'id': news['id'],
                    'name': news['title'],
                    'status': 'added'
                })
        if news_list:
            # storing tasks logs for news in Task model
            old_news_id_list = ','.join([str(i) for i in old_news_id_list]) if old_news_id_list else ''
            new_news_id_list = ','.join([str(i) for i in new_news_id_list]) if new_news_id_list else ''
            '''
            Task history log
            '''
            task_history_obj_list.append(TaskHistory(task_id=old_data['id'], action_user_id=editor_id, action='changed',
                                                     action_field='news', prev_value=old_news_id_list,
                                                     curr_value=new_news_id_list, extra=news_list))

        '''
        Task history log entry
        '''
        TaskHistory.objects.bulk_create(task_history_obj_list, ignore_conflicts=True)

        if variables_dict['has_title_diff'] or variables_dict['has_assignee_diff'] or variables_dict[
            'has_status_diff'] or variables_dict['has_due_date_diff'] or variables_dict['has_description_diff'] or \
                variables_dict['has_product_diff'] or variables_dict['has_archive_diff'] or\
                variables_dict['has_substance_diff']:
            task_editor_qs = TaskEditor.objects.filter(
                Q(task_id=old_data['id']) & ~Q(editor_id=editor_id)).select_related('editor')
            for task_editor in task_editor_qs.all():
                email_to.append(task_editor.editor.email)
            template_id = settings.MAILJET_TASK_UPDATE_NOTIFICATION_TEMPLATE_ID
            send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)
            print('success')
        print('task_management_update_email_notification____________END____________')

    except Exception as ex:
        logger.error(str(ex), exc_info=True)
        print('task_management_update_email_notification____________AN ERROR OCCURRED____________')
