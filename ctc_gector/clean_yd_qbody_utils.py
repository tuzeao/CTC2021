from clean_trans_symbol_to_ocr import clean_label
import re

FRAC_pt_all = re.compile(r'frac \d+ \d+')
FRAC_pt = re.compile(r'frac (\d+) (\d+)')


def clean_qbody_text(text):
    """提取sql题库数据中的文本，只提取一道题的"""
    import re
    def process_sql_latex(sql_text):
        img_latex_pt = re.compile(r"<img.*?data-latex=\"\\\\(.*?)\"/>")
        m = img_latex_pt.search(sql_text)
        while m is not None:
            latex = m.group(1)
            sql_text = re.sub(img_latex_pt, ' ' + latex + ' ', sql_text)
            m = img_latex_pt.search(sql_text)
        return sql_text

    def preprocess_sql(sql_text):
        """处理sql中的录题数据"""
        if not sql_text: return ""
        # if len(sql_text) > 160 or len(sql_text) < 8: return ""

        text = str(sql_text).strip()
        text = text.replace("\n", "")

        text = process_sql_latex(text)

        img_pt = re.compile(r"<img.*?>")
        div_pt = re.compile(r"<div.*?>")
        pstyle_pt = re.compile(r"<p style.*?>")
        span_pt = re.compile(r"<span.*?>")
        p1 = re.compile(r"<p.*?>")
        p2 = re.compile(r"<label.*?/label>")
        p3 = re.compile(r"<input.*?>")
        p4 = re.compile(r"<blk.*?/blk>")
        p5 = re.compile(r"<table.*?>")
        p6 = re.compile(r"<ul.*?>")
        p7 = re.compile(r"<li.*?/li>")
        p8 = re.compile(r"<td.*?>")
        p9 = re.compile(r"<em.*?>")
        p10 = re.compile(r"<dl.*?>")
        p11 = re.compile(r"<dl.*?>")
        p12 = re.compile(r"<.*?>")

        replace_pts = [img_pt, div_pt, pstyle_pt, span_pt, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        replace_symbs = ['<p>', '</p>', '</div>', '</span>', '&quot;', '&nbsp;', '<br/>',
                         '</td>', '</tr>', '</tbody>', '</table>', '<br>', '<tbody>',
                         '<tr>', '<td>', '<li>', '</li>', '</ul>', '<ul>', '<u>', '</u>',
                         '<sup>', '</sup>', '$', '\\t', '</em>', '<dd>', '</dd>', '</dl>',
                         '>>>>', '>>>', '<<<', '<<<<', '&ldquo;', '&rdquo;']

        for pt in replace_pts:
            text = re.sub(pt, ' ', text)

        for symb in replace_symbs:
            text = text.replace(symb, '')
        text = ' '.join(text.split())
        return text

    return preprocess_sql(text)

def clean_some_latex(text):
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')
    text = text.replace(' square ', '※')
    text = text.replace(' div ', '÷')
    text = text.replace(' times ', '×')
    text = text.replace(' quad ', ' ')
    text = text.replace(' geq ', '≥')
    text = text.replace(' leq ', '≤')

    def _frac_replace(text):
        m = FRAC_pt_all.findall(text)
        for frac_text in m:
            num = FRAC_pt.search(frac_text)
            d1, d2 = num.group(1), num.group(2)
            new_frac = "\\frac{%s}{%s}" % (d1, d2)
            text = text.replace(frac_text, new_frac)
        return text
    text = _frac_replace(text)


    return text

def clean_html_and_to_ocr_yd(text):
    text = clean_qbody_text(text)
    text = clean_some_latex(text)
    text = clean_label(text)
    # 最终去空格，符合ocr要求
    text = text.replace(' ', '')
    text = text.replace('　', '')
    text = text.replace('()', '(※)')

    return text

