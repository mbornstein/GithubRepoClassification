# Github Repository Classification

This repo contains our github repository classification project for the [informatiCup2017](https://github.com/InformatiCup/InformatiCup2017) challenge. You can find the PDF report [here](docs/report.pdf).

Also have alook at the notebooks:

* [Comparison of different Classification models](Classification Models.ipynb) 
* [Data Visualization](Data Visualization.ipynb)

## Requirements
* Python3
* Git must be installed and in system path

## Getting Started

The entry point of the program is ```main.py```. Running ```python3 main.py``` starts the test mode. This mode trains and validates different models. When given a file as parameter (e.g. ```python3 main.py data/valset_unclassified.txt```), the program classifies all repositories in that file and print the results to stdout.
Saving the trained model with pickle or joblib resulted a strange loss in accuracy when loading it again. That is why we fall to the solution of training the model at the start of the prediction phase.

In order to speed up the training, we provide a csv ([data/enriched_data.csv](data/enriched_data.csv)) with all feature data for the training dataset precalculated. Let the dataimporter import this csv file to avoid downloaded 20GB of repositories.

## Categories

| Label   | short description                                                                                                          |
|---------|----------------------------------------------------------------------------------------------------------------------------|
| DEV​     | a repository primarily used for development of a tool, component, application, app, or API                                 |
| HW​ repo | a repository primarily used for homework, assignments and other course-related work and code                               |
| EDU​     | a repository primarily used to host tutorials, lectures, educational information and code related to teaching              |
| DOCS​    | a repository primarily used for tracking and storage of non-educational documents                                          |
| WEB​     | a repository primarily used to host static personal websites or blogs                                                      |
| DATA​    | a repository primarily used to store data sets                                                                             |
| OTHER​   | use this category only if there is no strong correlation to any other repository category, for example, empty repositories |
