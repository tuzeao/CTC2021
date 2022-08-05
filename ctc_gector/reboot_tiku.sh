#!/usr/bin/env sh

#source /home/homework/.bashrc
#WORKSPACE=`pwd`
python='/ssd/exec/tuzeao/anaconda3/envs/gector/bin/python'

kill_process(){
    pids=`ps aux | grep "jieba_server.py" | grep "dev" | grep -v "grep" | awk -F ' ' '{print $2}'`
    for pid in $pids
    do
        if [ "$pid" != "" ];then
            kill -9 $pid
        fi
    done
}

kill_process


for port in {8360..8364}
do
      nohup $python -u jieba_server.py ${port} dev &
      echo "server in port ${port} start"
done
