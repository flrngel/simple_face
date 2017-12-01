#!/bin/bash

infloop() {
time=$1
shift
while :
do
  sleep $time
  $@
done
}

infloop 1 python app.py
