#!/bin/bash

rm -rf /usr/local/nginx/html/bdbbuyanalysis
mkdir /usr/local/nginx/html/bdbbuyanalysis
cp -rf /root/Bdbproject/bdbbuy_analysis/BdbbuyDataCenterWeb/dist/* /usr/local/nginx/html/bdbbuyanalysis/

/usr/local/nginx/sbin/nginx -s reload
