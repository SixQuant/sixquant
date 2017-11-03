# coding=utf-8

import sixquant as fq

global first
first = True


def get_top_up(n):
    df = fq.get_day_today_quote(fields=['close', 'amount', 'pt_price', 'pt_ampl', 'pt_turn'], dropna=True)

    # 换手10%及以上，或涨幅5%及以上，或震幅5%及以上
    df = df.query('pt_price>0 and (pt_price>5 or pt_ampl>5 or pt_turn>10)')[:n]
    df = df.sort_values(by=['pt_turn', 'pt_price', 'pt_ampl'], ascending=[False, True, True])

    df['name'] = df.index.map(lambda x: fq.get_stock_name(x))
    df['amount'] = (df['amount'] / 10000.0).round(2)  # 成交额(万)
    df = df[['name', 'close', 'amount', 'pt_price', 'pt_ampl', 'pt_turn']]

    df.rename(columns=lambda x: '股票名称' if x == 'name' else x, inplace=True)
    df.rename(columns=lambda x: '最新价' if x == 'close' else x, inplace=True)
    df.rename(columns=lambda x: '成交额（万元）' if x == 'amount' else x, inplace=True)
    df.rename(columns=lambda x: '涨幅' if x == 'pt_price' else x, inplace=True)
    df.rename(columns=lambda x: '震幅' if x == 'pt_ampl' else x, inplace=True)
    df.rename(columns=lambda x: '换手率' if x == 'pt_turn' else x, inplace=True)

    return df


def callback():
    global first
    if first or fq.is_trading_time():
        first = False
        df = get_top_up(50)
        print(df.head(5))
        df.to_html('top_up_50.html')


timer = fq.Timer(interval=5, callback=callback, async=False)
timer.start()
