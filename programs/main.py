from _resource import *
import os

__doc__ = """
----- HELP -----
[COMMANDS]:
    - cd <file name>
    - view <file name>

[CD COMMAND]:
    Navigates you to the specified file name, if it does not exist
    it leaves you at the file already selected.

[VIEW COMMAND]:
    Prints the doc of the file currently selected, which explains what the file does
    and how to use the file.

[SOURCE CODE CONCERNS]:
    If you are wondering why the source code for the files seems to be more complicated
    then it should be. It would be due to the fact that all files in the "branchless-program"
    file are, well branchless. None of the files here SHOULD contain if statements.
"""

__DIVIDER = "-----------------------"


def selected_print(file_name): print(f"    - {file_name} <<")
def unselected_print(file_name): print(f"    - {file_name}")


def __call_rotate(formatted_input, list_of_files):
    call_conditional = {1: (lambda file_index: file_index)}

    file_run_outputs = []
    for index, file_name in enumerate(list_of_files):
        try:
            file_run_outputs.append(call_conditional[(file_name == formatted_input[1])](index))
        except (IndexError, KeyError):
            continue
    return file_run_outputs


def __call_view(file_name):
    return __import__(file_name.split('.')[0]).__doc__


def view(raw_input, list_of_files, current_index):
    split_input = raw_input.split(" ")
    is_null_conditional = {1: __call_view}

    try:
        conditional = (split_input is not None) * \
                      (split_input[1] == list_of_files[current_index])
        print(__DIVIDER)
        file_doc = is_null_conditional[conditional](split_input[1])
        print(file_doc)
        print(__DIVIDER)
        input("Press Enter to Continue...")
    except (IndexError, KeyError):
        print(__DIVIDER)
        print(f"Unable to view the doc for the file \"{split_input[1]}\". Make sure the file is selected and exists.")
        input("Press Enter to Continue...")
        print(__DIVIDER)


def rotate(raw_input, list_of_files, current_index):
    split_input = raw_input.split(" ")
    is_null_conditional = {1: __call_rotate}

    try:
        conditional = (split_input is not None) + 0
        new_file_name = is_null_conditional[conditional](split_input, list_of_files)
        return new_file_name[0]
    except (IndexError, KeyError):
        return current_index


def main():
    print_conditional = {0: unselected_print, 1: selected_print}
    rotate_conditional = {1: rotate}
    view_conditional = {1: view}
    help_conditional = {1: (lambda: {'index': 0, 'cmd': "view main.py"})}

    index = 0
    while True:
        raw_files = os.listdir()
        raw_files = removeItems([".idea", "__pycache__", "crile-files"], raw_files)
        raw_files = repositionItemInList(0, "main.py", raw_files)

        selected = raw_files[index]

        print(f"\n{__DIVIDER}")
        print("Files:")
        for file_name in raw_files:
            print_conditional[(selected == file_name)](file_name)
        print(__DIVIDER)
        print('Type "help" for a list of commands.')
        cmd = input("Execute Command: ")

        try:
            destructed = help_conditional[(cmd == "help")+0]()
            index = destructed["index"]
            cmd = destructed["cmd"]
        except KeyError:
            try: index = rotate_conditional[(cmd.split(" ")[0] == "cd") + 0](cmd, raw_files, index)
            except KeyError:
                try: view_conditional[(cmd.split(" ")[0] == "view") + 0](cmd, raw_files, index)
                except KeyError: continue


if __name__ == "__main__":
    main()
