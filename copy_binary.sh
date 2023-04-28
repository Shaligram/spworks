
#set machine 1
#read -s -p "Transfer from 192.168.0.11 to .50/.171 [1/0] " machine


if [ "$1" -eq 1 ]; then
echo "->>>>>>>>>>>>>>>>>>>>Transfering to .50"
machine=1
else
echo "->>>>>>>>>>>>>>>>>>>>Transfering to .171"
machine=0
fi

read -s -p "Press enter" junk

#scp -r bin.debug root@192.168.0.11:/root/shaligram/incoming/
#scp -r vcm-cli/cli root@192.168.0.11:/root/shaligram/incoming/

#scp  vcm-dpe/dpi/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
#scp  vcm-dpe/dpi/mdp-dpi/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
#scp  vcm-dpe/dpi/mdp-dpi/plugins/* root@192.168.0.11:/root/shaligram/incoming/lib/
#scp  cmake-build-debug/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
#scp  vcm-install/VCM-SAF/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
#scp vcm-cluster-gen/vcm/third-party/confd/lib/libconfd.so root@192.168.0.11:/root/shaligram/incoming/lib/


rsync -av bin.debug root@192.168.0.11:/root/shaligram/incoming/
rsync -av vcm-cli/cli root@192.168.0.11:/root/shaligram/incoming/

rsync -v vcm-dpe/dpi/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
rsync -v vcm-dpe/dpi/mdp-dpi/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
rsync -v vcm-dpe/dpi/mdp-dpi/plugins/* root@192.168.0.11:/root/shaligram/incoming/lib/
rsync -vq cmake-build-debug/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
rsync -vq vcm-install/VCM-SAF/lib/* root@192.168.0.11:/root/shaligram/incoming/lib/
rsync -vq vcm-cluster-gen/vcm/third-party/confd/lib/libconfd.so root@192.168.0.11:/root/shaligram/incoming/lib/


echo "->>>>>>>>>>>>>>>>>>>>Transfering to final destination"

if [ $machine -eq 1 ]; then
ssh root@192.168.0.11 <<'ENDSSH'
#sshpass -p root123 scp -r /root/shaligram/incoming/* root@192.168.0.50:/root/shaligram/incoming/
sshpass -p root123 rsync -a /root/shaligram/incoming/* root@192.168.0.50:/root/shaligram/incoming/
ENDSSH
echo "->>>>>>>>>>>>>>>>>>>>Transferd to .50"
else
ssh root@192.168.0.11 <<'ENDSSH'
#sshpass -p root123 scp -r /root/shaligram/incoming/* root@192.168.0.171:/root/shaligram/incoming/
sshpass -p root123 rsync -a /root/shaligram/incoming/* root@192.168.0.171:/root/shaligram/incoming/
ENDSSH
echo "->>>>>>>>>>>>>>>>>>>>Transferd to .171"
fi
