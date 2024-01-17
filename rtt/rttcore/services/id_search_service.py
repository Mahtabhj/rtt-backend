class IdSearchService:
    @staticmethod
    def does_id_exit_in_sorted_list(sorted_list, key_id):
        """
        This function will receive a list as 1st parameter(sorted in ascending order) and an integer value as
        2nd parameter. This function will check whether the integer is present in the list or not. If the value is in
        the list then the function will return true and false otherwise.

        This function is based on 'binary search' algorithm, where:
            [01]. The list must be sorted in ascending order.
            [02]. Time complexity is: O(log n)

        How Binary search algo works:
            Binary search is an efficient algorithm for finding an item from a sorted list of items.
        It works by repeatedly dividing in half the portion of the list that could contain the item,
        until you've narrowed down the possible locations to just one.
        For more info: https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search
        """
        low = 0
        high = len(sorted_list) - 1
        while low <= high:
            mid = (high + low) // 2
            # If key_id is greater, ignore left half
            if sorted_list[mid] < key_id:
                low = mid + 1
            # If key_id is smaller, ignore right half
            elif sorted_list[mid] > key_id:
                high = mid - 1
            # means key_id is present
            else:
                return True

        # If we reach here, then the element was not present
        return False
