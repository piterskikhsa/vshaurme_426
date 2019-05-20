#!/bin/bash

cd ~/vshaurme/
git pull
. ~/vshaurme/venv/bin/activate

pip install -r requirements.txt
pybabel compile -d vshaurme/translations
touch /var/www/www_vshaurme_su_wsgi.py
echo "Deployed at $(date)" >> deploy.txt
