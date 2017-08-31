:; tail -n +2 .commands.sh; exit
#
git add --all
git commit --allow-empty --allow-empty-message -m ''
git commit --allow-empty --allow-empty-message -m '' --amend
git push origin master
#
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
#
pipenv install
pipenv install requests
pipenv run python main/worker.py
pipenv shell
#
git all && git cam && git pom -f
git all && git com && git pom
