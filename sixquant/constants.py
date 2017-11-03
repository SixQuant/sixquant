# coding=utf-8

INDEX_SH = 'IDX.000001'  # 上证指数
INDEX_SZ = 'IDX.399001'  # 深证成指
INDEX_CY = 'IDX.399006'  # 创业板指
INDEX_SH50 = 'IDX.000016'  # 上证50
INDEX_HS300 = 'IDX.000300'  # 沪深300

INDEXS = [INDEX_SH, INDEX_SZ, INDEX_CY, INDEX_SH50, INDEX_HS300]
INDEX_NAMES = ['上证指数', '深证成指', '创业板指', '上证50', '沪深300']

# =========================================================

THRESHOLD_SMALL_CAP = 20 * 10000 * 10000  # 小市值阈值，流通市值（20亿）

# =========================================================

DATA_SERVER_URL = 'http://fox.cainiaotouzi.cn/api'

HOLYDAYS_FILE = DATA_SERVER_URL + '/holydays'

BASICS_FILE = DATA_SERVER_URL + '/basics'

CONCEPTS_FILE = DATA_SERVER_URL + '/concepts'

TODAY_FILE = DATA_SERVER_URL + '/today'

TODAY_SMALL_FILE = DATA_SERVER_URL + '/today/small'
TODAY_SMALL_NO_ST_NO_SUBNEW_FILE = DATA_SERVER_URL + '/today/small_no_st_no_subnew'

TODAY_QUOTE_FILE = DATA_SERVER_URL + '/today/quote'
TODAY_MONEY_FILE = DATA_SERVER_URL + '/today/money'

# =========================================================

BUNDLE_SERVER_URL = 'http://oyiztpjzn.bkt.clouddn.com/'
