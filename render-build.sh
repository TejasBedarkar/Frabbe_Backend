#!/usr/bin/env bash
set -o errexit

# 1. Install Bench
pip install frappe-bench

# 2. Build the Bench folder
# We skip redis check because we connect to Render's internal Redis later
bench init --skip-redis-config-check --python python3.11 frappe-bench

cd frappe-bench

# 3. Pull your code from GitHub into the new bench
bench get-app https://github.com/TejasBedarkar/Frabbe_Backend.git

# 4. Create the site folder manually (since we don't run 'new-site')
mkdir -p sites/magna.in