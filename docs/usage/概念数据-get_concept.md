## 概念数据-get_concept*

get_concept* 函数用于股票概念数据

```
import sixquant as sq

concepts = get_concepts_no_black('002136')

print(type(concepts))
print(concepts)
```

输出：

    <class 'list'>
    ['锂电池', '钛白粉']
### 使用举例

#### 获得股票所有概念列表

```python
concepts = sq.get_concepts_list()
```

#### 获得去除常见黑名单之后的概念列表

```python
concepts = sq.get_concepts_list_no_black()
```

#### 获得单只股票所属概念数组

```python
# 可能返回空数组[]
concepts = get_concepts_no_black(stock)
```

#### 获得单只股票所属概念数组(推荐)

```python
# 可能返回空数组[]
concepts = get_concepts_no_black(stock)
```

