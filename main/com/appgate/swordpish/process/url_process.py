import collections
import os

from rx import from_future, from_list, repeat_value, operators as op
from rx.subject import Subject
import logging

CustomConsumerRecord = collections.namedtuple("CustomConsumerRecord", ["value"])


class UrlProcess:
    def __init__(self, kafka_provider, model_evaluator, features_provider, config):
        self.__model_evaluator = model_evaluator
        self.__features_provider = features_provider
        self.__config = config
        self.logger = logging.getLogger(__class__.__name__)
        self.consumer = kafka_provider.consumer()
        self.consumer.subscribe([self.__get_topic_to_subscribe()])
        self.producer = kafka_provider.producer()

    def flow(self):
        return repeat_value(0).pipe(
            op.map(lambda s: self.__next_message()),
            op.do_action(lambda m: self.logger.debug("Producer record %s", m)),
            op.map(lambda s: s.value),
            op.flat_map(lambda message:
                        from_list(message['urls']).pipe(
                            op.map(self.__extract_features),
                            op.do_action(lambda m: self.logger.debug("Got features: %s", m)),
                            op.map(self.__evaluate),
                            op.do_action(lambda m: self.logger.debug("Got result: %s", m)),
                            op.reduce(lambda acc, x: acc + [x], list()),
                            op.map(lambda scores: message | {"response": scores})
                        )),
            op.do_action(lambda m: self.logger.debug("Final result %s", m)),
            op.map(lambda message: self.producer.send(self.__get_topic_to_publish(), message)),
            op.flat_map(self.__future_to_observable),
            op.do_action(lambda m: self.logger.debug("Resulting score %s", m),
                         lambda e: self.logger.error("Url process error: %s", e)),
            op.retry(),
        )

    def __get_topic_to_subscribe(self):
        suscribeTopic = os.environ['SUSCRIBE_TOPIC']
        return suscribeTopic

    def __get_topic_to_publish(self):
        publishTopic = os.environ['PUBLISH_TOPIC']
        return publishTopic

    def __next_message(self):
        try:
            element = next(self.consumer)
            self.logger.debug("Next element: {}".format(element))
            return self.__craft_basic_response(element, "OK")
        except Exception as e:
            self.logger.error("Error detail: %s", e)
            return self.__craft_basic_response(CustomConsumerRecord({}), "ERROR", "Error detail: {0}".format(e))

    def __evaluate(self, message):
        try:
            score = self.__model_evaluator.evaluate(message['features'])
            return self.__craft_eval_response(message, score, None)
        except Exception as e:
            self.logger.error("Eval error: %s", e)
            return self.__craft_eval_response(message, 0, "Eval error: {0}".format(e))

    # noinspection PyMethodMayBeStatic
    def __craft_basic_response(self, element, response_status, response_message=""):
        return CustomConsumerRecord(
            {"responseStatus": response_status, "errorMessage": response_message} | element.value)

    # noinspection PyMethodMayBeStatic
    def __craft_eval_response(self, message, score, error):
        return message | {"score": score, "error": error}

    def __extract_features(self, url):
        return {
            "url": url,
            "features":
                {
                    url: {"url": url} | self.__features_provider.extractFeaturesFromUrl(url)
                }
        }

    # noinspection PyMethodMayBeStatic
    def __future_to_observable(self, future_record_metadata):
        subject = Subject()
        future_record_metadata \
            .add_callback(subject.on_next) \
            .add_errback(subject.on_error)
        return subject
