# coding=utf-8

import re
import string

phone_map = {
    'ā': 'a',
    'á': 'a',
    'ǎ': 'a',
    'à': 'a',
    'ō': 'o',
    'ó': 'o',
    'ǒ': 'o',
    'ò': 'o',
    'ē': 'e',
    'é': 'e',
    'ě': 'e',
    'è': 'e',
    'ī': 'i',
    'í': 'i',
    'ǐ': 'i',
    'ì': 'i',
    'ū': 'u',
    'ú': 'u',
    'ǔ': 'u',
    'ù': 'u',
    'ǖ': 'ü',
    'ǘ': 'ü',
    'ǚ': 'ü',
    'ǜ': 'ü',
}
parse_not_ch = re.compile(f"[^\u4e00-\u9fa5]")


def clean_phone(strs):
    """
    清除拼音相关的特殊字符
    """
    new_str = ''
    for char in strs:
        if char in phone_map:
            new_str += phone_map[char]
        else:
            new_str += char
    return new_str


def similar_char_normal(strs):
    """
    相似文本归一化，可能是其他国家文字，比如日文
    """
    # 过滤加减等于符号
    strs = strs.replace('＋', '+').replace('—', '-').replace('﹢', '+')
    strs = strs.replace('－', '-').replace('＝', '=').replace('﹣', '-')
    # 过滤不等号相关
    strs = strs.replace('﹥', '>').replace('＞', '>').replace('﹤', '<').replace(u'＜', u'<')
    strs = strs.replace('（', '(').replace('）', ')')
    strs = strs.replace('～', '~').replace('＃', '#')

    strs = strs.replace('ー', '一')
    strs = strs.replace('；', ';')
    strs = strs.replace(',', '，')
    strs = strs.replace('：', ':')
    strs = strs.replace('％', '%')
    strs = strs.replace('“', '"')
    strs = strs.replace('”', '"')
    strs = strs.replace('５', '5')
    strs = strs.replace('３', '3')
    strs = strs.replace('４', '4')
    strs = strs.replace('７', '7')
    strs = strs.replace('０', '0')
    strs = strs.replace('１', '1')
    strs = strs.replace('６', '6')
    strs = strs.replace('９', '9')
    strs = strs.replace('２', '2')
    strs = strs.replace('８', '8')
    strs = strs.replace('？', '?')
    strs = strs.replace('﹦', '=')
    strs = strs.replace('．', '.')
    strs = strs.replace('𦫼', '□')
    strs = strs.replace('★', '☆')
    strs = strs.replace('◆', '◇')
    strs = strs.replace('▲', '△')
    strs = strs.replace('Δ', '△')
    strs = strs.replace('₂', '²')
    strs = strs.replace('♢', '◇')
    strs = strs.replace('●', '○')
    strs = strs.replace('〇', '○')
    strs = strs.replace('■', '□')
    strs = strs.replace('▪', '□')
    strs = strs.replace('∎', '□')
    strs = strs.replace('▢', '□')
    strs = strs.replace('Π', 'π')
    strs = strs.replace('β', 'β')
    strs = strs.replace('▼', '▽')
    strs = strs.replace('▶', '▷')
    strs = strs.replace('►', '▷')
    strs = strs.replace('▸', '▷')
    strs = strs.replace('º', '°')
    strs = strs.replace('∶', ':')
    strs = strs.replace('≠', '≠')
    strs = strs.replace('∧', '^')
    strs = strs.replace('Λ', '^')
    strs = strs.replace('ʌ', '^')
    strs = strs.replace('＿', '_')
    strs = strs.replace('❤', '♡')
    strs = strs.replace('♡', '♡')
    strs = strs.replace('♥', '♡')
    strs = strs.replace('✰', '✩')
    strs = strs.replace('♦', '♢')
    strs = strs.replace('ˈ', '‘')
    strs = strs.replace('＇', '‘')
    strs = strs.replace('〞', '‘')
    strs = strs.replace('Ⓞ', '⌾')
    strs = strs.replace('⊚', '⌾')
    strs = strs.replace('⊚', '⌾')
    strs = strs.replace('◎', '⌾')
    strs = strs.replace('◉', '⌾')
    strs = strs.replace('⭐', '✩')
    strs = strs.replace('｛', '{')
    strs = strs.replace('［', '[')
    strs = strs.replace('］', ']')
    strs = strs.replace('⁰', '°')
    strs = strs.replace('↑', '↑')
    strs = strs.replace('←', '←')
    strs = strs.replace('→', '→')
    strs = strs.replace('➩', '→')
    strs = strs.replace('⇨', '→')
    strs = strs.replace('⇐', '←')
    strs = strs.replace('⇔', '⇆')
    strs = strs.replace('↓', '↓')
    strs = strs.replace('／', '/')
    strs = strs.replace('＊', '*')
    strs = strs.replace('›', '>')
    strs = strs.replace('·', '.')  # 不确定是否要转，eg.人名
    strs = strs.replace('•', '.')
    strs = strs.replace('﹒', '.')
    strs = strs.replace('【', '[')
    strs = strs.replace('】', ']')
    strs = strs.replace('\'', '‘')
    strs = strs.replace('′', '‘')
    strs = strs.replace('”', '‘')
    strs = strs.replace('’', '‘')
    strs = strs.replace('“', '‘')
    strs = strs.replace('〃', '‘')
    strs = strs.replace('？', '?')
    strs = strs.replace(',', '，')
    strs = strs.replace('‰', '%')
    strs = strs.replace('〖', '[')
    strs = strs.replace('〗', ']')
    strs = strs.replace('"', '‘')
    strs = strs.replace('〈', '《')
    strs = strs.replace('〉', '》')
    strs = strs.replace('「', '[')
    strs = strs.replace('」', ']')
    strs = strs.replace('『', '[')
    strs = strs.replace('』', ']')
    strs = strs.replace('〔', '[')
    strs = strs.replace('〕', ']')
    strs = strs.replace('﹝', '[')
    strs = strs.replace('﹞', ']')
    strs = strs.replace('丨', '|')
    strs = strs.replace('丶', '、')
    strs = strs.replace('！', '!')
    strs = strs.replace('｜', '|')
    strs = strs.replace('〢', '|')
    strs = strs.replace('∣', '|')
    strs = strs.replace('Ｉ', '|')
    strs = strs.replace('⚪', '○')
    strs = strs.replace('✖', '×')
    strs = strs.replace('∽', '~')
    strs = strs.replace('圏', '圈')
    strs = strs.replace('拋', '抛')
    strs = strs.replace('｝', '}')
    strs = strs.replace('C', 'c')
    strs = strs.replace('オ', '才')
    strs = strs.replace('庹', '度')
    strs = strs.replace('＂', '‘')
    strs = strs.replace('ト', '卜')
    strs = strs.replace('ｍ', 'm')
    strs = strs.replace('γ', 'r')
    return strs


def english_normal(strs):
    strs = strs.replace('Ⅰ', 'I')
    strs = strs.replace('Ｂ', 'B')
    strs = strs.replace('Ｈ', 'H')
    strs = strs.replace('α', 'a')
    strs = strs.replace('C', 'c')
    strs = strs.replace('K', 'k')
    strs = strs.replace('O', 'o')
    strs = strs.replace('P', 'p')
    strs = strs.replace('S', 's')
    strs = strs.replace('U', 'u')
    strs = strs.replace('V', 'v')
    strs = strs.replace('W', 'w')
    strs = strs.replace('X', 'x')
    strs = strs.replace('Z', 'z')
    return strs


def clean_superscript(strs):
    """
    将2²归一化为2^2}
    """
    if '^' in strs:

        strs = strs.replace('^{²}', '²')
        strs = strs.replace('^{³}', '³')
        strs = strs.replace('^{⁴}', '⁴')
        strs = strs.replace('^{°}', '°')
        strs = strs.replace('^²}', '²')
        strs = strs.replace('^³}', '³')
        strs = strs.replace('^⁴}', '⁴')
        strs = strs.replace('^°}', '°')
        strs = strs.replace('^²', '²')
        strs = strs.replace('^³', '³')
        strs = strs.replace('^⁴', '⁴')
        strs = strs.replace('^°', '°')
        strs = strs.replace('²', '^{2}')
        strs = strs.replace('³', '^{3}')
        strs = strs.replace('⁴', '^{4}')
        # strs = strs.replace('°', '^{°}')
        strs = re.sub(r'\^([^{]*?)}', r'^{\1}', strs) # 2^2} -> 2^{2}
        strs = re.sub(r'\^([^{][0-9\.]*)', r'^{\1}', strs)  # 2^2->2^{2}
    else:
        strs = strs.replace('²', '^{2}')
        strs = strs.replace('³', '^{3}')
        strs = strs.replace('⁴', '^{4}')
        # strs = strs.replace('°', '^{°}')
    return strs


def one2many_normal(strs):
    """
    处理多个字符合并为一个字符的case
    """
    strs = strs.replace('㎡', 'm²')
    strs = strs.replace('m³', 'm³')
    strs = strs.replace('㎝', 'cm')
    strs = strs.replace('㎏', 'kg')
    strs = strs.replace('℃', '°c')
    strs = strs.replace('⑷', '(4)')
    strs = strs.replace('‖', '||')
    strs = strs.replace('∥', '//')
    strs = strs.replace('㏒', 'log')
    strs = strs.replace('㏑', 'ln')
    return strs


def normal_dot(strs):
    strs = strs.replace('••••••', '…').replace('······', '…')
    strs = strs.replace('·····', '…').replace('····', '…')
    strs = strs.replace('......', '…')
    # 过滤省略号
    strs = strs.replace('··', '…')
    strs = strs.replace('‥', '…')
    strs = strs.replace('...', '…')
    strs = strs.replace('.....', '…')
    # yu_idx = strs.find('余')
    # if yu_idx != -1:
    #     if yu_idx > 0 and parse_not_ch.match(strs[yu_idx - 1]) or yu_idx < len(strs) - 1 and parse_not_ch.match(
    #             strs[yu_idx + 1]):
    #         strs = strs.replace(u'余', '…')
    return strs


def normal_sqrt(strs):
    strs = strs.replace('根号{', '/sqrt{')
    strs = strs.replace(r'根 号', '/sqrt')
    strs = re.sub(r'根号{(.*?)}', r'/sqrt{\1}', strs)
    return strs


def normal_tu(strs):
    # 过滤涂改相关
    strs = strs.replace('�', '涂').replace('ᚏ', '涂').replace('“涂”', '涂')
    strs = strs.replace('0̶', '涂').replace('1̶', '涂').replace('2̶', '涂')
    strs = strs.replace('3̶', '涂').replace('4̶', '涂').replace('5̶', '涂')
    strs = strs.replace('6̶', '涂').replace('7̶', '涂').replace('8̶', '涂').replace('9̶', '涂')
    strs = strs.replace('--', '')  # 针对竖式标注
    strs = strs.replace('---', '')
    strs = re.sub('\S̶', '涂', strs)
    strs = re.sub(r'涂+', r'涂', strs)
    return strs


def normal_fen(label):
    label = re.sub(r'{(\([0-9]+\))/(\([0-9]+\))}', r'/frac{\1}{\2}', label)
    label = re.sub(r'{([0-9]+)/(\([0-9]+\))}', r'/frac{\1}{\2}', label)
    label = re.sub(r'{(\([0-9]+\))/([0-9]+)}', r'/frac{\1}{\2}', label)
    label = re.sub(r'{([0-9]+)/([0-9]+)}', r'/frac{\1}{\2}', label)

    label = re.sub(r'(\([0-9]+\))/(\([0-9]+\))', r'/frac{\1}{\2}', label)
    label = re.sub(r'([0-9]+)/(\([0-9]+\))', r'/frac{\1}{\2}', label)
    label = re.sub(r'(\([0-9]+\))/([0-9]+)', r'/frac{\1}{\2}', label)
    label = re.sub(r'([0-9]+)/([0-9]+)', r'/frac{\1}{\2}', label)
    label = label.replace('又/frac', '/frac')

    # 非数字分式，目前有bug
    # label = re.sub(r'\{(.*?)\}/\{(.*?)\}', r'{\1/\2}', label)
    # label = re.sub(r'([^+\-×÷={}()…~≈<>≤≥]+)/\{(.*?)\}', r'{\1/\2}', label)
    # label = re.sub(r'{(.*?)}/([^+\-×÷={}()…~≈<>≤≥]+)', r'{\1/\2}', label)
    # label = re.sub(r'([^+\-×÷={}()…~≈<>≤≥]+)/([^+\-×÷={}()…~≈<>≤≥]+)', r'{\1/\2}', label)
    return label


def clearTihao(strs):
    '''
    将题号统一变为!23!
    '''
    strs = strs.replace('❶', '!1!').replace('❸', '!3!').replace('❹', '!4!')
    strs = strs.replace('❽', '!8!').replace('❻', '!6!')
    strs = strs.replace('®', '!R!')
    strs = strs.replace('Ⓡ', '!R!')
    strs = strs.replace('©', '!c!')
    strs = strs.replace('Ⓒ', '!c!')
    strs = strs.replace('Ⓐ', '!A!')
    strs = strs.replace('①', '!1!')
    strs = strs.replace('②', '!2!')
    strs = strs.replace('③', '!3!')
    strs = strs.replace('④', '!4!')
    strs = strs.replace('⑤', '!5!')
    strs = strs.replace('⑥', '!6!')
    strs = strs.replace('⑦', '!7!')
    strs = strs.replace('⑧', '!8!')
    strs = strs.replace('⑨', '!9!')
    strs = strs.replace('⑩', '!10!')

    cond1 = re.match(r'!\(?\d+\)?!', strs)  # 匹配形如!(23)!，!23!
    cond2 = re.match(r'!\*\d+\*!', strs)  # 匹配形如!*23*!,
    cond3 = re.match(r'\*\d+\*', strs)  # 匹配形如 *23*
    if cond1 != None:
        s = cond1.span()
        ind = s[1]
    elif cond2 != None:
        s = cond2.span()
        ind = s[1]
    elif cond3 != None:
        s = cond3.span()
        ind = s[1]
    else:
        strs = re.sub(r'!(.+?)!', r'圆{\1}', strs)
        return strs
    ind0 = s[0]
    ind1 = s[1]
    if ind0 == 0 and len(strs) - 1 > ind1 and strs[ind1] not in ['+', '-', '×', '÷', '=', '<', '>']:
        head = strs[:ind]
        end = strs[ind:]
        head = head.replace('*', '').replace('(', '').replace(')', '').replace('!', '')
        head = '!' + head + '!'
        strs = head + end
    strs = re.sub(r'!(.+?)!', r'圆{\1}', strs)
    return strs


def normal_repeat(strs):
    strs = re.sub('-+', '-', strs)
    strs = re.sub('_+', '_', strs)
    strs = re.sub('‘+', '‘', strs)
    strs = re.sub('…+', '…', strs)
    return strs


def clean_label(strs):
    # 新增
    strs = strs.replace('#', '')
    # strs = strs.replace(' ', '')
    # strs = strs.replace('　', '')
    strs = strs.replace('\n', '')
    strs = re.sub(r'循环{([0-9]*)}', r'\1', strs)
    strs = strs.replace('"""', "‘")
    strs = strs.strip('"')
    strs = strs.replace('0✓', '!✓!')
    strs = strs.replace('☑', '!✓!')
    # 过滤相似字符：
    strs = similar_char_normal(strs)
    # 归一化英文
    strs = english_normal(strs)
    # 过滤拼音
    #strs = clean_phone(strs)
    # 对上标进行归一化
    strs = clean_superscript(strs)
    # 处理多个字符合并为一个字符的case
    strs = one2many_normal(strs)
    # 处理小数点
    strs = normal_dot(strs)
    # 处理根号
    strs = normal_sqrt(strs)
    # 处理涂改
    strs = normal_tu(strs)
    # 处理分数
    strs = normal_fen(strs)
    # 过滤题号
    strs = clearTihao(strs)
    # 过滤重复符号
    strs = normal_repeat(strs)
    # 替换括号
    strs = strs.replace('()', '(※)')
    return strs


def get_char_type(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return 'chinese'
    elif ch not in string.ascii_lowercase + string.ascii_uppercase:
        return 'others'
    else:
        return 'en'


def clean_latex(char):
    char.replace('/pi', 'π')
    char = char.replace('/ldots', '…')
    char = char.replace('/cdot', '…')
    char = char.replace('/cdots', '…')
    char = char.replace('/cos', 'c o s')
    char = char.replace('/mu', 'u')
    char = char.replace('/Delta', '△')
    char = char.replace('V', 'v')
    char = char.replace('P', 'p')
    char = char.replace('X', 'x')
    char = char.replace('/log', 'l o g')
    char = char.replace('/tan', 't a n')
    char = char.replace('/sin', 's i n')
    char = char.replace('C', 'c')
    char = char.replace('/times', '×')
    return char


def normal_self(label):
    label = label.replace('#end2end', '')
    return label


def normal_arith(label):
    label = label.replace('≈', '~')
    return label


if __name__ == '__main__':
    strs = '是50^2}'
    strs = re.sub(r'\^([^{]*?)}', r'^{\1}', strs)
    print(strs)
    power_test = ['是50^2,', '是50^2},', '是50^{2},',
                  '是50^²,', '是50^²},', '是50^{²},',
                  '是50^°,', '是50^°},', '是50^{°},'
                  ]
    for orign in power_test:
        print(orign)
        print(clean_label(orign))
        print('-----------------------------------------')
