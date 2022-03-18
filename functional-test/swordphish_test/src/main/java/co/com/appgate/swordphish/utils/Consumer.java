package co.com.appgate.swordphish.utils;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Consumer {

    public static List<Double> ValidateScore(KafkaConsumer<String, String> consumer, String topicSalida) {

        Logger logger = LoggerFactory.getLogger(Consumer.class.getName());
        consumer.subscribe(Collections.singleton(topicSalida));

        boolean flag = true;
        List <Double> score = new ArrayList<>();

        while (flag) {
            ConsumerRecords<String, String> records =
                    consumer.poll(Duration.ofMillis(100));

            for (ConsumerRecord<String, String> record : records) {
                logger.info("\n[][][][][][][][][][][][][][]MOSTRANDO INFORMACION[][][][][][][][][][][][][][]\n");
                logger.info("Partition: " + record.partition() + ", offSet: " + record.offset());
                JSONObject json = new JSONObject(record.value());
                logger.info("correlationID: " + json.getString("correlationId") + " - traceabilityId: " +
                        json.getString("traceabilityId"));
                try {
                    JSONArray response = new JSONArray(json.getJSONArray("response"));
                    for (int i = 0; i < response.length(); i++) {
                        JSONObject responseObject = response.getJSONObject(i);
                        System.out.print("Este es la URL " + responseObject.getString("url") + "\t ");
                        System.out.println("Este es el score " + responseObject.getString("score"));
                        score.add(Double.parseDouble(responseObject.getString("score")));
                    }
                    flag = false;
                    break;
                } catch (Exception e) {
                    System.out.println("Mensaje o estructura incorrecta " + e.toString());
                    e.printStackTrace();
                }
            }
        }
        consumer.close();

        return score;
    }
}
