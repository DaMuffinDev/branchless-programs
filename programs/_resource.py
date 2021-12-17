

with open("../documentation/resource-doc.txt", "r") as DOC_FILE:
    __doc__ = DOC_FILE.read()


def repositionItemInList(__index, __item, __list):
    __list.remove(__item)
    __list.insert(__index, __item)
    return __list


def removeItems(__item_list, __list):
    for item in __item_list:
        try:
            __list.remove(item)
        except ValueError:
            continue
    return __list


def removeNonePyExtensions(__list):
    has_py_extension_conditional = {1: (lambda: 0)}
    
    invalid_items = []
    for item in __list:
        try: has_py_extension_conditional[(item.split(".")[1] == "py") + 0]()
        except (KeyError, IndexError): invalid_items.append(item)
    __list = removeItems(invalid_items, __list)
    return __list