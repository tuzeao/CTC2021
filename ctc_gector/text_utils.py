import re


def text_process(query):
    # 平方立方问题
    query = query.replace('m²', 'm2').replace('m³', 'm3')
    query = query.replace("m^3", "m3").replace("m^2", "m2")

    return query
