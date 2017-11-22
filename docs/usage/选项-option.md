## 选项 option

option 用于设置用户自定义选项

选项包括

* 本地数据路径 option.set_data_path

#### 本地数据路径

本地数据路径用于存储缓存在本地的各种数据，缺省为 当前用户主目录/.sixquant，用户也可以重新设置。

```python
import sixquant as sq
# 打印本地数据路径
print(sq.get_data_path())
```

#### 

方法一：通过环境变量 SIXQUANT_DATA_DIR 重新设置本地数据路径

```bash
export SIXQUANT_DATA_DIR=/Volumes/Cloud/DataSet/sixquant
```

#### 

方法二：通过代码重新设置本地数据路径

```
import sixquant as sq
sq.set_data_path('data')
```

#### 
