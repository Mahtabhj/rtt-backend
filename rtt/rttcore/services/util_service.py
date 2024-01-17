class UtilsService:
    @staticmethod
    def has_more(total_count, per_page_data_limit, current_page_num):
        has_more = True
        if (total_count - per_page_data_limit * current_page_num) < 1:
            has_more = False
        return has_more
