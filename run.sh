#!/usr/bin/env bash

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
COLOR_OFF='\033[0m'

if [ "$EUID" -ne 0 ]
  then echo -e "${YELLOW}Please run operative framework as root${COLOR_OFF}"
  exit
fi

if ! [ -x "$(command -v mongod)" ]; then
  echo -e "${RED}Error:${COLOR_OFF} mongod is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v npm)" ]; then
  echo -e '${RED}Error:${COLOR_OFF} NPM is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v python)" ]; then
  echo -e '${RED}Error:${COLOR_OFF} python is not installed.' >&2
  exit 1
fi

echo -e "${YELLOW}Running operative framework HD...${COLOR_OFF}"
ps aux  |  grep -i "framework/app.py"  |  awk '{print $2}'  |  xargs sudo kill -9
ps aux  |  grep -i "mongod --auth"  |  awk '{print $2}'  |  xargs sudo kill -9
ps aux  |  grep -i "npm"  |  awk '{print $2}'  |  xargs sudo kill -9
mongod --auth >/dev/null &
echo y | npm --prefix 'client/' start &
python framework/app.py >/dev/null &
