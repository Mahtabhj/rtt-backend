import difflib


class SequenceMatcherService:

    @staticmethod
    def get_highlighted_unified_diff_string(old_string, new_string):
        if old_string:
            old_string = list(old_string.split())
        else:
            old_string = []
        if new_string:
            new_string = list(new_string.split())
        else:
            new_string = []
        highlighted_str = ''
        space_str = ''
        green_space = "<span style='background-color:#93c47d'> </span>"
        red_space = "<span style='background-color:#ea9999'> </span>"
        prev_status = ''
        count = 0
        for diff in difflib.unified_diff(old_string, new_string, n=len(old_string) + len(new_string)):
            count += 1
            if count > 3:
                dif_status = diff[:1]
                if dif_status == '+':
                    if space_str and prev_status == '+':
                        space_str = green_space
                    highlighted_str += f"{space_str}<span style='background-color:#93c47d'>{diff[1:]}</span>"
                    space_str = ' '
                    prev_status = '+'
                elif dif_status == '-':
                    if space_str and prev_status == '-':
                        space_str = red_space
                    highlighted_str += f"{space_str}<span style='background-color:#ea9999'>{diff[1:]}</span>"
                    space_str = ' '
                    prev_status = '-'
                else:
                    highlighted_str += f"{space_str}{diff[1:]}"
                    space_str = ' '
                    prev_status = ''

        return count > 3, highlighted_str
