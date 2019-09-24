
exit

git add --all
git commit --allow-empty --allow-empty-message -m ''
git commit --allow-empty --allow-empty-message -m '' --amend
git push origin master

heroku config:add name=
heroku local
heroku local web
heroku local worker
heroku logs
heroku logs --source app
heroku logs --source heroku
heroku open
heroku ps
heroku run bash

pipenv install
pipenv install requests
pipenv run python main/worker.py
pipenv shell

git all && git cam && git pom -f
git all && git com && git pom

git clone https://github.com/heroku/python-getting-started.git
cd python-getting-started

python3 -m venv getting-started
pip install -r requirements.txt

createdb python_getting_started

python manage.py migrate
python manage.py collectstatic

heroku local
