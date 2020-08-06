# certbot-dns-name-com
A certbot DNS plugin for name.com 
Usage:

check:
$ CERTBOT_NAME_COM_USERNAME=you_name_com_accout \
CERTBOT_NAME_COM_TOKEN=you_name_com_api_token \
certbot-auto renew --cert-name yourdomain.com --manual-auth-hook /path/to/certbot_dns_auth.sh --dry-run

renew:
$ CERTBOT_NAME_COM_USERNAME=you_name_com_accout \
CERTBOT_NAME_COM_TOKEN=you_name_com_api_token \
certbot-auto renew --cert-name yourdomain.com --manual-auth-hook /path/to/certbot_dns_auth.sh
