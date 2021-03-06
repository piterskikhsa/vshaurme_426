#!/bin/bash

cd ~/vshaurme/
git pull
. ~/vshaurme/venv/bin/activate

pip install -r requirements.txt
pybabel compile -d vshaurme/translations
flask getbadwords
flask db upgrade
touch /var/www/www_vshaurme_su_wsgi.py

REVISION=`git log -n 1 --pretty=format:"%H"`
ENVIRONMENT=production

RESPONSE=`curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ROLLBAR_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION`

echo "Deployed at $(date) $REVISION $RESPONSE" >> deploy.txt
