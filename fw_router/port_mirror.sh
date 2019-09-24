#!/bin/sh

ip link add tun0 type gretap remote 30.0.0.2 local 30.0.0.99 dev enp0s10
ip link set tun0 up 


source_if=enp0s9
dest_if=tun0
 
# enable the destination port
ifconfig $dest_if up;:
 
# mirror ingress traffic
tc qdisc add dev $source_if ingress;:
tc filter add dev $source_if parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev $dest_if;:
 
# mirror egress traffic
tc qdisc add dev $source_if handle 1: root prio;:
tc filter add dev $source_if parent 1: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev $dest_if;:
