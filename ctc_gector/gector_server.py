from entrance import gector_predict_single
import asyncio
from sanic import Sanic
from sanic import log
from sanic.response import json as sjson
import logging.handlers
import time
import sys
import os
import json

class MyLogger:
    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.logger = self.process()

    def process(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "log")):
            os.system("mkdir -p log")
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            fh = logging.handlers.TimedRotatingFileHandler("log/log.txt", 'midnight')
            fh.suffix = "%Y%m%d"
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y.%m.%d %H:%M:%S")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        return logger

mylogger = MyLogger("mylogger").logger

app = Sanic("gector")

@app.route('/q', methods=["POST", "GET"])
def handler(request):
    req_dict = request.form if request.form else request.json
    req_dict = request.args if not req_dict else req_dict
    # req_dict = {
    #     'source': request.form.get("source"),
    #     'target': request.form.get("target"),
    # }
    mylogger.info(f"ACCESS: [from:{request.ip}:{request.port}][to:{request.url}][args:{req_dict}]")
    begin = time.time()
    source, target = req_dict['source'], req_dict['target']
    if isinstance(req_dict['source'], list):
        source, target = req_dict['source'][0], req_dict['target'][0]
    response = gector_predict_single(source, target)
    time_cost = round(1000*(time.time()-begin), 1)
    response['time_cost'] = f"{time_cost}ms"
    mylogger.info(f"FINISH: [query: {req_dict.get('query')}][耗时: {time_cost}ms]")
    return sjson(response, dumps=json.dumps, ensure_ascii=False)


if __name__ == "__main__":
    port = sys.argv[1]
    app.run(host="0.0.0.0", port=int(port), access_log=False)
