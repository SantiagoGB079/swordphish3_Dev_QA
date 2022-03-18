import logging
from main.research.models import models_utils
import json
import pandas as pd
from io import StringIO


class ModelEvaluator:

    def __init__(self, model):
        self.logger = logging.getLogger(__class__.__name__)
        self.__model = model

    def evaluate(self, features_dictionary):
        self.logger.debug("****** evaluate %s", features_dictionary)
        json_dump = json.dumps(features_dictionary, indent=4)
        self.logger.debug("****** read_json %s", json_dump)
        features = pd.read_json(StringIO(json_dump), orient='index')
        self.logger.debug("****** features.sort_index %s", features)
        features.sort_index(axis=1, inplace=True)
        self.logger.debug("input_output_split %s", features)
        if len(features) == 0:
            raise Exception('No features')
        x_test, y_test = models_utils.input_output_split(data=features, output_column='label')
        self.logger.debug("input_preprocessing x %s", x_test)
        self.logger.debug("input_preprocessing y %s", y_test)
        x_test = models_utils.input_preprocessing(x=x_test, features_type='nlp')

        # Prediction
        self.logger.debug(">>>>>>>>>>>>>>> predict %s", x_test)
        y_predicted = self.__model.predict(x_test)
        return str(y_predicted[0, 0])
