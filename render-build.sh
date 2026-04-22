#!/usr/bin/env bash
set -o errexit

# 1. Install Bench
pip install frappe-bench

# 2. Initialize the Bench
bench init frappe-bench --frappe-branch version-15 --python python3.11 --skip-redis-config-generation --no-backups

cd frappe-bench

# 3. Get your custom app
bench get-app https://github.com/TejasBedarkar/Frabbe_Backend.git

# 4. CRITICAL: Create the config file manually
# This tells Frappe where your database is!
mkdir -p sites/magna.in
cat <<EOF > sites/magna.in/site_config.json
{
 "db_name": "$DB_NAME",
 "db_password": "$DB_PASSWORD",
 "db_type": "mariadb",
 "db_host": "$DB_HOST",
 "db_port": 3306,
 "full_name": "magna.in"
}
EOF

# 5. Set the site as the current one
echo "magna.in" > sites/current_site.txt

# 6. Build assets so the UI loads
bench build --app frappe
