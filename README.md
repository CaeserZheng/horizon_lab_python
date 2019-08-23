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
    │   ├── deviceManeger_device
    │   │   └── record.log
    │   ├── deviceManeger_passengerflow
    │   │   └── record.log
    │   └── deviceManeger_space
    │       └── record.log
    ├── services
    │   ├── __init__.py
    │   ├── deviceManager
    │   ├── iDevices
    │   │   ├── __init__.py
    │   │   ├── device.py
    │   │   ├── passengerflow.py
    │   │   └── space.py
    │   ├── iServices
    │   │   ├── __init__.py
    │   │   ├── faced.py
    │   │   ├── facesets.py
    │   │   └── faceu.py
    │   ├── iTools
    │   │   ├── __init__.py
    │   │   └── passengerflow.py
    │   └── intelligentService
    ├── test
    │   ├── __init__.py
    │   ├── iDevice
    │   │   ├── test_device.py
    │   │   ├── test_passengerflow.py
    │   │   └── test_space.py
    │   ├── iService
    │   │   ├── test_faced.py
    │   │   ├── test_facesets.py
    │   │   └── test_faceu.py
    │   ├── test.py
    │   ├── test_param_cfg.py
    │   └── utils.py
    ├── test.py
    ├── utils.py
    └── ws
        ├── __init__.py
        └── get_visitor_by_ws.py

</pre>

####记录
- 2019.07.18 测试 attributes 参数
    - TODO 文档请求范例有问题，https://iotdoc.horizon.ai/busiopenapi/part2_api_devices/device.html#part2_3

- 2019.07.18 测试智能服务
    - TODO 文档站错误比较多，整理集中反馈
    
- 2019.07.19 
    - 尝试写测试类
    - 添加.gitignore
    - 隐匿ak、sk
    
- 2019.07.19 
    - 添加人脸识别
    - TODO 智能分析模块
    
- 2019.07.21 
    - TODO 实现websocket client ，接受服务端推送
    
- 2019.07.22
    - 添加pf_visitors_recv.py  使用ws 接收服务端推送