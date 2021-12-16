import sys
import os
import shutil

__doc__ = """
Crile is a branch less python file that allows you to create new files and folders
with the name and directory/path that you choose.

Using the "." for the path argument will set it in the current directory

[KEY]:
    * - Optional
    <> - User input

[CREATING FOLDERS]:
    Run: python crile.py folder <name> <*path>
    Ex:
        python crile.py folder testFolder
        python crile.py folder testFolder .

[CREATING FILES]:
    Run: python crile.py py <name> <*path>
    Ex:
        python crile.py py test
        python crile.py py test testFolder

[DELETING FILES & FOLDERS]:
    Run: python crile.py delete <name> <path> <type>
    Ex: 
        python crile.py delete testFile.py . file
        python crile.py delete testFolder . folder

[WIPING FILES]:
    Run: python crile.py wipe <path>
    Ex:
        python crile.py wipe crile-files
        python crile.py wipe .

[RESTORE DEFAULT FILES]:
    Run: python crile.py restore <path>
    Ex:
        python crile.py restore .
        python crile.py restore testFolder

If no path is specified it will be defaulted to the "crile files & folders" folder.
"""


def __default_path(): return os.path.join(os.getcwd(), "crile-files")


def __delete_file(file_data):
    os.chdir(file_data["path"])
    os.remove(file_data["name"])


def __delete_dir(file_data):
    shutil.rmtree(file_data["path"])


def __delete(file_name, path, object_type):
    object_conditional = {0: __delete_dir, 1: __delete_file}
    object_path = os.path.join(os.getcwd(), path)
    object_conditional[(object_type == "file")]({"name": file_name, "path": object_path})


def __wipe_files(path):
    folder_path = os.path.join(os.getcwd(), path)
    input(f"[WARNING]: Your about to wipe all files in the directory: \"{folder_path}\"; \nPress Enter to Continue...")
    shutil.rmtree(folder_path)


def __create_folder(folder_name, path):
    not_null_conditional = {0: __default_path, 1: (lambda: os.path.join(os.getcwd(), path))}
    new_folder_path = os.path.join(not_null_conditional[(path is not None) + 0](), folder_name)
    os.makedirs(new_folder_path)


def __create_file(file_name, path):
    not_null_conditional = {0: __default_path, 1: (lambda: os.path.join(os.getcwd(), path))}
    new_file_path = not_null_conditional[(path is not None) + 0]()
    os.chdir(new_file_path)
    with open(f"{file_name}.py", "x") as FILE:
        FILE.close()


def __call_restore(path):
    os.chdir(path)
    os.makedirs("crile-files")


def __restore(path):
    not_false_conditional = {1: __call_restore}
    full_file_path = os.path.join(os.getcwd(), path)
    path_exists = os.path.exists(full_file_path) + 0

    try:
        not_false_conditional[path_exists](full_file_path)
    except KeyError:
        print(f"File path: \"{full_file_path}\"; does not exist!")


def main():
    file_conditional = {1: __create_file}
    folder_conditional = {1: __create_folder}
    wipe_conditional = {1: __wipe_files}
    delete_conditional = {1: __delete}
    restore_conditional = {1: __restore}

    create_option = sys.argv[1]
    object_name = sys.argv[2]

    try: object_path = sys.argv[3]
    except IndexError: object_path = None
    try: object_type = sys.argv[4]
    except IndexError: object_type = None

    try:
        folder_conditional[(create_option == "folder") + 0](object_name, object_path)
    except KeyError:
        pass
    try:
        file_conditional[(create_option == "py") + 0](object_name, object_path)
    except KeyError:
        pass
    try:
        wipe_conditional[(create_option == "wipe") + 0](object_name) # Should be the path of which the files inside will be wiped
    except KeyError:
        pass
    try:
        delete_conditional[(create_option == "delete") + 0](object_name, object_path, object_type)
    except KeyError:
        pass
    try:
        restore_conditional[(create_option == "restore") + 0](object_name) # Should be the path where the files will be created
    except KeyError:
        pass

if __name__ == "__main__":
    main()
