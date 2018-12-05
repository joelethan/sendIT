# SendIT [![Build Status](https://travis-ci.org/joelethan/sendIT.svg?branch=Travis%2B_)](https://travis-ci.org/joelethan/sendIT) [![Maintainability](https://api.codeclimate.com/v1/badges/ceb2c8d5e078eb027d7d/maintainability)](https://codeclimate.com/github/joelethan/sendIT/maintainability) [![Coverage Status](https://coveralls.io/repos/github/joelethan/sendIT/badge.svg?branch=Travis%2B_)](https://coveralls.io/github/joelethan/sendIT?branch=Travis%2B_)
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

## Getting Started

 Clone the repository https://github.com/joelethan/sendIT

## Requirements

- Have Python 3.6.5 installed postgresql-9.5
- Have Postgresql-9.5.14 installed
- Have a virtual environment installed to separate the project's packages from the computer's packages
- Have Postman installed to test the API endpoints

## Installation
A step by step guide on how to setup and run the application. 

### Setting-up a database
```
Install Postgresql
Create a postgresql user called `postgres` with a password `postgres`
Access the postgres server through `pgAdmin` and create a production database `sendit` and a test database `test_db`

```

 Clone the repository by running the command in terminal or command line prompt
```
git clone https://github.com/joelethan/sendIT
```
 Change directory into the projects root by running
```
cd sendIT
```
 Checkout the `develop` branch
```
git checkout develop
```
 Create a virtual environment and activate it
```
virtualenv venv
```
```
.\venv\Scripts\activate
```

 Install project packages
```
pip install -r requirements.txt
```

 Check if packages are installed
```
pip freeze
```

 Run the API
```
python run.py
```

 Expected ouput
```
 * Serving Flask app "app.views" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 294-773-545
 * Running on http://127.0.0.1:5003/ (Press CTRL+C to quit)
```
### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
GET|/api/v1|Fetch Index page
POST|/auth/signup|Create a new User
POST|/auth/login|Login a User
POST|/api/v1/parcels|Create a Parcel delivery order
GET|/api/v1/parcels|Fetch all Parcel delivery orders
GET|/api/v1/parcels/`parcel_id`|Fetch a Parcel delivery order
PUT|/api/v1/parcels/`parcel_id`/destination|Update the distination of an Order
PUT|/api/v1/parcels/`parcel_id`/status|Update the status of an Order
PUT|/api/v1/parcels/`parcel_id`/presentLocation|Update the presentLocation of an Order


## Project link
Heroku: https://joelcamp14.herokuapp.com/api/v1/

## Author

Katusiime Joel Ian
