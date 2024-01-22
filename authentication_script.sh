#!/bin/bash

username=$1
password=$2

# Perform SQLite authentication logic
result=$(sqlite3 user_database.db "SELECT count(*) FROM users WHERE username='$username' AND password='$password';")

if [ "$result" -eq 1 ]; then
    exit 0  # Authentication successful
else
    exit 1  # Authentication failed
fi

