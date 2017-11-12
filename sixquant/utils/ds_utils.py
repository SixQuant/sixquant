# coding=utf-8

"""数据结构常用辅助函数"""


def append_if_not_exists(target, value_or_values):
    if target is None:
        if value_or_values is None:
            return None
        elif isinstance(value_or_values, list):
            target = []

    if isinstance(target, list):
        if value_or_values is None:
            return target
        elif isinstance(value_or_values, list):
            for x in value_or_values:  # 合并上用户真正想要的字段
                if x not in target:
                    target.append(x)
        else:
            x = value_or_values
            if x not in target:
                target.append(x)

        return target

    return target
