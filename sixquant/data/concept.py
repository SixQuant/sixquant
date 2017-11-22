# coding=utf-8

from ..constants import CONCEPTS_FILE
from ..utils.daily_cache import daily_cache
from ..utils.fetcher import fetcher

"""
股票概念信息
"""

# 股票概念黑名单
CONCEPTS_BLACK_LIST = ['新股与次新股',
                       '融资融券', '转融券标的',
                       '深港通', '沪港通概念',
                       '证金持股', 'MSCI概念',
                       '举牌', '股权转让',
                       '参股新三板']


def parse_concepts_compact_text(text):
    """
    解析紧凑格式的概念数据文本
    :return:
    """
    code_concepts = {}  # 股票所属概念字典
    concept_codes = {}  # 概念下属股票字典
    for line in text.split('\n'):
        n = len(line)
        if n > 0:
            if line[0] == '#':
                concept = line[1:]
            else:
                code = line
                try:
                    a = concept_codes[concept]
                except KeyError:
                    a = []
                    concept_codes[concept] = a
                a.append(code)
                try:
                    a = code_concepts[code]
                except KeyError:
                    a = []
                    code_concepts[code] = a
                a.append(concept)

    return concept_codes, code_concepts


def get_concepts_dict():
    """
    得到股票概念字典
    :return: concept_codes, code_concepts
    """
    key = 'concepts'
    data = daily_cache.get(key)
    if data is None:
        status, text = fetcher.http_get_text(CONCEPTS_FILE)
        if status == 200 and len(text) > 0:
            concept_codes, code_concepts = parse_concepts_compact_text(text)
            if len(concept_codes) > 0:
                data = concept_codes, code_concepts
                daily_cache.set(key, data)

    return data


def get_concepts_list(black_list=None):
    """
    得到股票所有概念列表
    :param black_list: 概念黑名单
    :return:
    """
    concept_codes, code_concepts = get_concepts_dict()
    concepts = list(concept_codes.keys())

    if black_list is not None and len(black_list) > 0:
        for concept in black_list:
            try:
                concepts.remove(concept)
            except ValueError:
                pass

    return concepts


def get_concepts_list_no_black():
    """
    去除常见黑名单之后的概念列表
    :return:
    """
    return get_concepts_list(black_list=CONCEPTS_BLACK_LIST)


def get_concepts(stock, black_list=None):
    """
    得到股票所属概念数组
    :param stock:
    :param black_list: 概念黑名单
    :return:
    """
    concept_codes, code_concepts = get_concepts_dict()
    try:
        concepts = code_concepts[stock]

        if black_list is not None and len(black_list) > 0:
            for concept in black_list:
                try:
                    concepts.remove(concept)
                except ValueError:
                    pass

        return concepts
    except KeyError:
        return None


def get_concepts_no_black(stock):
    """
    去除常见黑名单之后的股票所属概念数组
    :param stock:
    :return:
    """
    return get_concepts(stock, black_list=CONCEPTS_BLACK_LIST)
