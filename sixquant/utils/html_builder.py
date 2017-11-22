# coding=utf-8


def html_get_pt_price_color(pt_price):
    if pt_price >= 8:
        return 'bcr7'
    if pt_price >= 5:
        return 'bcr5'
    if pt_price >= 3:
        return 'bcr3'
    if pt_price >= 1:
        return 'bcr1'

    if pt_price <= -8:
        return 'bcg7'
    if pt_price <= -5:
        return 'bcg5'
    if pt_price <= -3:
        return 'bcg3'
    if pt_price <= -1:
        return 'bcg1'

    return 'bcr0'
