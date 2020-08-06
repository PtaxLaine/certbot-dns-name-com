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

if [[ -z "${CERTBOT_NAME_COM_USERNAME}" ]]; then
	echo "CERTBOT_NAME_COM_USERNAME environment variables is empty"
	exit -1
fi

if [[ -z "${CERTBOT_NAME_COM_TOKEN}" ]]; then
	echo "CERTBOT_NAME_COM_TOKEN environment variables is empty"
	exit -1
fi

$pythoncmd $script $paction $CERTBOT_DOMAIN $CERTBOT_VALIDATION $CERTBOT_NAME_COM_USERNAME $CERTBOT_NAME_COM_TOKEN | logger -t certbot_name_com

if [[ "$paction" == "add" ]]; then
        # DNS TXT f
        /bin/sleep 40
fi
