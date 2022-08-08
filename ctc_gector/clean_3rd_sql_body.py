from clean_3rd_qbody_utils import clean_html_and_to_ocr_3rd
from clean_extract_option import options_with_abcd, options_with_symbol_1234, options_with_1234
from clean_base import Qbody
import json
import re


def clean_3rd_process(qbody):
    text = clean_html_and_to_ocr_3rd(qbody)
    if '①' in text and '②' in text:
        options, text_without_options = options_with_symbol_1234(text)
        if options:
            return build_return(text_without_options, options)
    lower_text = text.lower()
    if 'a.' in lower_text and 'b.' in lower_text:
        options, text_without_options = options_with_abcd(text, strict=True)
        if options:
            return build_return(text_without_options, options)
    if '1' in text and '2' in text:
        options, text_without_options = options_with_1234(text)
        if options:
            return build_return(text_without_options, options)

    return build_return(text)


def build_return(text, options=None):
    if options:
        options = options[::-1]
    qb = Qbody(stem=text, options=options)
    return qb.to_json()


