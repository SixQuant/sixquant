# SixQuant



## 架构设计

### 角色
* 四个角色：实时数据服务器、历史数据生成者、第三方CDN服务器、客户端
  - 实时数据服务器：提供实时数据服务，可以有多个
  - 历史数据生成者：按年、月、日生成历史数据文件，可以有多个生成者
  - 第三方CDN服务器：负责文件分发，减少服务器压力
  - 客户端：缓存历史数据，请求实时数据，整合后提供数据服务

### 数据同步
* 实时数据通过 HTTP 请求从服务器实时获得
* 历史数据通过文件下载后合并到本地数据库
* 同步过程
  - 数据生成者盘后整理完历史数据后生成文件上传到第三方 CDN 服务器
  - 客户端定时判断如果历史数据不完整则定时轮训并下载历史数据
  - 客户端下载到数据后合并到本地缓存数据库中
  - 客户端启动后，异步线程会每日会对历史数据进行一次校验，以应对可能的服务器数据错误需要重新下载正确数据

### bundle
- 

### 客户端数据库设计（数据库引擎采用 SQLite3）
* basic_name(名称) 
	- date DATE NOT NULL,
	- code VARCHAR(10) NOT NULL,
  - name VARCHAR(8) NOT NULL,

* day(日线数据) 
	- date DATE NOT NULL,
	- code VARCHAR(10) NOT NULL,
	- open FLOAT,
	- close FLOAT,
	- high FLOAT,
	- low FLOAT,
	- volume FLOAT,
	- amount FLOAT,
	- factor FLOAT
	- pe FLOAT

### 客户端数据库表改进
- code 字段采用字符串是否会稍微影响性能，改成数字？