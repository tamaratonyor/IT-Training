#!/usr/bin/env bash

cd opt
mkdir /home/tammy/opt/kafka
cd kafka
wget https://www.apache.org/dyn/closer.cgi?path=/kafka/2.3.1/kafka-2.3.1-src.tgz
tar -zxvf kafka-2.3.1-src.tgz
cd
sudo gedit .bash_profile.sh
echo "export KAFKA_HOME=/home/tammy/opt/kafka" >> .bash_profile.sh
