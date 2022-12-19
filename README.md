# Misnomers
Misnomers was a project created by my friend Dawson and I for [HackKU 2021](https://hackku-2021.devpost.com/). The goal of our project was to create a easy-to-use, minimalist website and application programming interface (API) for generating unique fantastical character names using machine learning.

# Table of Contents
* [Usage](#usage)
* [Origin Story](#origin-story)
* [How It Works](#how-it-works)
    * [Training The Model](#training-the-model)
    * [The Web App](#the-web-app)
    * [Hosting](#hosting)

# Usage
Unfortunately, the website is no longer being hosted on the internet. Apologies!

You can view the Misnomers website [here](https://misnomers.herokuapp.com/). The API can also be called directly by sending a `GET` request to https://misnomers.herokuapp.com/api. The expected response is an array of JSON objects, similar to the following.
```
[{"name":"Anher"},{"name":"Uanne"},{"name":"Ildyn"},{"name":"Ysi"},{"name":"Hilyng"}]
```
It should be noted that the API can be slow at times, so please be patient with it.

# Origin Story
Misnomers came to be after Dawson and I tried and failed to create a baby name generator using the same techniques Misnomers uses now. When looking at some of the potential "baby names", inspiration struck us! These names weren't for human babies, but children of our minds. These would be perfect names for [Dungeons and Dragons](https://en.wikipedia.org/wiki/Dungeons_%26_Dragons) characters! The rest is history.

# How It Works

## Training The Model
The first step was to train the model which would serve names to the website. To do this, we used [Keras](https://keras.io/) to create a recurrent neural network (RNN). The code which does this is located in the `model_train` folder. After the model is trained, it is stored in the `namegen-300.hdf5` file.

## The Web App

Misnomers is a [Flask](https://flask.palletsprojects.com/en/2.0.x/) web app. The app (`app.py`) hosts an API which the web frontend calls upon to be served names from the model. It calls the API everytime the page is loaded so new, unique names are shown every time. The `gen.py` script provides a `Model` class which allows the web app to interface with the model and get names for the API.

## Hosting

Misnomers is hosted on [Heroku](https://www.heroku.com/). The `requirements.txt` file specifies what Python packages Heroku will need to download to deploy Misnomers. `Procfile` specifies that the `gunicorn` web server is to be used when hosting the app on Heroku.
