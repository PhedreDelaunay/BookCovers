
class DebugHelper:
    """functions to aid with debugging"""

    # example
    # from bookcovers.debug_helper import DebugHelper
    # DebugHelper.print_dictionary(kwargs, "get_subject")
    @staticmethod
    def print_dictionary(dict: dict, prefix: str=None):
        for i, v in dict.items():
            print(f"    {prefix}", i, ": ", v)


    @staticmethod
    def print_dict_list(list_of_dicts):
        for dict in list_of_dicts:
            print(f"{dict}")