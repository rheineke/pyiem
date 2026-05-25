#!/usr/bin/env bash

# MYSQL_HOME=$PWD

# echo $MYSQL_HOME

# https://dev.mysql.com/doc/refman/5.7/en/osx-installation-launchd.html
cd /Library/LaunchDaemons
sudo launchctl load -F com.oracle.oss.mysql.mysqld.plist

# To configure MySQL to automatically start at bootup, you can:
# sudo launchctl load -w com.oracle.oss.mysql.mysqld.plist

# mysqld_safe Logging to '/usr/local/var/mysql/MacBook.err'

# mysqld_safe --explicit_defaults_for_timestamp --disable-partition-engine-check &
