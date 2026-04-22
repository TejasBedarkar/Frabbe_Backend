#!/usr/bin/env bash
set -o errexit

# 1. Install Bench
pip install frappe-bench

# 2. Initialize the Bench
bench init frappe-bench \
  --frappe-branch version-15 \
  --python python3.11 \
  --skip-redis-config-generation \
  --no-backups

cd frappe-bench

# 3. Get your custom HR app
bench get-app https://github.com/TejasBedarkar/Frabbe_Backend.git

# 4. Create the site (This generates the necessary config files)
# Note: This will fail if DB credentials aren't in env vars, 
# so we use 'force' or manual config creation.
mkdir -p sites/magna.in

# 5. Create the site_config.json automatically
cat <<EOF > sites/magna.in/site_config.json
{
 "db_name": "$DB_NAME",
 "db_password": "$DB_PASSWORD",
 "db_type": "mariadb",
 "db_host": "$DB_HOST",
 "db_port": 3306
}
EOF

# 6. Set as default site
echo "magna.in" > sites/current_site.txt

# 7. Build assets
bench build
