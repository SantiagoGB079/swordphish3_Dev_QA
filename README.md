# swordphish3

# Install requirements

Install docker (see instructions [here](https://docs.docker.com/engine/install/)):

Install docker compose (see instructions [here](https://docs.docker.com/compose/install/#install-compose)):

# Requirements ¡¡¡IMPORTANT!!!!

Set docker user:

    export USER_ID=$(id -u $USER) 
    export GROUP_ID=$(id -g $USER)


# Setup

Install dependencies

    docker-compose run pipenv install --dev

# Start process 

Command:

    docker-compose run pipenv run python -m main

# Kafka info

Look for 'kafka_information' key within configuration file (Ex: application-dev.yml) to get topics names:

    kafka_information:
        kafka_brokers: kafka:9092
        subscribe_topic: "input_topic"
        publish_topic: "output_topic"

Input message example:

    {
        "correlationId":"uuid",
        "traceabilityId":"uuid",
        "replyTo":"dtp.weblogs-service.1.reply.analyze-urls",
        "urls":[
            "url1",
            "url2",
            "..."
        ]
    }

Output message example:

    {
        "correlationId":"uuid",
        "traceabilityId":"uuid",
        "response":[
            {
                "url":"url1",
                "score":0.48
            },
            {
                "url":"url2",
                "score":0.83
            }
        ]
    }

# Some useful Kafka commands:

First use kafka container:

    docker-compose exec kafka ash

Send messages:
    
    echo '{"urls":["https:\/\/somesite.com"]}' | ./bin/kafka-console-producer.sh --bootstrap-server=localhost:9092 --topic=url

Listen messages from all topics:

    ./bin/kafka-console-consumer.sh --bootstrap-server=localhost:9092 --whitelist '.*'

# Training

Re-train by using:

    docker-compose run pipenv run python -m main.swordphish

See 'main/swordphish.py' how setting this process up

# Credits
This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
