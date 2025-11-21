#!/usr/bin/env bash

set -euo pipefail  

DB_USER="root"

# Determine the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${DB_PASS:-}" ]]; then
    read -s -p "Enter MySQL password for user ${DB_USER}: " DB_PASS
    echo
fi

# Execute scripts in order
mysql -u"${DB_USER}" -p"${DB_PASS}" < "${SCRIPT_DIR}/Drop_Database.sql"
mysql -u"${DB_USER}" -p"${DB_PASS}" < "${SCRIPT_DIR}/Create_Schema.sql"
mysql -u"${DB_USER}" -p"${DB_PASS}" < "${SCRIPT_DIR}/Create_Tables.sql"
mysql -u"${DB_USER}" -p"${DB_PASS}" < "${SCRIPT_DIR}/Create_Procedures_and_Views.sql"
mysql -u"${DB_USER}" -p"${DB_PASS}" < "${SCRIPT_DIR}/Insert_Sample_Data.sql"

echo "Deployment complete."
