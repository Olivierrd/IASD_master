__author__ = "Zirui Wang"

"""
	Description:
		A simple simulator to demonstrate how to use PW-MSTL method
		experiment parameters can be tuned below
"""

from config import *
from Data_generator import gaussian_generator, uniform_generator

def MultiSouece_Transfer_Learning_Simulator(exp_params):
    accuracy = []
    for j in range(30) :

      if exp_params["generator"] == "gaussian" :
        source_labeled_indices, X_source, Y_source, X_target_train, X_target_test, Y_target_test = gaussian_generator(exp_params)
      
      elif exp_params["generator"] == "uniform" :
        source_labeled_indices, X_source, Y_source, X_target_train, X_target_test, Y_target_test = uniform_generator(exp_params)

      # Initialize the model with model parameters
      params = exp_params2model_params(exp_params)
      model = ReliableMultiSourceModel(X_source, Y_source, X_target_train, source_labeled_indices, params)
      model.train_models(exp_params["base_model"])

      Y_predicted = []
      for i in range(X_target_test.shape[0]):
          Y_predicted.append(model.multi_source_classify_PWMSTL(X_target_test[i].reshape(1, -1)))
      #print("Accuracy: ", accuracy_score(Y_predicted, Y_target_test))
      accuracy.append(accuracy_score(Y_predicted, Y_target_test))
    print(np.mean(accuracy))

# Experimental Parameters
if __name__ == '__main__':
    exp_params = {}
    # Core parameters required for PW-MSTL
    exp_params["start_mode"] = "warm"
    exp_params["b1"] = 1.0
    exp_params["tau_lambda"] = 1.0
    exp_params["rho"] = 1.0
    exp_params["beta_1"] = 10.0
    exp_params["beta_2"] = 10.0
    exp_params["mu"] = 0.1
    exp_params["max_alpha"] = 10.0

    # Dummy parameters
    exp_params["AL_method"] = "DUMMY"
    exp_params["base_model"] = "svm"

    # Experiment specific parameters
    exp_params["k"] = 5 #10
    exp_params["n"] = 100
    exp_params["d"] = 10
    exp_params["generator"] = "gaussian"

    MultiSouece_Transfer_Learning_Simulator(exp_params)
