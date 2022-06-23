# Project2

## Perpose and Design
We hope to realize Sudoku, an interesting game in this project. I hope people who play our games can find happiness and sense of achievement in our games. We have register, login, logout, upload game, personal game records and rank functions in our Sukoku
game. 
In this game, only administrator can upload the game. Default administrator is "admin" and the password is "123456". When admin enter in
the game page, there is a upload button. Admin can upload the new game by input each number in each table, like a real Sudoku game, or,
admin can input a string with numbers separated by ','.
There is some string for testing.
"8,1,7,6,5,9,4,2,3,6,5,3,4,2,8,7,1,9,4,2,9,3,1,7,6,8,5,7,8,2,5,4,6,9,3,1,3,6,5,7,9,1,8,4,2,9,4,1,2,8,3,5,6,7,2,9,6,1,7,4,3,5,8,1,3,8,9,6,5,2,7,4,5,7,4,8,3,2,1,9,6"
The string has a total of 81 digits, and each of the nine digits is a row in the game for a total of nine rows.
## Architecture
```
.
├── forms.py
├── __init__.py
├── models.py
├── __pycache__
│   ├── forms.cpython-38.pyc
│   ├── __init__.cpython-38.pyc
│   ├── models.cpython-38.pyc
│   └── routes.cpython-38.pyc
├── routes.py
├── static
│   ├── avatar120220519144314.jpg
│   ├── avatar120220519144403.jpg
│   ├── avatar320220519023147.jpg
│   ├── bg2.jpg
│   ├── bg.png
│   ├── css
│   │   ├── bootstrap.min.css
│   │   ├── bootstrap.min.css.map
│   │   ├── game.css
│   │   ├── index.css
│   │   ├── introduction.css
│   │   ├── login.css
│   │   ├── personal.css
│   │   └── style.css
│   ├── default_head_pic.jpg
│   ├── js
│   │   ├── bootstrap.min.js
│   │   ├── game.js
│   │   ├── jquery-3.6.0.js
│   │   ├── jquery.js
│   │   ├── personal.js
│   │   └── upload.js
│   ├── sudoku1.jpg
│   └── sudoku.png
└── templates
    ├── base.html
    ├── game.html
    ├── index.html
    ├── introduction.html
    ├── login.html
    ├── personal.html
    ├── rank.html
    ├── register.html
    └── upload.html

5 directories, 39 files
```
We have the static directory, the templates directory, the __init__.py, the forms.py, the models.py and the routes.py.
In the static, there are Javascript code files, CSS code files and some picture sources.
In the templates, there are nine HTML files as templates for flask. And the init.py is used to initial the application. 
The forms.py is used to declare the form submission. The models.py is used to declare the structure of the database. 
Finally, the routes.py is the views file that is backend API of the flask project.

## Prerequisites
Requires python3, flask, venv, and sqlite
### install python3
`sudo apt install python3`

### install python virtual environment
`sudo apt-get install python-virtualenv`

### install pip
`sudo apt install python3-pip`

### install flask
`pip install Flask`

### install sqlite
`sudo apt-get install sqlite3`

## Getting Started
Clone the project from the github: `git clone git@github.com:Changhao029/Project2.git`

Enter the project directory: `cd cd Project2`

Create the python virtual environment: `python3 -m venv venv`

Activate the python virtual enviroment: `source ./venv/bin/activate`

Install all the requirements from the requirements.txt file: `pip install -r requirements.txt`

Initial the database: 

(For test we have uploaded a database file 'project2.db', so if you just want to run the project, you could skip this init to 'flask run')

`flask db init`

`flask db migrate -m "init"`

`flask db upgrade`

To run the app: `flask run`.

To stop the app: Use 'ctrl+ C'.

To exit the environment: `deactivate`

## Running the tests

### 1.Unit test
You will see three Flask instance named "app" in the `./app/__init__.py`, like:
```
app.config.from_object(Config)
# app.config.from_object(Test_Config)
# app.config.from_object(Test_Config_Unit)
```
You should change the code to this:

```
# app.config.from_object(Config)
# app.config.from_object(Test_Config)
app.config.from_object(Test_Config_Unit)
```
And run `python -m unittest testApp.py` in the project root directory. You will see:
```
..<WrapperTestResponse 95 bytes [200 OK]>
............
----------------------------------------------------------------------
Ran 14 tests in 4.399s

OK

```
If you want to see the coverage, you should run:`coverage report ./app/*.py`. You will see:
```
Name                Stmts   Miss  Cover
---------------------------------------
./app/__init__.py      47      5    89%
./app/forms.py         11      0   100%
./app/models.py        33      5    85%
./app/routes.py       243     34    86%
---------------------------------------
TOTAL                 334     44    87%

```

### 2.System test
set the code of `./app/__init__.py` like that
```
# app.config.from_object(Config)
app.config.from_object(Test_Config_Unit)
```
then run `python3 -m tests.systemtest` in the project root directory to run the selenium test, the result will show:
```
----------------------------------------------------------------------
Ran 1 test in 8.002s

OK
```
Then change the code of `./app/__init__.py` to:
```
app.config.from_object(Config)
# app.config.from_object(Test_Config_Unit)
```
and then run the app again.
## Contribution
We each contributed about 50% to the project.
### Changhao Liu contribution review
My partner and I are jointly responsible for the topic selection, design,  development and testing of this project. In the development stage, I was mainly responsible for the back-end code development of login registration and personal page, as well as the front-end code development of the game interface. In addition, my partner and I were responsible for the debugging and testing of the code together. In the testing step, I was mainly responsible for the unit test.

### Yinuo Zhao contribution review
I am mainly responsible for the front-end development of index, base, introduction, login, registration and personal page, as well as the back-end development of game uploading. Both of us participate in selecting topics, designing, debugging and testing the project. I mainly do the system test with selenium.



