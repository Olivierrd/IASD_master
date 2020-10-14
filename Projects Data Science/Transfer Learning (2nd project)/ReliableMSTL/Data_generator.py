__author__ = ""

"""
	Description:
		A gaussian and uniform generator 
"""

from config import *

def gaussian_generator(exp_params):
    
    def f_labeled(x) : 
      w_0_T = np.ones((1,10)) # np.zeros((1,10))
      delta = 0.1
      epsilon = np.random.randn()
      delta_w = np.random.randn(1,10)
      return np.sign(np.dot(w_0_T+delta*delta_w,x) + epsilon)

    k, n, d = exp_params["k"], exp_params["n"], exp_params["d"]
    X_source, Y_source, source_labeled_indices = [], [], []

    X_target_train = np.random.randn(n, d)
    X_target_test = np.random.randn(n,d)

    Y_target_test = np.array([f_labeled(j) for j in X_target_test]).reshape(-1, 1)

    mu_t = np.mean(X_target_test) #mean of the target domain !
    sigma= 1
    p = [0.00001, 0.0001, 0.002, 0.0005, 0.001]

    for i in range(k):
        delta_mu = np.random.rand(n,d)
        mu = mu_t + p[i]*delta_mu
        X_source.append(np.random.randn(n,d)*sigma+mu)
        Y_source.append(np.array([f_labeled(j) for j in X_source[i]]).reshape(-1, 1))
        source_labeled_indices.append(np.random.choice(range(X_source[i].shape[0]), int(n/2), replace=False))
      
    return source_labeled_indices, X_source, Y_source, X_target_train, X_target_test, Y_target_test


def uniform_generator(exp_params) :
    # k sources, each with n instances with d dimensions    
    k, n, d = exp_params["k"], exp_params["n"], exp_params["d"]
    X_source, Y_source, source_labeled_indices = [], [], []
    for i in range(k):
        X_source.append(np.random.rand(n,d))
        Y_source.append(np.random.choice([-1, 1], n).reshape(-1, 1))
        source_labeled_indices .append(np.random.choice(range(X_source[i].shape[0]), int(n/2), replace=False))
    X_target_train = np.random.rand(n, d)
    X_target_test, Y_target_test = np.random.rand(n,d), np.random.choice([-1, 1], n).reshape(-1, 1)
    return source_labeled_indices, X_source, Y_source, X_target_train, X_target_test, Y_target_test

