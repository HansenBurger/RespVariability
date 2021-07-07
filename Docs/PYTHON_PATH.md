# Vscode中Python包同级调用问题整理

## 1.问题分析

### 1.1 主要问题

如图

```shell
.
└── Project
    ├── A
    │   ├── a1.py
    │   ├── a2.py
    │   └── __init__.py
    ├── B
    │   ├── b1.py
    │   └── b2.py
    └── test.py

```

同级文件B中的.py文件无法直接调用module A中的方法，会出现如下的错误。

```shell
ModuleNotFoundError: No module named 'A'
```

### 1.2 主要原因

vscode中的python extension会动态的添加当前文件的上层目录到PYTHONPATH。

有关python环境配置问题的官方文档[Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)。

## 2.解决办法

### 2.1 更换IDE

pycharm默认情况下会将项目的根目录添加到PYTHONPATH。

---

优点：方便一步到位

缺点：更改IDE切换使用习惯

---

### 2.2 代码导入

PYTHONPATH中的内容也存在sys.path中，可以通过调用内置的模块os和sys来导入。

通过向sys.path中增加上层目录来解决。

```python
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
```

简化变量后

```python
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
```

避免出现命名冲突还可以使用sys.path.insert，具体的使用方法可以参考[Python: Import module from parent directory](https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/)。

---

优点：对于单一文件的导入问题解决有效方便成本低

缺点：每个文件中都要增加代码量，相对笨拙

---

### 2.3 安装包

通过设置setup文件，基于项目目录创建venv，并安装到对应需要的依赖库。

详细内容可以参考[Tired of sys.path hacks?](https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944)。

---

优点：避免一次次的使用sys.path添加

缺点：没试验过，但是做成包安装对于仍要测试的方法还是存在不确定性

---

### 2.4 使用.env外部导入

通过在launch.json文件中设置env信息，来导入外部的包和库，这是官方文档中提到的一种方法。

主要通过在.env文件内增加自定义库的路径，然后修改launch.json以及setting中的信息实现调用。

相关参考文档：

1.[彻底解决VScode中采用pythonimport自定义模块显示unresolvedimport问题和无法跳转到自定义模块函数定义](http://www.cxyzjd.com/article/fdd096030079/107763444)

2.[How to correctly set PYTHONPATH for Visual Studio Code](https://newbedev.com/how-to-correctly-set-pythonpath-for-visual-studio-code)

3.[vscode import error for python module](https://stackoverflow.com/questions/46520127/vscode-import-error-for-python-module)

但根据以上的几种方案实验，没有成功，如果只是去除调用的warning问题，可以通过在setting.json中添加以下语句解决。

```json(current_loc.parents[0]
{
    "python.autoComplete.extraPaths": ["./src"]
}
```

其中src为存放自定义module的路径，具体可以参考[Troubleshooting](https://github.com/microsoft/python-language-server/blob/master/TROUBLESHOOTING.md#common-questions-and-issues)

## 3.总结

python禁止同级调用包的这个规则，一方面避免了循环调用，另一方面也对程序的设计提出了更高的要求。

## 4.补充

补充部分主要针对2.2节的代码导入方式的优化。

虽然用**os.path**的模块可以有效解决自定义module导入的问题，但越大的module和运行代码之间的层级差异，就需要越多的变量或者更长的代码，不美观占也用内存。

比如：

```shell
.
└── Project
    ├── A
    │   ├── a1.py
    │   ├── a2.py
    │   └── __init__.py
    ├── B
    │   ├── B1
    │   │   └──b1.py
    │   └── B2
    └── test.py

```

b1.py要调用module A, 使用2.2中的方法需要至少向上两个层级，三个变量。

```python
import os, sys

B1_loc = os.path.dirname(os.path.realpath(__file__))
B_loc = os.path.dirname(b1_loc)
Project_loc = os.path.dirname(B1_loc)
sys.path.append(Project_loc)
```

如果使用**pathlib**这个自带库，就能通过**parents**的模块，切割路径，实现不同层级切换

```python
import pathlib, sys

B1_loc = pathlib.Path.cwd()
Project_loc = B1_loc.parents[1]
sys.path.append(str(Project_loc)) # 需要注意添加到sys.path中的对象必须是字符串形式
```

简化后可以是

```python
import pathlib, sys

sys.path.append(str(pathlib.Path.cwd().parents[1]))
```

参考文档：

1. [华丽的蜕变-使用Pathlib模块,文件操作So Easy！](https://zhuanlan.zhihu.com/p/68197380)

2. [你应该使用pathlib替代os.path](https://zhuanlan.zhihu.com/p/87940289)