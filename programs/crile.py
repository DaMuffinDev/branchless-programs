import sys
import os
import json
import time


with open("../documentation/crile-doc.txt", "r") as DOC_FILE:
    __doc__ = DOC_FILE.read()


__DEFAULT_CRILE_JSON = \
"""{
    "@crile-compiler": [
        {
            "@settings": {
                "safe-run": true,
                "run-time": 0.05,
                "print-cmds": true
            }
        }
    ]
}
"""


def __call_keyError():
    raise KeyError


def __setup_json(name, path):
    __DEFAULT_FILE = "crile-jsons"

    does_directory_exists_conditional = {1: (lambda path: os.path.join(os.getcwd(), path))}
    does_file_exist_conditional = {1: (lambda: 0)}
    replace_file_conditional = {0: (lambda: 0), 1: __call_keyError}
    valid_replace_conditional = {0: (lambda: 0), 1: (lambda: 1)}

    try: path = does_directory_exists_conditional[(path is not None) + 0](path)
    except KeyError: path = os.getcwd()

    os.chdir(path)
    try: full_path = does_directory_exists_conditional[(path is not None) * (os.path.exists(
        os.path.join(
            os.path.join(
                os.getcwd(), path), __DEFAULT_FILE))) + 0](__DEFAULT_FILE)
    except KeyError: 
        os.makedirs(__DEFAULT_FILE)
        full_path = os.path.join(os.getcwd(), __DEFAULT_FILE)

    os.chdir(os.path.join(path, __DEFAULT_FILE))
    does_file_exist = os.path.exists(os.path.join(full_path, f"{name}.json"))

    try: 
        does_file_exist_conditional[(does_file_exist) + 0]()
        print(f"The file \"{name}.json\" already exists. Would you like to replace it?")
        should_replace = input(f"Y(1), N(0): ")

        try: valid_replace_conditional[int(should_replace)]()
        except: 
            print(f"Invalid input \"{should_replace}\", expected \"0\" or \"1\"; Operation Cancelled.")
            sys.exit(1)

        replace_file_conditional[int(should_replace)]()
    except KeyError:
        with open(f"{name}.json", "w") as new_json:
            new_json.write(__DEFAULT_CRILE_JSON)


def __run_json(json_file):
    os.chdir(os.getcwd())

    json_setting_conditional = {1: (lambda: 0)}

    json_type_conditional = {1: (lambda _type: f" {_type}")}
    json_path_conditional = {1: (lambda path: f" {path}")}
    json_name_conditional = {1: (lambda name: f" {name}")}
    json_new_path_conditional = {1: (lambda new_path: f" {new_path}")}
    json_new_name_conditional = {1: (lambda new_name: f" {new_name}")}
    json_delete_type_conditional = {1: (lambda delete_type: f" {delete_type}")}

    with open(json_file) as JSON:
        json_data = json.load(JSON)
    
    commands = []
    json_comp = json_data["@crile-compiler"]
    setting_data = {}
    
    for cmd in json_comp:
        try: 
            json_setting_conditional["@settings" in cmd]()
            setting_data = cmd
        except KeyError:
            command_template = "python crile.py"

            try: command_template += json_type_conditional[("type" in cmd) + 0](cmd["type"])
            except KeyError: pass

            try: command_template += json_name_conditional[("name" in cmd) + 0](cmd["name"])
            except KeyError: pass
            
            try: command_template += json_path_conditional[("path" in cmd) + 0](cmd["path"])
            except KeyError: pass

            try: command_template += json_new_name_conditional[("new_name" in cmd) + 0](cmd["new_name"])
            except KeyError: pass

            try: command_template += json_new_path_conditional[("new_path" in cmd) + 0](cmd["new_path"])
            except KeyError: pass

            try: command_template += json_delete_type_conditional[("delete_type" in cmd) + 0](cmd["delete_type"])
            except KeyError: pass
            
            commands.append(command_template)

    safe_run_conditional = {1: (lambda: 0)}
    print_run_conditional = {1: (lambda: 0)}
    setting_data = setting_data["@settings"]
    for runnable_cmd in commands:
        try:
            print_run_conditional[("print-cmds" in setting_data) + 0]() 
            print(runnable_cmd)
        except KeyError: pass
        try:
            safe_run_conditional[("safe-run" in setting_data) + 0]()
            time.sleep(setting_data["run-time"])
        except KeyError: pass
        os.system(runnable_cmd)


def __default_path(): return os.path.join(os.getcwd(), "crile-files")


def __delete_file(file_data):
    os.chdir(file_data["path"])
    os.remove(file_data["name"])


def __delete_dir(file_data):
    os.chdir(file_data["path"])
    shutil.rmtree(file_data["path"])


def __delete(file_name, path, object_type):
    delete_file_conditional = {1: __delete_file}
    delete_directory_conditional = {2: __delete_dir}
    object_path = os.path.join(os.getcwd(), path)
    delete_data = {"name": file_name, "path": object_path}
    try:
        delete_file_conditional[(object_type == "file") + 0](delete_data)
        return
    except KeyError: pass
    try: 
        delete_directory_conditional[(object_type == "folder") + 0](delete_data)
        return
    except KeyError: pass

    print(f"[ERROR]: Cannot delete \"{file_name}\"; An unknown error occured.")
    sys.exit(1)


def __wipe_files(path):
    folder_path = os.path.join(os.getcwd(), path)
    try: input(f"[WARNING]: You're about to wipe all files in the directory: \"{folder_path}\"; \nPress Enter to Continue OR (CTRL+C) to cancel...")
    except KeyboardInterrupt: print("\nOperation Aborted.\n")
    shutil.rmtree(folder_path)


def __create_folder(folder_name, path):
    not_null_conditional = {0: __default_path, 1: (lambda: os.path.join(os.getcwd(), path))}
    does_directory_exist_conditional = {1: (lambda directory: print(f"[ERROR]: Cannot create a directory that already exists: \"{directory}\""))}
    new_folder_path = os.path.join(not_null_conditional[(path is not None) + 0](), folder_name)
    try:
        does_directory_exist_conditional[os.path.exists(new_folder_path) + 0](new_folder_path)
        sys.exit(1)
    except KeyError: pass
    os.makedirs(new_folder_path)


def __copy_file_data(file, path):
    os.chdir(path)
    with open(file, "r") as f:
        contents = f.read()
    return contents


def __copy(file, path, new_file, new_file_path):
    old_file_path = os.path.join(os.getcwd(), path)

    does_directory_exist_conditional = {1: (lambda directory: print(f"[ERROR]: Directory \"{directory}\" does not exist!"))}
    is_new_path_conditional = {0: (lambda: old_file_path), 1: (lambda: os.path.join(os.getcwd(), new_file_path))}
    does_file_exist_conditional = {1: __create_file}

    new_file_path = is_new_path_conditional[(not new_file_path == old_file_path) + 0]()

    try:
        does_directory_exist_conditional[not os.path.exists(old_file_path) + 0](old_file_path)
        does_directory_exist_conditional[not os.path.exists(new_file_path) + 0](new_file_path)
        sys.exit(1)
    except KeyError: pass

    file_data = __copy_file_data(file, old_file_path)

    os.chdir(new_file_path)
    try: does_file_exist_conditional[(not os.path.exists(new_file_path)) + 0](new_file, new_file_path)
    except KeyError: pass

    with open(new_file, "w") as new_file:
        new_file.write(file_data)


def __create_file(file_name, path):
    not_null_conditional = {0: __default_path, 1: (lambda: os.path.join(os.getcwd(), path))}
    does_file_exist_conditional = {1: (lambda file_name: print(f"[ERROR]: Cannot create a file that already exists: \"{file_name}\""))}
    new_file_path = not_null_conditional[(path is not None) + 0]()

    try:
        does_file_exist_conditional[os.path.exists(os.path.join(new_file_path, file_name)) + 0](file_name)
        sys.exit(1)
    except KeyError: pass

    os.chdir(new_file_path)
    with open(f"{file_name}.py", "w") as FILE:
        FILE.close()


def __call_restore(path):
    does_directory_exist_conditional = {1: (lambda: 0)}
    os.chdir(path)
    try: does_directory_exist_conditional[(os.path.exists(path)) + 0]()
    except KeyError: os.makedirs("crile-files")


def __restore(path):
    not_false_conditional = {1: __call_restore}
    full_file_path = os.path.join(os.getcwd(), path)
    path_exists = os.path.exists(full_file_path) + 0

    try: not_false_conditional[path_exists](full_file_path)
    except KeyError: print(f"File path: \"{full_file_path}\"; does not exist!")


def main():
    file_conditional = {1: __create_file}
    folder_conditional = {1: __create_folder}
    wipe_conditional = {1: __wipe_files}
    delete_conditional = {1: __delete}
    restore_conditional = {1: __restore}
    copy_conditional = {1: __copy}
    json_run_conditional = {1: __run_json}
    json_setup_conditional = {1: __setup_json}

    create_option = sys.argv[1]

    try: optional_arg2 = sys.argv[2]
    except IndexError: optional_arg2 = None
    try: optional_arg3 = sys.argv[3]
    except IndexError: optional_arg3 = None
    try: optional_arg4 = sys.argv[4]
    except IndexError: optional_arg4 = None
    try: optional_arg5 = sys.argv[5]
    except IndexError: optional_arg5 = None

    try: folder_conditional[(create_option == "folder") + 0](sys.argv[2], optional_arg3)
    except KeyError: pass

    try: file_conditional[(create_option == "py") + 0](sys.argv[2], optional_arg3)
    except KeyError: pass

    try: wipe_conditional[(create_option == "wipe") + 0](sys.argv[2])
    except KeyError: pass

    try: delete_conditional[(create_option == "delete") + 0](sys.argv[2], sys.argv[3], sys.argv[4])
    except Exception as e:
        index_error_conditional = {1: (lambda: print("[ERROR]: Delete function missing arguments..."))}
        try: index_error_conditional[(e.__class__.__name__ == "IndexError") + 0]()
        except KeyError: pass
    
    try: restore_conditional[(create_option == "restore") + 0](sys.argv[2])
    except KeyError: pass

    try: copy_conditional[(create_option == "copy") + 0](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    except Exception as e:
        index_error_conditional = {1: (lambda: print("[ERROR]: Copy function missing arguments..."))}
        try: index_error_conditional[(e.__class__.__name__ == "IndexError") + 0]()
        except KeyError: pass

    try: json_run_conditional[(create_option == "run-json") + 0](sys.argv[2])
    except KeyError: pass

    try: json_setup_conditional[(create_option == "setup-json") + 0](sys.argv[2], optional_arg3)
    except KeyError: pass


if __name__ == "__main__":
    main()
