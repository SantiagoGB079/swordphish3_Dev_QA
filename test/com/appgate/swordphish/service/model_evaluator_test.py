import os.path
import sys
import unittest
from tensorflow import keras

from main.com.appgate.swordpish.service.features_provider import FeaturesProvider
from main.com.appgate.swordpish.service.model_evaluator import ModelEvaluator


class ModelEvaluatorTest(unittest.TestCase):

    def test_evaluate_should_retrieve_score_for_non_suspicious_url(self):
        """
        Test scenario: Legal URL should be evaluated with a score less than 0.5
            GIVEN: a well known url
             WHEN: Model Evaluator receives the url features
              AND: Model Evaluator execute the model evaluation
             THEN: the url score should be greater than 0
              AND: url score should be less than 0.5
        """

        # Arrange ...
        base_path = os.path.dirname(sys.path[0])
        model_path = os.path.join(base_path, 'model/swordphish3_dnn_features_appgate_may2021_train_nlp_model_v1.h5')
        model_evaluator = ModelEvaluator(model=keras.models.load_model(model_path))
        features = self.__make_url_features('https://somesite.com')

        # Act ...
        evaluation_result = model_evaluator.evaluate(features)
        print(f'Score for non suspicious url should be less than 0.5: [Score: {evaluation_result}]')

        # Assert ...
        self.assertTrue(float(evaluation_result) > 0)
        self.assertTrue(float(evaluation_result) < 0.5)

    def test_evaluate_should_retrieve_score_for_phishing_url(self):
        """
        Test scenario: Phishing URL should be evaluated with a score greater than 0.5
            GIVEN: a suspicious url
             WHEN: Model Evaluator receives the url features
              AND: Model Evaluator execute the model evaluation
             THEN: the url score should be greater than 0
              AND: url score should be greater than 0.5
        """

        # Arrange ...
        base_path = os.path.dirname(sys.path[0])
        model_path = os.path.join(base_path, 'model/swordphish3_dnn_features_appgate_may2021_train_nlp_model_v1.h5')
        model_evaluator = ModelEvaluator(model=keras.models.load_model(model_path))
        features = self.__make_url_features(
            'https://wdestaques24.acho-que-voce-pode-gostar-disso.co/destaques/americanas/produto/144563110/notebook'
            '-dell-gaming-g3-3590-a20p-9-intel-core-i5-8gb-geforce-gtx-1050-com-3gb-1tb-128gb-ssd-15-6-windows-10'
            '?fbclid=IwAR31nJFckNvfhH5opcoSvHGohz0ZQbgSnyvVoilDgUx5oGENMIPP9AtvIpA')

        # Act ...
        evaluation_result = model_evaluator.evaluate(features)
        print(f'Score for suspicious url should be greater than 0.5: [Score: {evaluation_result}]')

        # Assert ...
        self.assertTrue(float(evaluation_result) > 0.5)

    # noinspection PyMethodMayBeStatic
    def __make_url_features(self, url):
        return {url: {"url": url} | FeaturesProvider().extractFeaturesFromUrl(url)}
