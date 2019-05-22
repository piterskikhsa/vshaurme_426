#!/bin/bash

cd ~/vshaurme/
git pull
. ~/vshaurme/venv/bin/activate

pip install -r requirements.txt
pybabel compile -d vshaurme/translations
touch /var/www/www_vshaurme_su_wsgi.py
echo "Deployed at $(date)" >> deploy.txt

REVISION=`git log -n 1 --pretty=format:"%H"`
ENVIRONMENT=production

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$API_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \