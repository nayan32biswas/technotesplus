#!/bin/sh

Green="\033[0;32m"
Red="\033[0;31m"
Color_Off="\033[0m"

FILE=.env
if [ ! -f "$FILE" ]; then
    echo "\n${Red}$FILE does not exist. Please create $FILE file and assign documented variables${Color_Off}\n"
    exit
fi

docker-compose build api

cd ./frontend/
yarn install
VUE_APP_DEVHOST=http://localhost:8000 yarn build
echo "\n\n${Green}Build Successfully${Color_Off}"

mkdir -p ../server/static
cp -r dist/ ../server/static/
echo "${Green}Copy frontend build file${Color_Off}"

cd -

docker-compose up api worker -d

echo "\n\nVisit: ${Green}localhost:8000${Color_Off}"
