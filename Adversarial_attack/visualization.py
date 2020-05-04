import constants as cst

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import random


def show_data(x, y):
    plt.figure(figsize=(16, 8))
    for i in range(0, 18):
        index = random.randint(0, 50000)
        plt.subplot(3, 6, i + 1)
        plt.imshow(x[index], cmap="gray")
        plt.text(0, 2, s=f"label={cst.class_to_name[np.argmax(y[index])]}",
                 bbox=dict(facecolor='blue', alpha=0.9),
                 color="white")
        plt.axis("off")
    plt.show()


def show_one_image(x, y, index):
    plt.imshow(x[index], cmap="gray")
    plt.text(0, 2, s=f"label={cst.class_to_name[np.argmax(y[index])]}",
             bbox=dict(facecolor='blue', alpha=0.9),
             color="white")
    plt.axis("off")


def show_dataset_and_predictions(x, y, model):
    plt.figure(figsize=(16, 8))
    prediction = model.predict(x)
    acc = 0
    for i in range(len(prediction)):
        if np.argmax(prediction[i]) == np.argmax(y[i]):
            acc += 1
    acc = acc / len(prediction)
    text = str(round(acc * 100, 2)) + "%"
    print('The model performs ' + text + ' of accuracy on this data, here is a sample')
    for i in range(0, 18):
        plt.subplot(3, 6, i + 1)
        plt.imshow(x[i], cmap="gray")
        plt.text(0, 2, s=f"y_true={cst.class_to_name[np.argmax(y[i])]}",
                 bbox=dict(facecolor='blue', alpha=0.9),
                 color="white")

        prediction = model.predict(np.expand_dims(x[i], 0))
        prediction = np.argmax(prediction)

        color = "green" if prediction == np.argmax(y[i]) else "red"

        plt.text(0, 26, s=f"y_pred={cst.class_to_name[prediction]}",
                 bbox=dict(facecolor=color, alpha=0.9),
                 color="white")

        plt.axis("off")
    plt.show()
    return text


def preprocess_image_and_label(input_image, input_label):
    """
    preprocess one image and its label to visualize the noise created by the attack
    :param input_image: one element of x_train
    :param input_label: its label
    :return: processed image and label
    """
    image = tf.cast(input_image, tf.float32)
    image = image[None, ...]
    label = tf.reshape(input_label, (1, input_label.shape[-1]))
    return image, label


def create_adversarial_pattern(input_image, input_label, model):
    input_image, input_label = preprocess_image_and_label(input_image, input_label)
    loss_object = tf.keras.losses.CategoricalCrossentropy()
    with tf.GradientTape() as g:
        g.watch(input_image)
        prediction = model(input_image)
        loss = loss_object(input_label, prediction)

    # Get the gradients of the loss w.r.t to the input image.
    gradient = g.gradient(loss, input_image)
    # Get the sign of the gradients to create the perturbation
    signed_grad = tf.sign(gradient)
    return signed_grad


def show_noise(input_image, input_label, model):
    perturbations = create_adversarial_pattern(input_image, input_label, model)
    plt.imshow(perturbations[0])


def display_images(input_image, input_label, description, model):
    "input_image, _ = preprocess_image_and_label(input_image, input_label)"
    good_class = np.argmax(model(input_image))
    confidence = float(model(input_image)[:, good_class])
    label = cst.class_to_name[np.argmax(model(input_image))]
    plt.figure()
    plt.imshow(input_image[0])
    plt.title('{} \n {} : {:.2f}% Confidence'.format(description, label, confidence * 100))
    plt.show()


def show_FGSM_attack_effect(input_image, input_label, perturbations, model):
    epsilons = [0, 0.01, 0.03, 0.045, 0.06, 0.1, 0.15]
    descriptions = [('Epsilon = {:0.3f}'.format(eps) if eps else 'Input')
                    for eps in epsilons]
    input_image, _ = preprocess_image_and_label(input_image, input_label)

    for i, eps in enumerate(epsilons):
        adv_x = input_image + eps * perturbations
        adv_x = tf.clip_by_value(adv_x, 0, 1)
        display_images(adv_x, input_label, descriptions[i], model)


def show_PGD_attack_effect(input_image, input_label, perturbations, nb_iter, model):
    epsilons = [0, 0.002, 0.005, 0.008, 0.01, 0.03, 0.045]
    descriptions = [('Epsilon = {:0.3f}'.format(eps) if eps else 'Input')
                    for eps in epsilons]
    input_image, _ = preprocess_image_and_label(input_image, input_label)

    print("with " + str(nb_iter) + " iterations")
    adv_x = input_image
    for i, eps in enumerate(epsilons):
        for iteration in range(nb_iter):
            adv_x = adv_x + eps * perturbations
            eta = tf.clip_by_value(adv_x - input_image, -eps, eps)
            adv_x = tf.clip_by_value(adv_x + eta, 0, 1)
        display_images(adv_x, input_label, descriptions[i], model)
