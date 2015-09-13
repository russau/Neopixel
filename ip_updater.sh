#!/bin/bash
wifiip=$(ip addr | grep inet | grep wlan0 | awk -F" " '{print $2}'| sed -e 's/\/.*$//')
previousip=`cat wifiip.txt`
if [ "$wifiip" != "$previousip" ]
then
  echo "New wifi IP address $wifiip" >> /tmp/cronlog
  /usr/local/bin/aws route53 change-resource-record-sets --hosted-zone-id Z2VC8C1RZFL1P9 --change-batch "{\"Comment\":\"Wifi Address change\",\"Changes\":[{\"Action\":\"UPSERT\",\"ResourceRecordSet\":{\"Name\":\"rpi.cloudtraining.link.\",\"Type\":\"A\",\"TTL\":30,\"ResourceRecords\":[{\"Value\":\"$wifiip\"}]}}]}" >> /tmp/cronlog
fi
echo $wifiip > wifiip.txt
