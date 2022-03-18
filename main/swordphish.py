from main.research.data import data_utils
from main.research.models import models_utils, train_models

if __name__ == '__main__':
    features_type = "nlp"
    model_type = "dnn"
    dataset_name = "features_appgate_may2021_train"
    PROCESSED_DIRECTORY_PATH = "dataset"
    MODELS_DIRECTORY_PATH = "model"
    FILES_FORMAT = 'JSON'
    OUTPUT_COLUMN = 'label'
    print('\nTraining model...\n')
    train = data_utils.load_dataset(
        path='{}/{}'.format(PROCESSED_DIRECTORY_PATH, dataset_name),
        format=FILES_FORMAT)

    model, model_path = train_models.train_swordphish(data=train, output_column=OUTPUT_COLUMN,
                                                      model_type=model_type,
                                                      features_type=features_type,
                                                      model_folder=MODELS_DIRECTORY_PATH,
                                                      model_target_name=dataset_name,
                                                      )

