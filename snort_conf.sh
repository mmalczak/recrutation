#!/bin/sh 
 
apt-get update
sudo apt install -y gcc libpcre3-dev zlib1g-dev libluajit-5.1-dev libpcap-dev openssl libssl-dev libnghttp2-dev libdumbnet-dev bison flex libdnet

wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz
wget https://www.snort.org/downloads/snort/snort-2.9.14.1.tar.gz

tar xvzf daq-2.0.6.tar.gz
tar xvzf snort-2.9.14.1.tar.gz

cd daq-2.0.6
./configure && make && sudo make install
cd ../

cd snort-2.9.14.1
./configure --enable-sourcefire && make && sudo make install

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
sudo ldconfig


#sudo groupadd snort
#sudo useradd snort -r -s /sbin/nologin -c SNORT_IDS -g snort

sudo mkdir -p /etc/snort/rules
sudo mkdir /var/log/snort
sudo mkdir /usr/local/lib/snort_dynamicrules

sudo chmod -R 5775 /etc/snort
sudo chmod -R 5775 /var/log/snort
sudo chmod -R 5775 /usr/local/lib/snort_dynamicrules
sudo chown -R vagrant:vagrant /etc/snort
sudo chown -R vagrant:vagrant /var/log/snort
sudo chown -R vagrant:vagrant /usr/local/lib/snort_dynamicrules

echo 'include /etc/snort/rules/icmp.rules' >> /etc/snort/snort.conf
#echo 'alert icmp any any -> any any (msg:"ICMP Packet"; sid:477; rev:3;)' >> /etc/snort/rules/icmp.rules
echo 'alert tcp  any any -> 20.0.0.0/24 any (msg:"Possible TCP DoS"; threshold: type both, track by_src, count 200, seconds 3; sid:10;rev:1;)' >>  /etc/snort/rules/icmp.rules

