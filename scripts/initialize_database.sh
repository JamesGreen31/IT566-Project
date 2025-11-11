#!/usr/bin/env bash

DB_USER="root"
DB_PASS="toor"

mysql -u"$DB_USER" -p"$DB_PASS" < Drop_Database.sql
mysql -u"$DB_USER" -p"$DB_PASS" < Create_Schema.sql
mysql -u"$DB_USER" -p"$DB_PASS" < Create_Tables.sql
mysql -u"$DB_USER" -p"$DB_PASS" < Create_Procedures_and_Views.sql
mysql -u"$DB_USER" -p"$DB_PASS" < Insert_Sample_Data.sql

echo "Deployment complete."
