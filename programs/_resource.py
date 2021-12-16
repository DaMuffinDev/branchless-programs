

__doc__ = """
Contains a list of functions that are for the use of other files.
"""


def repositionItemInList(__index, __item, __list):
    __list.remove(__item)
    __list.insert(0, __item)
    return __list


def removeItems(__item_list, __list):
    for item in __item_list:
        try:
            __list.remove(item)
        except ValueError:
            continue
    return __list
