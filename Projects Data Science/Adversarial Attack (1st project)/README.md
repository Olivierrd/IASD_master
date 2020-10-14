# Adversarial Attack project

## Description

This project's goal is to try several adversarial attacks on CIFAR10 data and then try to do adversarial training. 

## Configuration

### Install dependancies

Make sure you have installed all necessary dependancies, I recommend to use a virtual environment. 
In this matter, a yml file  and requirements.txt file are available.
We recommend to use GPU to train in reasonable time. Tensorflow GPU is in the requirements, we let you install GPU drivers.
### Configuration of models and attacks

To configure the project, you have to modify constants.py file. 
In this file, you can choose to train or load model with different parameters. 
You can also try new attacks with different parameters. 

To load attacked data, make sure you have already launched attacks and set the paths to the attacked data in constants.py file


## Run the project

Once you have configured what you want, to run the project, simply execute main.py

## Visualize what was already done 

To visualize what was already done, you can open "Adversarial_Attacks_Project_Summary.ipynb". This notebook uses locally stored attacks,
if you want to visualize you attacks, you have to run attacks and modify paths in constants.py file.
A theoretical report (pdf) to explain what we have done is available inside the repo.