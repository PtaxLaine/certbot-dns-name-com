#!/bin/bash
set -e
paction=$1

if [[ "$paction" != "clean" ]]; then
	paction="add"
fi

pythoncmd="/bin/env python3"
source_dir="$(dirname ${BASH_SOURCE[0]})"
script="$source_dir/name_com_dns.py"

echo $CERTBOT_DOMAIN
echo $CERTBOT_VALIDATION

$pythoncmd $script $paction $CERTBOT_DOMAIN $CERTBOT_VALIDATION | logger -t certbot_name_com

if [[ "$paction" == "add" ]]; then
        # DNS TXT f
        /bin/sleep 40
fi
