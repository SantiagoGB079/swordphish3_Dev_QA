import os


def get_root_path() -> object:
    return str(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 2)[0])


def get_root_project_path():
    return str(get_root_path())
