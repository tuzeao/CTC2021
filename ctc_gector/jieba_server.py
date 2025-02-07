from jieba_math import math_pos_seg
from clean_yd_sql_qbody import clean_yd_process, server_text_to_ocr, clean_html_and_to_ocr_yd
from clean_yd_qbody_utils import clean_qbody_text, clean_some_latex
from clean_3rd_sql_body import clean_3rd_process, clean_html_and_to_ocr_3rd
from clean_3rd_qbody_utils import replace_some_latex_3rd

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


@app.route('/jieba_cut', methods=["POST", "GET"])
def handler(request):
    req_dict = request.form if request.form else request.json
    req_dict = request.args if not req_dict else req_dict
    # req_dict = {
    #     'source': request.form.get("source"),
    #     'target': request.form.get("target"),
    # }
    mylogger.info(f"ACCESS: [from:{request.ip}:{request.port}][to:{request.url}][args:{req_dict}]")
    begin = time.time()
    query = req_dict['q']
    if not query:
        query = [""]
    response = math_pos_seg(query[0])
    time_cost = round(1000*(time.time()-begin), 1)
    mylogger.info(f"FINISH: [query: {req_dict.get('query')}][耗时: {time_cost}ms]")
    return sjson(response, dumps=json.dumps, ensure_ascii=False)


@app.route('/tiku_sql_clean', methods=["POST", "GET"])
def handler(request):
    req_dict = request.form if request.form else request.json
    req_dict = request.args if not req_dict else req_dict
    # req_dict = {
    #     'source': request.form.get("source"),
    #     'target': request.form.get("target"),
    # }
    mylogger.info(f"ACCESS: [from:{request.ip}:{request.port}][to:{request.url}][args:{req_dict}]")
    begin = time.time()
    query = json.loads(req_dict['qbody'][0])
    source = req_dict.get('source', 'yd')
    source_map = {
        'yd': clean_yd_process, '3rd': clean_3rd_process,
    }
    response = source_map[source](query)
    time_cost = round(1000*(time.time()-begin), 1)
    mylogger.info(f"FINISH: [query: {req_dict.get('query')}][耗时: {time_cost}ms]")
    return sjson(response, dumps=json.dumps, ensure_ascii=False)


@app.route('/text_tools', methods=["POST", "GET"])
def handler(request):
    req_dict = request.form if request.form else request.json
    req_dict = request.args if not req_dict else req_dict
    # req_dict = {
    #     'source': request.form.get("source"),
    #     'target': request.form.get("target"),
    # }
    mylogger.info(f"ACCESS: [from:{request.ip}:{request.port}][to:{request.url}][args:{req_dict}]")
    begin = time.time()
    query = req_dict['q'][0]
    action = req_dict.get('action', 'all')
    source = req_dict.get('source', 'yd')
    _map = {
        "yd": {
            "remove_html": clean_qbody_text,
            "trans_latex": clean_some_latex,
            "trans_ocr": server_text_to_ocr,
            "all": clean_html_and_to_ocr_yd,
        },
        "3rd": {
            "remove_html": clean_qbody_text,
            "trans_latex": replace_some_latex_3rd,
            "trans_ocr": server_text_to_ocr,
            "all": clean_html_and_to_ocr_3rd,
        }
    }
    result = _map[source][action](query)
    response = {
        "query": query,
        "new_query": result,
        "source": source,
        "action": action,
    }
    time_cost = round(1000*(time.time()-begin), 1)
    mylogger.info(f"FINISH: [query: {req_dict.get('query')}][耗时: {time_cost}ms]")
    return sjson(response, dumps=json.dumps, ensure_ascii=False)


if __name__ == "__main__":
    port = sys.argv[1]
    app.run(host="0.0.0.0", port=int(port), access_log=False)
