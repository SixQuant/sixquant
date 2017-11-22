# coding=utf-8

from .html_builder import html_get_pt_price_color

_HTML_HEADER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
{refresh}
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="">
<meta name="author" content="">
<link rel="icon" href="/favicon.ico">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.cainiaotouzi.cn/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdn.cainiaotouzi.cn/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="https://cdn.cainiaotouzi.cn/css/dashboard.css">
<link rel="stylesheet" href="https://cdn.cainiaotouzi.cn/css/finance.css">
</head>
<body>

<nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
                    aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">菜鸟投资</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav navbar-right">
                <li><a href="#">帮助</a></li>
            </ul>
            <form class="navbar-form navbar-right">
                <input type="text" class="form-control" placeholder="搜索...">
            </form>
        </div>
    </div>
</nav>

<div class="container-fluid">
    <div class="row">
        <div class="col-sm-12 col-md-12 main">

"""

_HTML_FOOTER = """
        </div>
    </div>
</div>

<script src="https://cdn.cainiaotouzi.cn/js/jquery.min.js"></script>
<script src="https://cdn.cainiaotouzi.cn/js/bootstrap.min.js"></script>
<!--[if lt IE 9]>
<script src="/js/html5shiv.min.js"></script>
<script src="/js/respond.min.js"></script>
<![endif]-->
</body>
</html>
"""

_TABLE_HEADER = """
<div class="table-responsive">
    <table class="table table-striped">
"""

_TABLE_FOOTER = """
        </tbody>
    </table>
</div>
"""


def dataframe_to_html(df, title, refresh=0):
    """
    将 DataFrame 输出成 html
    :param df:
    :param title:
    :param refresh: 是否自动刷新（秒）
    :return:
    """
    refresh = ('<meta http-equiv="refresh" content="{secs}">'.format(secs=refresh)) if refresh > 0 else ''
    html = _HTML_HEADER.format(title=title, refresh=refresh)
    html += '<h2 class="sub-header">{title}</h2>'.format(title=title)
    html += _TABLE_HEADER
    html += '<thead><tr>'
    html += '<th>{column}</th>'.format(column=df.index.name)
    for column in df.columns:
        html += '<th>{column}</th>'.format(column=column)
    html += '</tr></thead><tbody>'
    n = len(df.columns)
    for stock, r in df.iterrows():
        try:
            pt_price = r['涨幅']
        except KeyError:
            try:
                pt_price = r['pt_price']
            except KeyError:
                pt_price = 0

        color = html_get_pt_price_color(pt_price)
        html += '<tr>'
        html += '<td class="' + color + '">{value}</td>'.format(value=stock)
        for i in range(n):
            if df.columns[i] in ['股票名称']:
                html += '<td class="' + color + '">{value}</td>'.format(value=r[i])
            elif df.columns[i] in ['涨幅', '震幅', '换手', '换手率']:
                html += '<td class="' + color + ' text-right">{value}%</td>'.format(value=r[i])
            else:
                html += '<td class="' + color + ' text-right">{value}</td>'.format(value=r[i])

        html += '</tr>\n'
    html += _TABLE_FOOTER
    html += _HTML_FOOTER

    return html


def dataframe_to_html_file(df, filename, title, refresh=0):
    """
    将 DataFrame 输出成 html 文件
    :param df:
    :param filename:
    :param title:
    :param refresh: 是否自动刷新（秒）
    :return:
    """
    html = dataframe_to_html(df=df, title=title, refresh=refresh)
    with open(filename, 'w') as html_file:
        html_file.write(html)
