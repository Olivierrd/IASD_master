import os
import models

# Some constants paths
DIR_BASE = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(DIR_BASE, 'data')
MODELS = os.path.join(DIR_BASE, 'models')

# To be modified if you want to load or train the model, if True, will train a model
TRAIN_standard_model = False
TRAIN_robust_model = False
TRAIN_large_robust_model = False

# To visualize results on image samples of models and accuracy, set to True
VIZ = False

# Paths of already trained model, to be modified as pleased
STANDARD_trained_model = os.path.join(MODELS, 'standard_model_78acc.h5')
ROBUST_trained_model = os.path.join(MODELS, 'robust_model_over_colab.h5')
LARGE_ROBUST_trained_model = os.path.join(MODELS, 'robust_model_over_rand_colab.h5')
BEST_ROBUST_trained_model = os.path.join(MODELS, 'new_robust_model2_over_colab.h5')

# Attacks configuration
# Will load attacked data if False
MAKE_ATTACK = False
ROBUST_MAKE_ATTACK = False
LARGE_ROBUST_MAKE_ATTACK = False

# Attack to perform (also used for adversarial training)
attack_style = 'PGD'  # 'PGD' or 'FGSM' or 'Carlini_Inf' or 'Deep_Fool' or 'Newton_Fool' or 'Basic_Iterative_Method'

# All Attacks parameters
# FGSM parameters
FGSM_attack_delta = 0.03

# PGD parameters (also used for adversarial training)
PGD_attack_delta = 0.03
PGD_attack_epsilon = 0.05
PGD_attack_nb_iter = 3

# Carlini_Inf parameters
CInf_eps = 0.03
CInf_max_iter = 40
CInf_learning_rate = 0.01

# Deep_Fool parameters
DFool_max_iter = 4
DFool_epsilon = 0.03
DFool_nb_grads = 10
DFool_batch_size = 1

# Newton Fool parameters
NFool_max_iter = 40
NFool_eta = 0.03
NFool_batch_size = 1

# Basic Iterative Method parameters
BIter_eps = 0.03
BIter_eps_step = 0.01
BIter_max_iter = 1
BIter_targeted = False
BIter_batch_size = 1

# Paths of already attacked data (doesn't exist if you don't have already attacked data)
ROBUST_ATTACKED_TEST_FGSM = os.path.join(DATA, 'attack_robust_over_test_FGSM_003.npy')
ROBUST_ATTACKED_TEST_PGD3iter = os.path.join(DATA, 'attack_robust_over_test_PGD0008_3iter.npy')
ROBUST_ATTACKED_TEST_PGD5iter = os.path.join(DATA, 'attack_robust_over_test_PGD0008_5iter.npy')
ATTACKED_TEST_PGD = os.path.join(DATA, 'attack_test_PGD_iter5_0008.npy')
ATTACKED_TEST_FGSM = os.path.join(DATA, 'x_test_attacked_FGSM_0_03.npy')
ATTACKED_TEST_CInf = os.path.join(DATA, 'CarliniLinf_23_acc_xtest.npy')
ATTACKED_TEST_CInf2 = os.path.join(DATA, 'CarliniLinf_12_acc_xtest.npy')
ATTACKED_TEST_NFool = os.path.join(DATA, 'newtonfool_12.3_acc_xtest.npy')
ATTACKED_TEST_BIter = os.path.join(DATA, 'BasicIterativeMethod_10.09_acc_xtest.npy')
LARGE_ROBUST_ATTACKED_TEST_FGSM = os.path.join(DATA, 'attack_robust_over_rand_test_FGSM003.npy')
LARGE_ROBUST_ATTACKED_TEST_PGD = os.path.join(DATA, 'attack_robust_over_rand_test_PGD0008_5iter.npy')
BEST_ROBUST_ATTACKED_TEST_PGD = os.path.join(DATA, 'attack_new_robust_model2_over_colabPGD0005_5iter.npy')
BEST_ROBUST_ATTACKED_TEST_FGSM = os.path.join(DATA, 'attack_new_robust_model2_over_colabFGSM003.npy')

# Configuration of models if training (to be modified as pleased)
config_standard_model = models.ModelConfig(
    conv_layers=[(256, 3), (256, 3), (256, 3)],
    epochs=100,
    batch_size=128,
    validation_split=0.1,
    nb_neurons_on_1st_FC_layer=32,
    lr=0.01
)

config_robust_model = models.ModelConfig(
    conv_layers=[(256, 3), (256, 3), (256, 3)],
    epochs=100,
    step_per_epoch=20,
    batch_size=128,
    validation_split=0.1,
    validation_steps=1,
    nb_neurons_on_1st_FC_layer=32,
    lr=0.01
)

config_large_robust_model = models.ModelConfig(
    conv_layers=[(256, 3), (256, 3), (256, 3)],
    epochs=100,
    step_per_epoch=20,
    batch_size=128,
    validation_split=0.1,
    validation_steps=1,
    nb_neurons_on_1st_FC_layer=32,
    lr=0.01
)

# constants labels of CIFAR10 to make some visualization
class_to_name = {
    0: "plane",
    1: "car",
    2: "bird",
    3: "cat",
    4: "deer",
    5: "dog",
    6: "frog",
    7: "horse",
    8: "ship",
    9: "truck"
}
