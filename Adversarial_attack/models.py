import attack_function as af
import numpy as np
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers
from tensorflow.keras.layers import Input, Dense, Lambda, Flatten, Reshape, \
    Conv2D, Conv2DTranspose, UpSampling2D, BatchNormalization, \
    LeakyReLU, Dropout, Softmax, MaxPool2D, AveragePooling2D, Activation
from tensorflow.keras.models import Model
import typing
import tensorflow as tf



class ModelConfig(typing.NamedTuple):
    conv_layers: typing.List
    epochs: int = 1
    step_per_epoch: int = 350
    batch_size: int = 128
    validation_split: float = 0.1
    validation_steps: int = 1
    nb_neurons_on_1st_FC_layer: int = 32
    lr: float = 0.01


def train_model(x_train, y_train, config, name):
    inp = Input(shape=(32, 32, 3))
    np.random.seed(38)
    tf.random.set_seed(38)
    x = Reshape((32, 32, 3))(inp)
    for filters, kernel_size in config.conv_layers:
        x = Conv2D(filters=filters, kernel_size=(kernel_size, kernel_size),
                   kernel_regularizer=regularizers.l2(0.001))(x)
        x = Activation("relu")(x)
        x = MaxPool2D((2, 2))(x)
    x = AveragePooling2D((2, 2))(x)
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(units=config.nb_neurons_on_1st_FC_layer, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(units=10)(x)
    x = Softmax()(x)
    model = Model(
        inputs=inp,
        outputs=x,
        name="lenet"
    )
    model.compile(
        loss='categorical_crossentropy',
        optimizer=tf.keras.optimizers.SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True),
        metrics=['accuracy']
    )

    model.summary()

    model.fit(x_train, y_train, batch_size=config.batch_size,
              epochs=config.epochs,
              validation_split=config.validation_split,
              # workers=4,
              verbose=1)

    saving_name = name + '.h5'
    model.save('models/' + saving_name)
    return model


def train_robust_model(x_train, y_train, config, name):
    inp = Input(shape=(32, 32, 3))
    np.random.seed(38)
    tf.random.set_seed(38)
    x = Reshape((32, 32, 3))(inp)
    for filters, kernel_size in config.conv_layers:
        x = Conv2D(filters=filters, kernel_size=(kernel_size, kernel_size),
                   kernel_regularizer=regularizers.l2(0.001))(x)
        x = Activation("relu")(x)
        x = MaxPool2D((2, 2))(x)
    x = AveragePooling2D((2, 2))(x)
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(units=config.nb_neurons_on_1st_FC_layer, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(units=10)(x)
    x = Softmax()(x)
    model = Model(
        inputs=inp,
        outputs=x,
        name="lenet"
    )
    model.compile(
        loss='categorical_crossentropy',
        optimizer=tf.keras.optimizers.SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True),
        metrics=['accuracy']
    )

    model.summary()

    train_gen = af.attack_gen(x_train, y_train, model, config.batch_size)
    size_val = int(config.validation_split*config.batch_size*config.step_per_epoch)
    val_gen = af.attack_gen(x_train, y_train, model, size_val)

    model.fit(train_gen,
              epochs=config.epochs,
              steps_per_epoch=config.step_per_epoch,
              validation_data=val_gen,
              validation_steps=config.validation_steps,
              verbose=1)

    saving_name = name + '.h5'
    model.save('models/' + saving_name)
    return model


def train_large_robust_model(x_train, y_train, config, name):
    inp = Input(shape=(32, 32, 3))
    np.random.seed(38)
    tf.random.set_seed(38)
    x = Reshape((32, 32, 3))(inp)
    for filters, kernel_size in config.conv_layers:
        x = Conv2D(filters=filters, kernel_size=(kernel_size, kernel_size),
                   kernel_regularizer=regularizers.l2(0.001))(x)
        x = Activation("relu")(x)
        x = MaxPool2D((2, 2))(x)
    x = AveragePooling2D((2, 2))(x)
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(units=config.nb_neurons_on_1st_FC_layer, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(units=10)(x)
    x = Softmax()(x)
    model = Model(
        inputs=inp,
        outputs=x,
        name="lenet"
    )
    model.compile(
        loss='categorical_crossentropy',
        optimizer=tf.keras.optimizers.SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True),
        metrics=['accuracy']
    )

    model.summary()

    train_gen = af.attack_gen_rand(x_train, y_train, model, config.batch_size)
    size_val = int(config.validation_split*config.batch_size*config.step_per_epoch)
    val_gen = af.attack_gen_rand(x_train, y_train, model, size_val)

    model.fit(train_gen,
              epochs=config.epochs,
              steps_per_epoch=config.step_per_epoch,
              validation_data=val_gen,
              validation_steps=config.validation_steps,
              verbose=1)

    saving_name = name + '.h5'
    model.save('models/' + saving_name)
    return model


