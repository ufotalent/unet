#!/bin/bash
while true; do
    while read line; do 
        ip=$(echo $line | awk '{print $2}')
        ping -qc 60 $ip | tail -n2 > pings/$ip.new &
    done < ip-name
    wait
    while read line; do 
        ip=$(echo $line | awk '{print $2}')
        cat pings/$ip.new | grep loss | awk -F ',' '{for (i=1;i<=NF;i++) print $i}'  | grep loss > pings/$ip
        cat pings/$ip.new | grep avg | awk -F '/' '{print $5}' >> pings/$ip 
    done < ip-name
done
