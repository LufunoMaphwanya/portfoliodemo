#  Portfolio demo
Create a portfolio app where users can register and see other users in network and their locations and profiles
<br>

#### Prerequisites:
1. python3<br />
1. virtualenv or similar<br />


1. [Initial set up](#set-up)<br>
2. [Running tests](#run-tests)<br>
3. [Running app](#run-app)<br><br>

## Set up
Clone project

```bash
git clone git@github.com:LufunoMaphwanya/portfoliodemo.git
cd portfoliodemo
```

Create virtual environment 
```bash
virtualenv venv
source venv/bin/activate
```


install requirements
```bash
pip install -r requirements.txt
```


Run Migrations
```bash
python manage.py migrate
```

OR from scratch: delete all migrations in migrations folder(s)
```bash
python manage.py makemigrations
python manage.py migrate
```



## Run tests

```bash
python manage.py test --verbosity=2
```


## Run app

```bash
python manage.py runserver
```

it should be available http://localhost:8000


<hr />
* Note:
Openstreet maps doesn't allow multi-pins ( or at least I could not find it, so one has to click on an account in network to see their location)