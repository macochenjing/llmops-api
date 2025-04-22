# -*- coding: utf-8 -*-

"""
@Time   : 2025/1/8 14:59
@Author : chenjingmaco@gmail.com
@File   : sqlalchemy.py
"""

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    """重写Flask-SQLAlchemy中的核心类，实现自动提交"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

'''
这段代码背后涉及到 Python 的几个关键机制：**上下文管理器 (`with`) + 生成器 (`yield`) + Flask-SQLAlchemy 事务封装**，我们逐层拆解说明：

---

# 🔍 一、这段代码的功能是什么？

它定义了一个自定义的事务管理器方法：  
```python
@contextmanager
def auto_commit(self):
    ...
```

目的是：**自动处理数据库事务（commit/rollback），简化业务代码中的 try/except 模式**。

---

## ✅ 使用方式是这样的：

```python
db = SQLAlchemy()

with db.auto_commit():
    user = User(name='Tom')
    db.session.add(user)
# 如果没出错，自动 commit；否则自动 rollback
```

---

# 🧠 二、关键点解析

### 1️⃣ `@contextmanager` 是什么？

它是 Python `contextlib` 标准库提供的装饰器，用于**把一个生成器（带 `yield` 的函数）变成上下文管理器**，从而支持 `with` 语句。

你可以把它理解成一种“快速写 with 的语法糖”，不需要自己写 `__enter__()` / `__exit__()` 方法。

---

### 2️⃣ `yield` 的作用是什么？

在 `@contextmanager` 中：

- `yield` 前的代码 → 在进入 `with` 块之前执行
- `yield` 后的代码 → 在 `with` 块执行完后再执行（包括异常处理）

🚩也就是说，这段代码的流程：

```python
with db.auto_commit():
    # → 进入 yield 之前：啥都不做
    # → yield：执行 with 块里的代码（数据库操作）
    # → 如果成功 → self.session.commit()
    # → 如果异常 → rollback + 抛出异常
```

这段代码相当于替你自动封装了事务处理逻辑。

---

### 3️⃣ 为什么它可以用 `with`？

因为 `@contextmanager` 把一个**生成器函数**转换成了一个**上下文管理器对象**，本质是等价于写了：

```python
class AutoCommitContext:
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, tb): ...
```

当你执行：

```python
with db.auto_commit():
```

其实就是：

```python
ctx = db.auto_commit()
ctx.__enter__()
try:
    ...  # 你的业务逻辑
finally:
    ctx.__exit__()
```

---

# ✅ 三、为什么这么设计很优雅？

### 💡 原本你可能要写很多这样的事务处理代码：

```python
try:
    user = User(name='Tom')
    db.session.add(user)
    db.session.commit()
except:
    db.session.rollback()
```

现在你可以这么写，代码更清爽、易复用：

```python
with db.auto_commit():
    db.session.add(User(name='Tom'))
```

---

# ✅ 四、完整流程图（可视化理解）

```python
@contextmanager
def auto_commit():
    try:
        yield        ← 这里执行你的 with 块中代码
        commit()
    except:
        rollback()
```

---

# 📌 总结一句话：

| 元素 | 作用 |
|------|------|
| `@contextmanager` | 把普通函数变成可用 `with` 的上下文管理器 |
| `yield` | 暂停函数执行 → 控制权让给 `with` 块内部执行 |
| `.commit()` | 如果 `with` 块成功执行，提交事务 |
| `.rollback()` | 如果出现异常，自动回滚事务 |

---

📎 bonus：你可以配合 Flask 使用这个装饰器让接口代码变得更干净：

```python
@bp.route('/register', methods=['POST'])
def register():
    with db.auto_commit():
        user = User(username='john')
        db.session.add(user)
        # 无需 try...except
```

---

如你需要，我可以再帮你：

- ✨ 改写成 async/await 支持异步事务封装  
- 🧪 添加日志、链路追踪以记录事务成功/失败  
- 📂 改造成一个通用事务装饰器函数，支持函数级别 @auto_commit 装饰器写法

要不要我帮你封装一版？
'''