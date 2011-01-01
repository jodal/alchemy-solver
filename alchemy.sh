#! /bin/sh

./alchemy.py > alchemy.dot
dot -Tpng -oalchemy.png alchemy.dot
