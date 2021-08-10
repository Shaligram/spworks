PREFIX=$1
DEVICE=$2
for i in {1..255}
do
    ip address add $PREFIX.$i/32 dev $DEVICE
done
