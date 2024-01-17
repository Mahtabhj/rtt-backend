from django.utils import timezone


class TaskListDisplayService:
    @staticmethod
    def get_task_list(task_doc_queryset):
        today = timezone.now()
        result = []
        for task in task_doc_queryset:
            assignee_obj = None
            if task.assignee:
                assignee_obj = {
                    'id': task.assignee.id,
                    'first_name': task.assignee.first_name,
                    'last_name': task.assignee.last_name,
                    'avatar': task.assignee.avatar
                }
            result.append({
                'id': task.id,
                'status': task.status,
                'name': task.name,
                'products': [{'id': product.id, 'name': product.name, 'image': product.image}
                             for product in task.products],
                'assignee': assignee_obj,
                'due_date': task.due_date,
                'overdue': True if (task.due_date and today > task.due_date) else False
            })

        return result
