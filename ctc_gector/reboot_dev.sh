#!/usr/bin/env sh

#source /home/homework/.bashrc
#WORKSPACE=`pwd`
python='/ssd/exec/tuzeao/anaconda3/envs/gector/bin/python'

kill_process(){
    pids=`ps aux | grep "gector_server.py" | grep "dev" | grep -v "grep" | awk -F ' ' '{print $2}'`
    for pid in $pids
    do
        if [ "$pid" != "" ];then
            kill -9 $pid
        fi
    done
}


kill_process
nohup $python -u baike_server.py 8360 dev &
echo "server in port 8360 start"
# ps -ef | grep baike_server.py  | grep -v grep | awk -F ' ' '{print $2}' | xargs -n 1 kill -9
