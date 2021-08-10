SOURCE=$1
DEST=$2
for i in {1..255}
do
    for j in {1..255}
    do
        curl -v --interface $SOURCE.$i http://$DEST.$j/hello.txt
    done
done
