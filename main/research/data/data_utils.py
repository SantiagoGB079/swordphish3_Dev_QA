import pandas as pd


def save_dataset(data, path, format):
    if format == 'JSON':
        data.to_json('{}.json'.format(path))
    else:
        print('Format {} is not supported.'.format(format))
        exit()


def load_dataset(path, format):
    if format == 'JSON':
        data = pd.read_json('{}.json'.format(path))
    else:
        print('Format {} is not supported.'.format(format))
        exit()
    return data