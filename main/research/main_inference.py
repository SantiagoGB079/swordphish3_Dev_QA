import pandas as pd
from tensorflow import keras
import glob
import json
import urllib.request as urlr
import interruptingcow
import main.research.Feature_Extractor as fe
from main.research.Feature_Extractor.Parser import url_parser
from main.research.models import models_utils
import sys

TIME_WAIT = 20


class TimeOutError(Exception):
    """InterruptingCow exceptions cause by timeout"""
    pass


def menu():
    # Reading existing models
    MODELS_DIRECTORY_PATH = 'model/*'
    existing_models = glob.glob(MODELS_DIRECTORY_PATH)
    print('----------------Making an inference from an existing model----------------')
    print('Select the model desired from the current ones:')
    current_models(existing_models)
    num_model = input()
    print('You have selected: ' + existing_models[int(num_model)])
    print('Input the full URL to evaluate (ex. https://www.youtube.com),')
    print('some phishing are available at https://awesomeopensource.com/project/mitchellkrogza/Phishing.Database')
    url = input()
    return existing_models[int(num_model)], url


def current_models(existing_models):
    num = 0
    for model_localization in existing_models:
        print('Input ' + str(num) + ' for ' + model_localization)
        num += 1


def features_from_url(url_input):
    result = {}
    page = urlr.urlopen(url_input, timeout=10)
    try:
        if page.getcode() == 200:
            with interruptingcow.timeout(TIME_WAIT, exception=TimeOutError):
                tag = url_parser.URL(url_input).domain
                content = fe.main(url_input, '0')
                result.update(
                    {tag: content.whois}
                )
    except(Exception) as error:
        print(error)

    return result


if __name__ == '__main__':
    file_json = 'data/processed/single_URL_features.json'
    path_model, objective = menu()

    # Feature extraction and store
    adhoc_features = features_from_url(objective)
    json_data = open(file_json, 'w')
    json.dump(adhoc_features, json_data, indent=4)
    json_data.close()

    # Loading features and model
    features = pd.read_json(file_json, orient='index')
    features.sort_index(axis=1, inplace=True)
    if len(features) == 0:
        sys.exit('No features')
    print('Loading model ...')
    x_test, y_test = models_utils.input_output_split(data=features, output_column='label')
    x_test = models_utils.input_preprocessing(x=x_test, features_type='soc+nlp')
    model = keras.models.load_model(path_model)

    # Prediction
    y_predicted = model.predict(x_test)

    print('Score obtained: ' + str(y_predicted[0, 0]))

    if y_predicted[0, 0] > 0.5:
        print('Phishing page')
    else:
        print('Legal page')
