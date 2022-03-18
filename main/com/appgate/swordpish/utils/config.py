from configparser import ConfigParser
from .project_utils import get_root_project_path


def config(section: object) -> object:
    filename = get_root_project_path() + '/configuration/params.ini'
    parser = ConfigParser()
    parser.read(filename)
    config_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for index, param in enumerate(params):
            config_params[params[index][0]] = params[index][1]
    else:
        raise Exception('Error: Section {0}, in the file {1}, does not exist'.format(section, filename))

    return config_params
