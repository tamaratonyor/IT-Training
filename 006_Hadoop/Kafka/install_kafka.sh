#!/usr/bin/env bash

cd opt
mkdir /home/tammy/opt/kafka
cd kafka
wget https://www-eu.apache.org/dist/kafka/2.3.1/kafka_2.11-2.3.1.tgz
tar -zxvf kafka-2.3.1-src.tgz
cd
sudo gedit .bash_profile.sh
echo "export KAFKA_HOME=/home/tammy/opt/kafka/kafka-2.3.1-src" >> .bash_profile.sh
