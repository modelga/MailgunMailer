#!/bin/bash

echo "" >> /srv/logs/deploy.txt
date_time=`date +%Y_%m_%d-%H_%M`
echo $date_time >> /srv/logs/deploy.txt
cd /srv/app
git_before=`git rev-parse HEAD`
git pull >> /srv/logs/deploy.txt
git_after=`git rev-parse HEAD`

if [ "$git_before" != "$git_after" ]; then
    supervisorctl restart app >> /srv/logs/deploy.txt
    exit 0
fi

echo "Nothing changed" >> /srv/logs/deploy.txt
exit 0