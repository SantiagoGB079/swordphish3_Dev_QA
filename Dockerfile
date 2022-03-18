FROM python:3.9-slim AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV KAFKA_TOPIC_SWORDPHISH3 kafka:9092
ENV SUSCRIBE_TOPIC dms-swordphish-url
ENV PUBLISH_TOPIC dms-swordphish-url-score
ENV MODEL_PROCESS /model/swordphish3_dnn_features_appgate_may2021_train_nlp_model_v1.h5


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

#copy config
copy config/logging.yml /home/config/logging.yml

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY main/ main/
COPY model/ /model

# Run the executable
ENTRYPOINT ["python", "-m", "main"]
CMD ["10"]
