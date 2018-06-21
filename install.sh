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
cp bin/opf_client.py /usr/local/bin/opf_client
echo -e "binary copied ${GREEN} /usr/local/bin/opf_client ${COLOR_OFF}"
cp bin/opf_console.py /usr/local/bin/opf_console
echo -e "binary copied ${GREEN} /usr/local/bin/opf_console ${COLOR_OFF}"
cp bin/opf_server.py /usr/local/bin/opf_server
echo -e "binary copied ${GREEN} /usr/local/bin/opf_single ${COLOR_OFF}"
cp bin/opf_single.py /usr/local/bin/opf_single
echo -e "binary copied ${GREEN} /usr/local/bin/opf_server ${COLOR_OFF}"
cp bin/opf_users.py /usr/local/bin/opf_users
echo -e "binary copied ${GREEN} /usr/local/bin/opf_users ${COLOR_OFF}"
echo "operative framework binary copied."
echo -e "${YELLOW}installation${COLOR_OFF} of ${YELLOW}python${COLOR_OFF} dependency ..."
pip install -r requirements.txt
echo -e "${YELLOW}installation${COLOR_OFF} of ${YELLOW}react.js${COLOR_OFF} dependency ..."
npm install --prefix "~/.operative_framework/client/"
echo -e "${GREEN}Installation successfully terminated,  start cmd 'opf_console' from new shell.${COLOR_OFF}"