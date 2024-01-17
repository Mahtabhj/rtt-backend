class ImpactAssessmentAnswerService:
    @staticmethod
    def get_answer_object(answer, current_user):
        pinned_by_obj = None
        if answer.pin_by:
            pinned_by_obj = {
                'id': answer.pin_by.id,
                'username': answer.pin_by.username,
                'first_name': answer.pin_by.first_name if answer.pin_by.first_name else None,
                'last_name': answer.pin_by.last_name if answer.pin_by.last_name else None,
            }
        answer_obj = {
            'id': answer.id,
            'answer_text': answer.answer_text,
            'date': answer.created,
            'can_edit': True if current_user == answer.answered_by.id else False,
            'edited': answer.edited if answer.edited else None,
            'answered_by': {
                'id': answer.answered_by.id,
                'username': answer.answered_by.username,
                'first_name': answer.answered_by.first_name if answer.answered_by.first_name else None,
                'last_name': answer.answered_by.last_name if answer.answered_by.last_name else None,
                'avatar': answer.answered_by.avatar.url if answer.answered_by.avatar else None
            },
            'pinned_by': pinned_by_obj
        }
        return answer_obj
