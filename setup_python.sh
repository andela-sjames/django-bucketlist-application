#!/usr/bin/env bash

apt-get update
apt-get -f install -y
apt-get install python-pip python-dev build-essential -y
