# Simple Beer API

## Install
- Clone with github: `$ git clone https://github.com/Zayah117/canpango-app.git`

*OR*

- Download and unzip files

## Setup
1. Setup a virtual environment for dependencies
	
	```
	$ virtualenv rest-api
	$ source rest-api/bin/activate
	```
	
	*If you're using Windows, the activate script will be inside 'Scripts' instead of 'bin'*
	```
	$ source rest-api/Scripts/activate
	```

2. Install libraries within virtual environment
	
	```
	$ pip install requests
	$ pip install flask
	$ pip install flask-restful
	$ pip install sqlalchemy
	```

3. Setup Sqlite database using Python (*Python 2.7.x*)
	
	In your app directory, run:
	```
	$ python database_setup.py
	```

	This should create `data.db` in your app directory.

## Using the app
1. `cd` to application directory

2. Run application with Python (*Python 2.7.x*)
	
	```
	$ python app.py
	```
	App will run at localhost on port 5000: `http://127.0.0.1:5000/`

3. Using curl to interact with the API
	
	**Users**

	Add a user: 
	```
	$ curl -X PUT http://localhost:5000/users -d "name=USERNAME&password=PASSWORD"
	```
	Get all users:
	```
	$ curl -X GET http://localhost:5000/users
	```

	**Beers**

	Add a beer:
	```
	$ curl -X PUT http://localhost:5000/beers -d "name=NAME&ibu=0&calories=0&abv=0.0&style=STYLE&brewery_location=LOCATION&username=USERNAME&password=PASSWORD"
	```
	View all beers:
	```
	$ curl -X GET http://localhost:5000/beers
	```
	View a specific beer based on id:
	```
	$ curl -X GET http://localhost:5000/beer/1
	```

	**Reviews**

	Add a review to a specific beer:
	```
	$ curl -X PUT http://localhost:5000/reviews/1 -d "aroma=0&appearance=0&taste=0&username=USERNAME&password=PASSWORD"
	```
	View all reviews for a specific beer:
	```
	$ curl -X GET http://localhost:5000/reviews/1
	```

4. Viewing API data in your browser
	
	Beers:

	`http://localhost:5000/beers`
	
	Specific Beer:
	
	`http://localhost:5000/beer/1`
	
	Users:
	
	`http://localhost:5000/users`
	
	Reviews for a beer:
	
	`http://localhost:5000/reviews/1`