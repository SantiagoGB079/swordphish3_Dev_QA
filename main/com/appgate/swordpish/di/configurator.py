import os

from dependency_injector import containers, providers
from tensorflow import keras

from main.com.appgate.swordpish.di import loadConfig
from main.com.appgate.swordpish.process.url_process import UrlProcess
from main.com.appgate.swordpish.service.features_provider import FeaturesProvider
from main.com.appgate.swordpish.service.kafka.kafka_provider import KafkaProvider
from main.com.appgate.swordpish.service.model_evaluator import ModelEvaluator
import confuse
import logging


class Configurator(containers.DeclarativeContainer):

    config = confuse.Configuration('Swordphish', __name__)
    loadConfig('../config/logging.yml')

    # ------------------------------------------------------------------------------------------------------------------
    # Kafka configuration
    # ------------------------------------------------------------------------------------------------------------------

    logging.info('Configuring Kafka ...')
    kafka_provider = providers.Singleton(KafkaProvider, '')

    # ------------------------------------------------------------------------------------------------------------------
    # Model Evaluator configuration
    # ------------------------------------------------------------------------------------------------------------------

    logging.info('Configuring Swordphish3 model ...')
    model = os.environ['MODEL_PROCESS']
    model_evaluator = providers.Singleton(ModelEvaluator, model=keras.models.load_model(model))
    logging.info('Sowrdphish3 model successfully configured: [%s]', model)

    # ------------------------------------------------------------------------------------------------------------------
    # Features Provider configuration
    # ------------------------------------------------------------------------------------------------------------------

    features_provider = providers.Singleton(FeaturesProvider)

    # ------------------------------------------------------------------------------------------------------------------
    # URL processor configuration
    # ------------------------------------------------------------------------------------------------------------------

    url_process = providers.Singleton(
        UrlProcess,
        kafka_provider=kafka_provider,
        model_evaluator=model_evaluator,
        features_provider=features_provider,
        config='')
