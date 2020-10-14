# Deep Learning

## Course

Introduction to Deep Learning. Deep Learning enable to train neural network with many layers so as to address various 
difficult problems. Applications range from image to games. In this course we will present Stochastic Gradient Descent 
for deep neural networks using different architectures (convolutions, dense, recurrent, residual). We will use 
Keras/Tensorflow and/or Pytorch and apply them to games and optimization.

## Project 

This is the page for the Deep Learning Project of the master IASD. The goal is to train a network for playing the game 
of Go. In order to be fair about training ressources the number of parameters for the networks you submit must be lower
than 1 000 000. The maximum number of students per team is two. The data used for training comes from Facebook ELF 
opengo Go program self played games. There are more than 109 000 000 different states in total in the training set. 
The input data is composed of 8 19x19 planes (color to play, ladders, current state on two planes, two previous states 
on four planes). The output targets are the policy (a vector of size 361 with 1.0 for the move played, 0.0 for the other
 moves), the value (1.0 if White won, 0.0 if Black won) and the state at the end of the game (two planes).

This [address](https://www.lamsade.dauphine.fr/~cazenave/DeepLearningProject.html?fbclid=IwAR2zGDBPyA9GSeJ6iNgz5Jv6UWVFJEfY6PRLUTXZun6Vf6r2eNEONLjGqgU
) describes the Deep Learning Project.

This project obtains the grade 12/20 and it has been done with the collaboration of [Maxime Talarmain](https://www.linkedin.com/in/maxime-talarmain-58aa99165).
