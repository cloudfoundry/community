#!/bin/sh

chown runner /cache

su runner -p -s /bin/sh -c '/ko-app/ghproxy --legacy-disable-disk-cache-partitions-by-auth-header=false --cache-dir=/cache --cache-sizeGB=5'
