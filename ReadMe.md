## Logogram [![Maintainability](https://api.codeclimate.com/v1/badges/2c913b1aab08348e7ad8/maintainability)](https://codeclimate.com/github/WinstonKamau/logogram/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/cba7836dc3fa470889fb63e824688f74)](https://www.codacy.com/app/WinstonKamau/logogram?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=WinstonKamau/logogram&amp;utm_campaign=Badge_Grade) [![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com) [![CircleCI](https://circleci.com/gh/WinstonKamau/logogram.svg?style=svg)](https://circleci.com/gh/WinstonKamau/logogram)

An application that aids its users memorise information

# Description

3-5 sentences describing the code and what it's purpose is

## Documentation

List of endpoints exposed by the service

## Setup

Step by step instructions on how to get the code setup locally. This may include:

### Dependencies

* This project uses the following technologies:
- Python - `3.7.0`
- virtualenv - `16.0.0`
* Application dependencies can be found [here](src/requirements.txt)

### Getting Started

1. Clone this repository, and change directory into the src folder(this folder contains the code for the application): 

```
git clone https://github.com/WinstonKamau/logogram.git
cd logogram/src
```
2. Create a virtual environment and install the dependencies needed for the application.
```
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Migrate the application
```
cd src/logogram
python manage.py migrate
```
4. Run the development server
```
cd src/logogram
python manage.py runserver
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