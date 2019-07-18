# 实现horizon paas 相关openapi

###SDK结构
<pre>
.
├── README.md
└── horizon
    ├── __init__.py
    ├── auth.py
    ├── compat.py
    ├── config.py
    ├── dohttp.py
    ├── services
    │   ├── __init__.py
    │   ├── analysisTools
    │   │   └── __init__.py
    │   ├── deviceManager
    │   │   ├── __init__.py
    │   │   ├── device.py
    │   │   └── space.py
    │   └── intelligentService
    │       └── __init__.py
    ├── test.py
    ├── test2.py
    ├── tmp.py
    └── utils.py
</pre>

####记录
- 2019.07.18 测试 attributes 参数
    - TODO 文档请求范例有问题，https://iotdoc.horizon.ai/busiopenapi/part2_api_devices/device.html#part2_3

- 2019.07.18 测试智能服务
    - TODO 文档站错误比较多，整理集中反馈