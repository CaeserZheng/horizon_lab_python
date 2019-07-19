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
    ├── example
    ├── log
    │   ├── deviceManeger_space_record.log
    │   └── intelligentService_facesets_record.log
    ├── services
    │   ├── __init__.py
    │   ├── analysisTools
    │   │   └── __init__.py
    │   ├── deviceManager
    │   │   ├── __init__.py
    │   │   ├── device.py
    │   │   ├── passengerflow.py
    │   │   └── space.py
    │   └── intelligentService
    │       ├── __init__.py
    │       ├── facei.py
    │       ├── facesets.py
    │       └── faceu.py
    ├── test
    │   ├── __init__.py
    │   ├── deviceManager
    │   │   └── test.py
    │   ├── intelligentService
    │   │   └── test.py
    │   ├── test_param_cfg.py
    │   └── utils.py
    └── utils.py

</pre>

####记录
- 2019.07.18 测试 attributes 参数
    - TODO 文档请求范例有问题，https://iotdoc.horizon.ai/busiopenapi/part2_api_devices/device.html#part2_3

- 2019.07.18 测试智能服务
    - TODO 文档站错误比较多，整理集中反馈
    
- 2019.07.19 
    - 尝试些测试类
    - 添加.gitignore
    - 隐匿ak、sk
    
- 2019.07.19 
    - 添加人脸识别
    - TODO 智能分析模块