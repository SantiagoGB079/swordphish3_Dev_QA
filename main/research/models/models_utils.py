import os
import joblib
import string
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
NEW_FILE = False

def split_data_for_training(data, output_column='label', test_size=0.3):
    data.reset_index(drop=True, inplace=True)
    # Split data into train/test.
    y = data[output_column]
    data_train, data_test = train_test_split(data, stratify=y, test_size=test_size, random_state=22)
    return data_train, data_test


def input_output_split(data, output_column='label'):
    y = np.array(data.label)
    x = data.drop([output_column], axis=1)
    return x, y


def input_preprocessing(x, features_type):
    if features_type == 'soc':
        x = x.drop(['url'], axis=1).to_numpy()
    elif features_type == 'nlp':
        X = x['url'].to_list()
        # Define vocabulary
        vocabulary = get_vocabulary()
        # Creating a mapping from unique characters to indices
        char2index = {u: i for i, u in enumerate(vocabulary)}
        index2char = np.array(vocabulary)
        max_url_size = 40
        X_sequences = []
        # Iterate over urls
        for url in X:
            # Translate text in URL to indices (0 if char is not in vocabulary)
            temp_text_as_int = np.array([char2index[c] if c in vocabulary else 0 for c in url])
            if len(temp_text_as_int) > max_url_size:
                temp_text_as_int = temp_text_as_int[:max_url_size]
            else:
                temp_text_as_int = np.pad(temp_text_as_int, pad_width=(0, max_url_size - len(temp_text_as_int)),
                                          mode='constant')
            X_sequences.append(temp_text_as_int)
        # Replace original data by sequences.
        x = np.array(X_sequences)
    elif features_type == 'soc+nlp':
        soc = input_preprocessing(x, features_type='soc')
        nlp = input_preprocessing(x, features_type='nlp')
        x = [soc, nlp]
    else:
        raise SystemExit('Features Type {} has not been implemented yet.'.format(features_type))
    return x


def get_vocabulary():
    vocabulary = sorted(set(string.printable))
    return vocabulary


def get_embedding_size():
    embbeding_size = 8
    return embbeding_size


def compute_class_weight(y):
    y = np.array(y)
    class_weights = dict()
    labels = np.unique(y)
    for label in labels:
        class_weights[label] = y.size / (labels.size * y[y == label].size)
    return class_weights


def clean_data_for_training(data, features_type, output_column='label'):
    if features_type == 'soc':
        data = data.drop(['url'], axis=1)
    elif features_type == 'nlp':
        data = data[['url', output_column]]
    elif features_type == 'soc+nlp':
        data = data
    else:
        raise SystemExit('Features Type {} has not been implemented yet.'.format(features_type))
    data.reset_index(drop=True, inplace=True)
    return data


def save_model(model, target_folder, target_name, model_type, features_type):
    # Check what kind of model is being saved.
    if type(model).__name__ in ['Sequential', 'Functional']:  # Check if model was trained using TensorFlow.
        model_extension = 'h5'
    else:
        model_extension = 'joblib'

    # Define name of the model to save in disk.
    number = 1
    boolean = True
    while boolean:
        model_name = os.path.join(target_folder,
                                  'swordphish3_{}_{}_{}_model_v{}.{}'.format(model_type, target_name, features_type,
                                                                             number, model_extension))
        if not os.path.isfile(model_name) or not NEW_FILE:
            boolean = False
        else:
            number += 1
    # Save model.
    if model_extension == 'h5':
        tf.keras.models.save_model(model, model_name, save_format='h5')
    elif model_extension == 'joblib':
        joblib.dump(model, model_name)
    else:
        raise SystemExit('Type of model {} has not been implemented yet.'.format(type(model).__name__))
    return model_name


def load_model(filepath):
    if '.h5' in filepath:
        model = tf.keras.models.load_model(filepath=filepath)
    elif '.joblib' in filepath:
        model = joblib.load(filename=filepath)
    else:
        raise SystemExit('Models with extension {} are not supported yet.'.format(filepath.split('.')[-1]))
    return model


def log_training_setup(logfile_path, dataset_name, model_path, re_process_raw, re_make_dataset):
    # Log training information into file.
    logfile = open(logfile_path, "w+")
    logfile.write("Dataset name: {}\n"
                  "Model name: {}\n"
                  "Re-Create Features: {}\n"
                  "Re-Make Dataset: {}\n"
                  "\n"
                  .format(dataset_name, model_path, re_process_raw, re_make_dataset,
                          ))
    return logfile
