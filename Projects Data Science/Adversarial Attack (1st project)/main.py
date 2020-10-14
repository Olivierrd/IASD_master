from tensorflow.keras.models import load_model
import numpy as np

import constants as cst
import import_data
import models
import attack_function
import visualization

if __name__ == '__main__':
    # Load CIFAR10 data
    x_train, y_train, x_test, y_test = import_data.format_data()

    # Train or Load standard model (trained on not attacked data)
    if cst.TRAIN_standard_model:
        print("Training a new standard model")
        model = models.train_model(x_train, y_train, cst.config_standard_model, 'standard_model')
    else:
        print("Loading standard model")
        model = load_model(cst.STANDARD_trained_model)

    # Attack Data
    if cst.MAKE_ATTACK:
        print("Attacking data")
        x_test_attacked = attack_function.make_attack(x_test, y_test, model, 'x_test_attacked_FGSM_0_03', cst.attack_style)
    else:
        print("Load attacked data")
        x_test_attacked = np.load(cst.ATTACKED_TEST)

    if cst.VIZ:
        # Show the effect of the attack on model predictions
        print("On not attacked data, on the test data the model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test, y_test, model)
        print("On attacked data, on the test data the model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test_attacked, y_test, model)

    # Train or Load a robust model but only on attacked data
    if cst.TRAIN_robust_model:
        print("Training a new only attack robust model")
        robust_model = models.train_robust_model(x_train, y_train, cst.config_robust_model, 'robust_model')
    else:
        print("Loading robust standard model")
        robust_model = load_model(cst.ROBUST_trained_model)

    # Attack Data with robust model
    if cst.ROBUST_MAKE_ATTACK:
        print("Attacking data")
        x_test_attacked_robust = attack_function.make_attack(x_test, y_test, robust_model,
                                                             'robust_attack_test_PGD', cst.attack_style)
    else:
        print("Load attacked data")
        x_test_attacked_robust = np.load(cst.ROBUST_ATTACKED_TEST)

    if cst.VIZ:
        # Show the effect of adversarial learning
        print("On not attacked data, on the test data the robust model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test, y_test, robust_model)
        print("On attacked data, on the test data the robust model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test_attacked_robust, y_test, robust_model)

    # Train or Load a robust model on attacked data and not attacked data
    if cst.TRAIN_large_robust_model:
        print("Training a new only attack robust model")
        large_robust_model = models.train_large_robust_model(x_train, y_train, cst.config_large_robust_model,
                                                             'large_robust_model')
    else:
        print("Loading robust standard model")
        large_robust_model = load_model(cst.LARGE_ROBUST_trained_model)

    # Attack Data with robust model
    if cst.LARGE_ROBUST_MAKE_ATTACK:
        print("Attacking data")
        x_test_attacked_large_robust = attack_function.make_attack(x_test, y_test, robust_model,
                                                                   'large_robust_attack_test_PGD', cst.attack_style)
    else:
        print("Load attacked data")
        x_test_attacked_large_robust = np.load(cst.LARGE_ROBUST_ATTACKED_TEST_FGSM)

    if cst.VIZ:
        # Show the effect of adversarial learning on attacked and not attacked data
        print("On not attacked data, on the test data the robust model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test, y_test, large_robust_model)
        print("On attacked data, on the test data the robust model has an accuracy of:")
        visualization.show_dataset_and_predictions(x_test_attacked_large_robust, y_test, large_robust_model)
