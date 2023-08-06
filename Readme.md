# Corider-CRUD Flask Application


### This is a backend API written in Flask for a Corider-CRUD application. The application allows you to perform CRUD operations (Create, Read, Update, Delete) on a  resource using HTTP requests.

Python version: 3.8

1. SETUP & INSTALLATION

Make sure you have the said Python version installed.
```
git clone <repo-url>
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
Running The App
```
python app.py
```
Viewing The App

Go to ```http://127.0.0.1:5000``` or ```http://localhost:5000```.


2. USING DOCKER:

How to pull the docker image:
```
$ docker pull swimming9acadia/corider
```
Build the image using the following command:
```
$ docker build -t swimming9acadia/corider .
```
Run the Docker container using the command shown below:
```
$ docker run -d -p 5000:5000 swimming9acadia/corider
```
