#!/bin/bash
for k in $( seq 1 30 )
do
    if [ $k -lt 10 ]
    then
        tar1=fall_data/fall-0${k}-cam0-rgb
        tar2=fall_data/fall-0${k}-cam1-rgb
    else
        tar1=fall_data/fall-${k}-cam0-rgb
        tar2=fall_data/fall-${k}-cam1-rgb
    fi
    
    #unzip $tar1
    #unzip $tar2

    ls $tar1 | awk '{print tar1"/"$1}' tar1=$tar1 >> train_name.txt
    ls $tar2 | awk '{print tar2"/"$1}' tar2=$tar2 >> train_name.txt
done
