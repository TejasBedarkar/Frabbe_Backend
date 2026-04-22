#!/usr/bin/env bash
set -o errexit

# 1. Install Bench
pip install frappe-bench

# 2. Build the Bench for Version 15 
# We add --skip-backups to prevent the 'crontab' error on Render
bench init frappe-bench \
  --frappe-branch version-15 \
  --python python3.11 \
  --skip-redis-config-generation \
  --no-backups

cd frappe-bench

# 3. Get your custom app
bench get-app https://github.com/TejasBedarkar/Frabbe_Backend.git

# 4. Create the site folder manually
mkdir -p sites/magna.in
