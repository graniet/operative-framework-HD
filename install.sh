#!/usr/bin/env bash

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
COLOR_OFF='\033[0m'

echo -e "${YELLOW}Welcome to operative framework HD installation script ${COLOR_OFF}"
echo -e "Making directory ${YELLOW}~/.operative_framework${COLOR_OFF} ..."
mkdir ~/.operative_framework
echo -e "Moving framework, client folder to '${YELLOW}~/.operative_framework${COLOR_OFF}' ..."
cp -R framework/ ~/.operative_framework/framework
cp -R client/ ~/.operative_framework/client
cp bin/opf_single.py /usr/local/bin/opf_single
echo -e "binary copied ${GREEN} /usr/local/bin/opf_single ${COLOR_OFF}"
cp bin/opf_importer.py /usr/local/bin/opf_importer
echo -e "binary copied ${GREEN} /usr/local/bin/opf_importer ${COLOR_OFF}"
cp bin/opf_users.py /usr/local/bin/opf_users
echo -e "binary copied ${GREEN} /usr/local/bin/opf_users ${COLOR_OFF}"
echo "operative framework binary copied."
echo -e "${YELLOW}installation${COLOR_OFF} of ${YELLOW}python${COLOR_OFF} dependency ..."
pip install -r requirements.txt
echo -e "${GREEN}Installation successfully terminated.${COLOR_OFF}"
echo -e "${GREEN}1) open new shell: sudo mongod --auth .${COLOR_OFF}"
echo -e "${GREEN}2) open new shell: sudo python framework/app.py .${COLOR_OFF}"
echo -e "${GREEN}3) open new shell: cd client/ && npm install && npm start .${COLOR_OFF}"