#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

rsync -a ../../vpn/gen/client_dev/ ./openvpn_team_main_net_client_dev/
rsync -a ../../vpn/gen/client_prod/ ./openvpn_team_main_net_client_prod/

python3 init_slots.py

python3 gen_team_tokens_dev.py
python3 gen_rootpasswds_dev.py

#python3 init_slots.py
#python3 init_teams.py