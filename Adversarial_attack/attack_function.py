import constants as cst

import numpy as np
from tqdm import tqdm_notebook
import os
import tensorflow as tf
import random
from art.classifiers import KerasClassifier
from art.attacks import BasicIterativeMethod, CarliniLInfMethod, DeepFool, NewtonFool


def FGSM(x_test, y_test, delta, model):
    index = np.argmax(y_test)
    x = tf.constant(np.expand_dims(x_test, 0), dtype=tf.float32)
    y = tf.one_hot(index, 10)
    y = tf.reshape(y, (1, 10))

    with tf.GradientTape() as tape:
        tape.watch(x)
        prediction = model(x)
        loss_object = tf.keras.losses.CategoricalCrossentropy()
        loss = loss_object(y, prediction)
        gradient = tape.gradient(loss, x)
        signed_grad = tf.sign(gradient)
        x_attack = x + delta * np.squeeze(signed_grad, 0)
        x_attack = np.clip(x_attack, 0, 1)  # car on a des valeurs comprises entre 0 et 1 et non 255
    return np.reshape(x_attack, (32, 32, 3))


def PGD_infini(x_test, y_test, delta, epsilon, num_iter, model):
    index = np.argmax(y_test)
    x = tf.constant(np.expand_dims(x_test, 0), dtype=tf.float32)
    y = tf.one_hot(index, 10)
    y = tf.reshape(y, (1, 10))
    x_attack = x
    with tf.GradientTape() as g:
        g.watch(x)
        prediction = model(x)
        loss_func = tf.keras.losses.CategoricalCrossentropy()
        loss_value = loss_func(y, prediction)
        gradient = g.gradient(loss_value, x)
        signed_grad = np.sign(gradient)
        for i in range(num_iter):
            x_attack = x_attack + delta * signed_grad
            eta = tf.clip_by_value(x_attack - x, -epsilon, epsilon)
            x_attack = tf.clip_by_value(x_attack + eta, 0, 1)

    return np.reshape(x_attack, (32, 32, 3))


def carlini_inf(x_test, model, eps, max_iter, learning_rate):
    classifier = KerasClassifier(model=model, clip_values=(0, 1))
    attack_cw = CarliniLInfMethod(classifier=classifier, eps=eps, max_iter=max_iter, learning_rate=learning_rate)
    x_test_adv = attack_cw.generate(x_test)
    return np.reshape(x_test_adv, (32, 32, 3))


def deep_fool(x_test, model, max_iter, epsilon, nb_grads, batch_size):
    classifier = KerasClassifier(model=model, clip_values=(0, 1))
    attack_cw = DeepFool(classifier=classifier, max_iter=max_iter, epsilon=epsilon, nb_grads=nb_grads, batch_size=batch_size)
    x_test_adv = attack_cw.generate(x_test)
    return np.reshape(x_test_adv, (32, 32, 3))


def newton_fool(x_test, model, max_iter, eta, batch_size):
    classifier = KerasClassifier(model=model, clip_values=(0, 1))
    attack_cw = NewtonFool(classifier, max_iter=max_iter, eta=eta, batch_size=batch_size)
    x_test_adv = attack_cw.generate(x_test)
    return np.reshape(x_test_adv, (32, 32, 3))


def basic_iter(x_test, model, eps, eps_step, max_iter, targeted, batch_size):
    classifier = KerasClassifier(model=model, clip_values=(0, 1))
    attack_cw = BasicIterativeMethod(classifier=classifier, eps=eps, eps_step=eps_step, max_iter=max_iter, targeted=targeted, batch_size=batch_size)
    x_test_adv = attack_cw.generate(x_test)
    return np.reshape(x_test_adv, (32, 32, 3))


def make_attack(x, y, model, name, style='PGD'):
    if style == 'PGD':
        attacked_data = np.array(
            [PGD_infini(x[idx], y[idx], cst.PGD_attack_delta, cst.PGD_attack_epsilon, cst.PGD_attack_nb_iter, model) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    if style == 'FGSM':
        attacked_data = np.array(
            [FGSM(x[idx], y[idx], cst.FGSM_attack_delta, model) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    if style == 'Carlini_Inf':
        attacked_data = np.array(
            [carlini_inf(x[idx], model, cst.CInf_eps, cst.CInf_max_iter, cst.CInf_learning_rate) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    if style == 'Deep_Fool':
        attacked_data = np.array(
            [deep_fool(x[idx], model, cst.DFool_max_iter, cst.DFool_epsilon, cst.DFool_nb_grads, cst.DFool_batch_size) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    if style == 'Newton_Fool':
        attacked_data = np.array(
            [NewtonFool(x[idx], model, cst.NFool_max_iter, cst.NFool_eta, cst.NFool_batch_size) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    if style == 'Basic_Iterative_Method':
        attacked_data = np.array(
            [basic_iter(x[idx], model, cst.BIter_eps, cst.BIter_eps_step, cst.BIter_max_iter, cst.BIter_targeted, cst.BIter_batch_size) for idx in tqdm_notebook(range(len(x)))])
        np.save(os.path.join(cst.DATA, name), attacked_data)
    return attacked_data


def attack_gen(x_train, y_train, model, batch_size):
    while True:
        x = []
        y = []
        for batch in range(batch_size):
            index = random.randint(0, 49999)
            if cst.attack_style == "PGD":
                x.append(
                    PGD_infini(x_train[index], y_train[index], cst.PGD_attack_delta, cst.PGD_attack_epsilon, cst.PGD_attack_nb_iter,
                               model))
                y.append(y_train[index])
            if cst.attack_style == 'FGSM':
                x.append(FGSM(x_train[index], y_train[index], cst.FGSM_attack_delta, model))
                y.append(y_train[index])
        x = np.array(x)
        y = np.array(y)

        yield (x, y)


def attack_gen_rand(x_train, y_train, model, batch_size, attack_delta=0.003, attack_nb_iter=3, attack_style="FGSM"):
    while True:
        x = []
        y = []
        for batch in range(batch_size):
            index = random.randint(0, 49999)
            tresh = random.randint(0, 100)
            if tresh > 50:
                if attack_style == "PGD":
                    x.append(PGD_infini(x_train[index], y_train[index], attack_delta, attack_nb_iter, model))
                    y.append(y_train[index])
                if attack_style == 'FGSM':
                    x.append(FGSM(x_train[index], y_train[index], attack_delta, model))
                    y.append(y_train[index])
            else:
                x.append(x_train[index])
                y.append(y_train[index])
        x = np.array(x)
        y = np.array(y)

        yield (x, y)



