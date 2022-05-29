
# wind

**Wind是一款面向云的高性能、高效率以及高扩展性的分布式游戏服务器引擎**。Wind利用Python语言的简洁语法以及丰富的生态库来提高游戏业务的开发效率，针对一些对性能有要求的游戏业务功能(如实时战斗功能)，Wind利用Golang的高并发特性来保证服务的高性能，同时Wind使用kubernetes部署并接入云组件来保证服务在云上自动伸缩，有效的分配云上公共资源，提高服务资源的利用率。

![wind run](doc/WindLogo.png)

# 为什么存在

游戏界有Unity和Unreal这样完善并且开箱即用的客户端引擎，这样的引擎大大缩短了游戏的开发周期，基本上一天就能做一个能跑的游戏。但是却并不存在一款大家熟知分布式服务器引擎，这样的服务器引擎可以快速上手并且能满足游戏生命周期各个阶段的开发需求。**Wind致力于做一款简洁、方便以及易上手的分布式服务器引擎，帮助独立游戏开发者或者中小企业快速搭建服务器框架并且开发游戏业务，降低游戏服务器的开发难度，同时将游戏服务部署在云上，节省服务成本。**

# Wind特性

- [x]  **高效率：** Wind利用Python简明的语法和生态库来编写业务量大的游戏业务逻辑，提升开发效率。
- [x]  **高性能：** Wind利用Golang来保证引擎底层功能或者实时性游戏业务的高性能。
- [x]  **高扩展性：** Wind使用组件化设计，你可以很方便的替换原有组件。
- [x]  **易上手：** Wind逻辑层使用单线程异步协程来编写业务逻辑，简单方便并且不用担心多线程锁问题。
- [x]  **在线热更新：** 目前游戏界很多使用纯Golang开发游戏服务，但Golang对热更新支持不友好，Wind组合了python动态语言，所以很好解决Golang游戏服务不能热更的问题。Wind支持在线函数级别热更新。
- [x]  **负载均衡：** 支持最大阈值选取、最小阈值选取以及随机选取算法。
- [x]  **服务发现：** 支持动态伸缩各类型服务。
- [ ]  **多协议：** 网络层支持多种不同传输协议，TCP，UDP，KCP。
- [ ]  **k8s部署与动态伸缩：** 服务层接入k8s组件，动态伸缩云上服务资源。

# Wind安装获取

- **安装Python**

Wind默认在Windows平台下开发。Wind业务逻辑使用Python编写，Golang编译成动态库供Python调用，运行前需要安装Python版本，支持Python3.7+。

Wind使用etcd做服务发现功能，使用nats做分布式消息队列，所以需要安装对应Python客户端库。在`script`目录下运行 **`install_python_requirements.bat`**  安装对应Python库。

- **获取Wind代码**

```
git clone <https://github.com/ferris1/wind.git>
```

- **启动单服务**

在`script`目录下双击运行`start_gateway.bat` 文件，启动gateway服务

- **启动分布式服务**

启动分布式服务时需要保证运行etcd服和nats服，具体运行参考官网，要不然各个服务不能合作运行。

在`script`目录下运行 `start_all.bat` 启动所有服务，目前只有两类服务，一个是Gateway服务，用于消息路由，一个是Game服务，用于处理游戏逻辑。最终分布式服务框架可以根据游戏业务自己定制，具体可以参考这篇文章[从服务器发展史看现代游戏服务器架构](https://zhuanlan.zhihu.com/p/500840594)

# 文档

[使用文档](https://www.yuque.com/yuqueyonghu2yz87x/vmgg56/mgw6gc)  

# 使用案例

[Unity3D案例视频](https://www.bilibili.com/video/BV1w541197in/)     [Unity3D案例文档](https://www.yuque.com/yuqueyonghu2yz87x/vmgg56/mudakg)  [Unity3D案例代码](https://github.com/ferris1/WindDemo)
