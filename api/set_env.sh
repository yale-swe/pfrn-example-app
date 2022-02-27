#!/bin/bash

# Usage: sh set_env.sh '<username>' '<password>' '<host_address>' '<db_name>'
# TODO: Add something to set the scope. 
# Simple bash script that takes in command line 
# arguments and sets the environment variables
# accordingly. Note that for the purposes of the tutorial:
# DB_USER = 'pfrn_user'
# DB_PASS = 'pfrn_password'
# DB_HOST = 'localhost'
# DB_NAME = 'pfrn_db'
export DB_USER=$1
export DB_PASS=$2
export DB_HOST=$3
export DB_NAME=$4