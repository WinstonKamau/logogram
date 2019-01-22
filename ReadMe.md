## Logogram [![Maintainability](https://api.codeclimate.com/v1/badges/2c913b1aab08348e7ad8/maintainability)](https://codeclimate.com/github/WinstonKamau/logogram/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/cba7836dc3fa470889fb63e824688f74)](https://www.codacy.com/app/WinstonKamau/logogram?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=WinstonKamau/logogram&amp;utm_campaign=Badge_Grade) [![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com) [![CircleCI](https://circleci.com/gh/WinstonKamau/logogram.svg?style=svg)](https://circleci.com/gh/WinstonKamau/logogram) [![Coverage Status](https://coveralls.io/repos/github/WinstonKamau/logogram/badge.svg)](https://coveralls.io/github/WinstonKamau/logogram)

An application that aids its users memorise information

# Description

3-5 sentences describing the code and what it's purpose is

## Documentation

List of endpoints exposed by the service

## Setup

Step by step instructions on how to get the code setup locally. This may include:

### Dependencies

This project uses the following technologies:
* Python: `3.7.0`
* virtualenv: `16.0.0`

Application dependencies can be found [here](requirements.txt)

### Getting Started

#### Clone this repository, and change directory into the src folder(this folder contains the code for the application)
    ```
    git clone https://github.com/WinstonKamau/logogram.git
    cd logogram
    ```
#### Create a virtual environment and install the dependencies needed for the application for development
Install pipenv based on the instructions on this [link](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
    ```
    pipenv --three install -d
    ```
#### Migrate the application
    ```
    pipenv run src/logogram/manage.py migrate
    ```
#### Run the development server
    ```
    pipenv run src/logogram/manage.py runserver
    ```

#### Run tests
    ```
    pipenv run src/logogram/manage.py test
    ```
Using coverage
    ```
    pipenv run coverage run src/logogram/manage.py test
    pipenv run coverage report
    ```

### Run The Service

List of steps to run the service (e.g. docker commands)

### Microservices

List out the microservices if any that this repo uses

## Testing

Step by step instructions on how to run the tests so that the developer can be sure they've set up the code correctly

## Contribute

Any instructions needed to help others contribute to this repository

## Deployment

Step by step instructions so that the developer can understand how code gets updated
