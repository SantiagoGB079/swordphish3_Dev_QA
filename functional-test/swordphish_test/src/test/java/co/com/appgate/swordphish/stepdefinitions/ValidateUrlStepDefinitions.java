package co.com.appgate.swordphish.stepdefinitions;

import co.com.appgate.swordphish.models.RequestMessage;
import co.com.appgate.swordphish.utils.Consumer;
import co.com.appgate.swordphish.utils.Producer;
import cucumber.api.java.Before;
import cucumber.api.java.en.And;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.hamcrest.MatcherAssert;
import org.hamcrest.Matchers;
import java.util.*;

import static co.com.appgate.swordphish.utils.Constants.*;

public class ValidateUrlStepDefinitions {

    List<String> url = new ArrayList<>();
    List<Boolean> listPhishing = new ArrayList<>();
    KafkaProducer<String, String> producer;
    KafkaConsumer<String, String> consumer;

    @Before
    public void setUp() {
        Properties properties1 = new Properties();
        properties1.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        properties1.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties1.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producer = new KafkaProducer<>(properties1);

        Properties propertiesSalida = new Properties();
        propertiesSalida.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        propertiesSalida.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        propertiesSalida.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        propertiesSalida.setProperty(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        propertiesSalida.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");

        consumer = new KafkaConsumer<>(propertiesSalida);
    }

    @When("^the user send to url$")
    public void theUserSendToUrl(Map<String, Boolean> urls) {
        for (Map.Entry m : urls.entrySet()) {
            url.add("" + m.getKey());
            listPhishing.add(Boolean.valueOf(m.getValue().toString()));
        }
    }

    @And("^the information$")
    public void theInformation(List<RequestMessage> data) {
        data.get(0).setUrls(url);
        Producer.producerKafka(data, producer, TOPIC_ENTRADA);
    }

    @Then("^the user will see a score with criteria of (.*)$")
    public void theUserWillSeeAScoreGreaterAndLessThan(double score) {
        List<Double> scorePoint = Consumer.ValidateScore(consumer, TOPIC_SALIDA);

        for (int i = 0; i < scorePoint.size(); i++) {
            if ((!listPhishing.get(i))) {
                MatcherAssert.assertThat(scorePoint.get(i), Matchers.lessThan(score));
            } else {
                MatcherAssert.assertThat(scorePoint.get(i), Matchers.greaterThan(score));

            }
        }
    }

}
