import logging.config
import os

import yaml


def loadConfig(config_path,
               default_level=logging.DEBUG,
               default_format="%(asctime)s %(levelname)s %(name)s: %(message)s"):
    if os.path.exists(config_path):
        try:
            logging.config.dictConfig(yaml.load(open(config_path, 'rb').read(), Loader=yaml.FullLoader))
        except Exception as e:
            print(e)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=default_level, format=default_format)
    else:
        logging.basicConfig(level=default_level, format=default_format)
        print('Failed to load configuration file. Using default configs')
