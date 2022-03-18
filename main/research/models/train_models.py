import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Embedding, Bidirectional, LSTM

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from main.research.models import models_utils


def train_swordphish(data, output_column, model_type, features_type, model_folder, model_target_name):
    # Prepare data for training
    x_train, y_train = models_utils.input_output_split(data=data, output_column=output_column)
    x_train = models_utils.input_preprocessing(x=x_train, features_type=features_type)

    # Estimate class weights for unbalanced datasets
    class_weights = models_utils.compute_class_weight(y=y_train)

    # Train model
    model = fit_model_on_data(x=x_train, y=y_train, class_weights=class_weights, model_type=model_type,
                              features_type=features_type)

    # Save model.
    model_path = models_utils.save_model(model=model, target_folder=model_folder, target_name=model_target_name,
                                         model_type=model_type, features_type=features_type)
    return model, model_path


def fit_model_on_data(x, y, class_weights, model_type, features_type):
    # Initialize model
    model = None
    if features_type == 'soc':
        # Initialize and fit model
        if model_type == 'logistic':
            model = LogisticRegression(C=1.1, max_iter=1000, n_jobs=-1, class_weight=class_weights)
            # Fit model.
            model.fit(x, y)
        elif model_type == 'svm':
            model = SVC(probability=True, class_weight=class_weights)
            # Fit model.
            model.fit(x, y)
        elif model_type == 'rf':
            model = RandomForestClassifier(n_estimators=150, bootstrap=True, n_jobs=-1, class_weight=class_weights)
            # Fit model.
            model.fit(x, y)
        elif model_type == 'dnn':
            model = tf.keras.models.Sequential()
            model.add(Dense(32, activation='relu', input_shape=(x.shape[1],)), )
            model.add(BatchNormalization())
            model.add(Dense(20, activation='relu'))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
            model.add(Dense(10, activation='relu'), )
            model.add(Dropout(0.2))
            model.add(Dense(1, activation='sigmoid'))

            # Compile model.
            model.compile(loss='binary_crossentropy', metrics=['accuracy'])

            # Fit model.
            model.fit(x, y, epochs=200, class_weight=class_weights, verbose=0)
        else:
            print('Type of model: {} is not implemented yet.'.format(model_type))
            exit()
    elif features_type == 'nlp':
        # Define model.
        vocabulary = models_utils.get_vocabulary()
        embedding_size = models_utils.get_embedding_size()
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Embedding(len(vocabulary), embedding_size, input_length=x.shape[-1]))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
        # Compile model.
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                      optimizer=tf.keras.optimizers.Adam(1e-4),
                      metrics=['accuracy'])

        # Fit model on data.
        model.fit(x, y, epochs=100,
                  validation_split=0.1,
                  class_weight=class_weights,
                  verbose=1,
                  )
    elif features_type in ['soc+nlp', 'nlp+soc']:
        # Define model parameters.
        vocabulary = models_utils.get_vocabulary()
        embedding_size = models_utils.get_embedding_size()

        # Define inputs
        soc_input = tf.keras.layers.Input(shape=(x[0].shape[-1],), name='soc_input')
        nlp_input = tf.keras.layers.Input(shape=(x[1].shape[-1],), name='nlp_input')

        # Feature extraction for soc.
        soc = Dense(32, activation='relu')(soc_input)
        soc = BatchNormalization()(soc)
        soc = Dense(24, activation='relu')(soc)
        soc = BatchNormalization()(soc)
        soc = Dropout(0.1)(soc)
        soc = Dense(16, activation='relu')(soc)

        # Feature extraction for nlp
        nlp = Embedding(input_dim=len(vocabulary), output_dim=embedding_size)(nlp_input)
        nlp = Bidirectional(LSTM(128))(nlp)
        nlp = Dense(64, activation='relu')(nlp)

        # Concatenation
        latent_features = tf.keras.layers.Concatenate()([soc, nlp])
        latent_features = Dense(32, activation='relu')(latent_features)
        latent_features = Dense(16, activation='relu')(latent_features)

        phishing = Dense(1, activation='sigmoid')(latent_features)

        model = tf.keras.Model(inputs=[soc_input, nlp_input], outputs=phishing)

        # Compile model.
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                      optimizer=tf.keras.optimizers.Adam(1e-4),
                      metrics=['accuracy'])

        print(model.summary())
        # Fit model on data.
        model.fit(x, y, epochs=100,
                  validation_split=0.1,
                  class_weight=class_weights,
                  verbose=1,
                  )
    else:
        print('Model architecture for {} is not implemented yet.'.format(features_type))
        exit()
    return model
