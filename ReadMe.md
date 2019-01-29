## Logogram [![Maintainability](https://api.codeclimate.com/v1/badges/2c913b1aab08348e7ad8/maintainability)](https://codeclimate.com/github/WinstonKamau/logogram/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/cba7836dc3fa470889fb63e824688f74)](https://www.codacy.com/app/WinstonKamau/logogram?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=WinstonKamau/logogram&amp;utm_campaign=Badge_Grade) [![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com) [![CircleCI](https://circleci.com/gh/WinstonKamau/logogram.svg?style=svg)](https://circleci.com/gh/WinstonKamau/logogram) [![Coverage Status](https://coveralls.io/repos/github/WinstonKamau/logogram/badge.svg)](https://coveralls.io/github/WinstonKamau/logogram)

Logogram is a simple API that is meant to help users memorize words and their meaining. The API allows users to store words together with their meaning in flashcards that they can retrieve easily. It can be useful for memorizing jargons of a particular field, or practising for your tests.

# Description

The Logogram application enables users to:
- Signup to the application and be able to retrieve, edit and delete their personal information from the site.
- Login and Logout of the application.
- View other users in the application.
- Create, Edit, Retrieve and Delete their own flashcard.
- Create, Edit, Retrieve and Delete a word within their own flashcards.
- Retrieve a list of all flashcards the user owns
- Retrieve a list of all words within a flashcard that the user owns.

## Documentation

| **URL EndPoint**          | **HTTP Method**| **Public Access** | **Summary**                            |
| ------------------------  | ---------------| ----------------- |----------------------------------------|
| /api/v1/users/            |     GET        |      True         | Retrieves all users on the Logogram App|
| /api/v1/users/            |     POST       |      True         | Create a new user on the Logogram App  |
| /api/v1/users/pk/         |     GET        |      False        | Retrieve a user's personal details     |
| /api/v1/users/pk/         |     PUT        |      False        | Edit a user's personal details         |
| /api/v1/users/pk/         |     DELETE     |      False        | Delete a user from the App             |
| /api/v1/flashcards/       |     GET        |      False        | Retrieve all flashcards of a user      |
| /api/v1/flashcards/       |     POST       |      False        | Create a new flashcard                 |
| /api/v1/flashcards/pk/    |     PUT        |      False        | Edit a specific flashcard              |
| /api/v1/flashcards/pk/    |     GET        |      False        | Retrieve a specific flashcard          |
| /api/v1/flashcards/pk/    |     DELETE     |      False        | Delete a specific flashcard            | 
| /api/v1/flashcards/pk/words/|     GET      |      False        | Retrieves all words of a flashcard     |
| /api/v1/flashcards/pk/words/|     POST     |      False        | Create a word on a flashcard           |
| /api/v1/flashcards/pk/words/pk/|     PUT   |      False        | Edit a specific word on a flashcard    | 
| /api/v1/flashcards/pk/words/pk/|  DELETE   |      False        | Delete a specific word on a flashcard  |
| /api/v1/flashcards/pk/words/pk/|  GET      |      False        | Retrieve a specific word on a flashcard|

## Setup

### Dependencies

This project uses the following technologies:

| **Version**     | **Packages/Languages/Frameworks**                              |
|-----------------|----------------------------------------------------------------|
|`3.7`            | [Python](https://www.python.org/downloads/release/python-370/) |
|`2018.10.13`     | [Pipenv](https://pypi.org/project/pipenv/2018.10.13/)          |
|`3.9.1`          | [Django Rest Framework](https://www.django-rest-framework.org/)|
|`2.1.5`          | [Django](https://www.djangoproject.com/)                       |


Other application dependencies can be found [here](Pipfile)

### Getting Started

#### Clone this repository, and change directory into the logogram folder
    git clone https://github.com/WinstonKamau/logogram.git
    cd logogram
#### Install application dependencies
    pipenv --three install -d
#### Migrate the application
    pipenv run src/logogram/manage.py migrate
#### Run the Service
    pipenv run src/logogram/manage.py runserver

## Testing

#### Run tests
    cd src/logogram
    pipenv run python manage.py test
#### Run tests with coverage
    cd src/logogram
    pipenv run coverage run --rcfile=../../.coveragerc manage.py test
    pipenv run coverage report --rcfile=../../.coveragerc
