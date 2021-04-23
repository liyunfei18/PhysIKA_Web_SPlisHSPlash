# PhysIKA_Web_SPlisHSPlash

+ 该工程为PhysIKA_Web中流体模拟方法所用的流体仿真框架
+ git clone之后，cmd进入到工程目录下并输入
```shell script
python setup.py build_ext
```
+ 工程生成完毕后，在生成的 build 文件夹中的 lib.win-amd64-* 文件夹中可以找到pyd文件，
+ 将工程目录下的 sph_run.py 拷贝到pyd目录中，
+ 最后使用 sph_run.py 文件的绝对路径更新PhysIKA_Web工程中pathconfig.json配置文件中的对应内容即可。
+ 注意：该工程部分内容需要cuda，目前只测试过cuda10.1版本，其他版本可能存在问题。
