# S01 — Python 环境与 smoke test：让"可导入"成为可验证的事实

> 完成状态：DONE  
> 日期：2026-11-06  
> 关联 Roadmap：S01  
> 本次使用的 pstack 工作流：实际调用 `/pstack:poteto-mode`，匹配 **Feature** playbook。应用的原则：Laziness Protocol、Test Behavior Not Implementation、Prove It Works。跳过的环节及原因见第 2 节末尾。  
> 代码版本：当前工作树。目录**不是 git 仓库**（未执行 `git init`），因此没有 commit hash 可引用。

## 1. 一句话概括

这一步把 silq 从"一堆文档"变成"一个可以被安装、被导入、被测试的 Python 包"，并用一个测试证明这件事是真的。

对 Agent Runtime 的意义：后面每一步（Event 模型、状态机、评估器）的测试结论都建立在"测试导入的就是我们要发布的那份代码"这个前提上。如果这个前提不成立，后面所有的绿灯都可能是假的。Agent 工程里评估（evaluation）的可信度同样依赖可复现的环境：同一份 `uv.lock`、同一个解释器版本，才能让"baseline 成功率 vs 新方案成功率"的比较有意义。

## 2. 本步范围（做了 / 没做）

- **已实现：**
  - 用 `uv` 管理的 CPython 3.12.15 创建虚拟环境 `.venv`。
  - `src/` layout 的 Python 包 `silq`，只暴露一个常量 `__version__`。
  - 一个 `pytest` smoke test，断言模块版本与已安装分发包的元数据版本一致。
  - `ruff` lint + format 检查（默认规则集）。
  - `uv.lock` 锁定全部依赖的精确版本。
- **未实现：** 没有任何 Event / Goal / Action 逻辑，没有 CLI，没有 mypy 类型检查（**NOT CONFIGURED**），没有 CI，没有 git 仓库。
- **本步新增/修改文件：**
  - `pyproject.toml`（新增，生产配置）
  - `.python-version`（新增，生产配置）
  - `src/silq/__init__.py`（新增，生产代码，1 行）
  - `tests/test_smoke.py`（新增，测试）
  - `uv.lock`（由 `uv sync` 生成，不手写）
  - `docs/learning/S01-python-env-and-smoke-test.md`、`docs/learning/README.md`、`docs/PROGRESS.md`（文档）
- **验收条件：** 见第 6 节，`docs/PROGRESS.md` 中的 S01 checklist 全部满足。
- **pstack Feature playbook 中跳过的环节：**
  - `how`：仓库里还没有任何代码可供分析。
  - `architect`：没有跨函数边界的代码。
  - 委托 subagent 写代码、worktree 隔离：项目 `CLAUDE.md` 禁止启动后台工作，且改动只有约 20 行；此外目录不是 git 仓库，无法建 worktree。
  - `interrogate` 和独立 code review：本步设计没有争议，只做了**自我审查**。这**不是**独立审查，特此说明。
  - 开 PR：不是 git 仓库，用户也没有要求。

## 3. 心智模型（Mental Model）

关键区分：**"一个文件夹里有 `.py` 文件"** 不等于 **"一个已安装的包"**。

```text
pyproject.toml ──(uv sync)──> uv_build 构建 ──> .venv 中安装 silq 0.1.0 (editable)
      │                                              │
      │ version = "0.1.0"                            │ 写入分发元数据 (dist-info)
      ▼                                              ▼
src/silq/__init__.py                       importlib.metadata.version("silq")
  __version__ = "0.1.0"                              │
      │                                              │
      └──────────── test_smoke.py 断言两者相等 ──────┘
```

- **输入：** `pyproject.toml`（声明）、`src/silq/__init__.py`（代码）。
- **输出：** `.venv` 中一个可被 `import silq` 找到的包，以及它的元数据。
- **持久状态：** `.venv/`（可随时删除重建，已被 `.gitignore` 忽略）、`uv.lock`（应提交，保证可复现）。
- **不变量（invariant）：** 已安装包的元数据版本 == 模块代码里的 `__version__`。
- **失败情况：** 包没装上（`ModuleNotFoundError`）；装上了但版本两处不一致（`AssertionError`）；用了错误的解释器（见第 7 节）。

"editable install" 的含义：`uv sync` 把 silq 以 editable 模式安装（`uv.lock` 第 94 行 `source = { editable = "." }`）。`.venv` 里不复制源码，而是指向 `src/silq/`。所以改了源码不用重装，但**改了 `pyproject.toml` 的元数据就必须重新 sync**。`uv run` 每次运行前会自动 sync，所以这一点平时感觉不到。

## 4. 核心代码逐段解析

### 4.1 `src/silq/__init__.py:L1` — `__version__`

```python
__version__ = "0.1.0"
```

只有一行。为什么不放一个 `hello()` 函数（`uv init --lib` 的模板默认会放）？因为 roadmap 要求"一个可导入的函数**或常量**"，而 `hello()` 是一个没有任何调用者、以后一定会删掉的函数（Laziness Protocol：最小 diff，不写会被删的代码）。`__version__` 则是 Python 包的通用约定，有真实读者（用户、bug 报告、以后的 trace 记录）。

隐藏前提：这个字符串和 `pyproject.toml:L3` 的 `version = "0.1.0"` 是**同一个事实写了两遍**。这是有意接受的重复，由测试来守护，取舍见第 5 节。

### 4.2 `pyproject.toml:L1-L20` — 项目声明

```toml
[project]
name = "silq"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.6"]

[build-system]
requires = ["uv_build>=0.12.23,<0.13.0"]
build-backend = "uv_build"
```

逐段说明：

- `dependencies = []`：运行时**零依赖**。pytest 和 ruff 只是开发工具，放进 `[dependency-groups].dev`（PEP 735）。区别在于：如果以后有人 `pip install silq`，不会被迫装上 pytest。`uv sync` 默认会安装 `dev` 组。
- `[build-system]`：告诉安装器"用什么把源码变成可安装的包"。`uv_build` 是 uv 自带的构建后端，版本范围直接取自 `uv init --lib` 在本机生成的模板（先在临时目录生成，再照抄，不凭记忆猜）。`uv_build` 默认就按 `src/<包名>/` 查找模块，所以不需要额外配置包路径。
- `requires-python = ">=3.12"` 与 `.python-version` 的 `3.12` 配合：前者是"允许的范围"，后者是"本机开发时具体用哪个"。
- 故意**没有**写 `authors`：`uv init` 模板会自动填入 git 配置中的姓名和邮箱，而 `CLAUDE.md` 要求仓库中不放个人数据。

`L15-L20` 的 `[tool.pytest.ini_options] testpaths = ["tests"]` 让 pytest 只收集 `tests/`；`[tool.ruff]` 设定 `target-version = "py312"`，使 lint 规则与 `requires-python` 一致。

### 4.3 `tests/test_smoke.py:L1-L7` — 测试了哪个行为？

```python
from importlib.metadata import version

import silq


def test_installed_package_version_matches_module_version() -> None:
    assert silq.__version__ == version("silq")
```

- **Arrange：** L3 `import silq`。这一行本身就是第一个断言：如果包没装上，测试在**收集阶段**就会以 `ModuleNotFoundError` 失败。
- **Act：** 读取两个来源的版本。`silq.__version__` 来自源码；`version("silq")` 来自安装时写入 `.venv` 的分发元数据（dist-info），即来自 `pyproject.toml`。
- **Assert：** 两者相等。

为什么不写 `assert silq.__version__ == "0.1.0"`？那只是把同一个常量重抄一遍，`pyproject.toml` 改成 0.2.0 时它仍然通过，什么都没证明。根据 *Test Behavior, Not Implementation* 原则，用两种假想改动检验一个测试：

1. **破坏行为**（版本漂移）：测试必须失败。已实际验证，见第 6 节"负面测试"。
2. **只改内部实现**（例如把 `__version__` 挪到 `src/silq/_version.py` 再在 `__init__` 里 re-export）：测试应该继续通过。它确实会通过，因为它只看公开属性。

**未覆盖的边界：** 测试不能证明 `silq` 是从 `src/` 导入的，而不是从别处同名包导入的。如果 `.venv` 里恰好有另一个叫 `silq` 的包，且版本也是 0.1.0，测试仍会通过。目前靠 `uv.lock` 和手动检查 `silq.__file__` 排除这种可能（第 6 节）。

## 5. 技术原理与设计取舍

- **核心概念（术语中英对照）：**
  - 分发包（distribution）vs 导入包（import package）：前者是 `pip`/`uv` 安装的单位，有元数据；后者是 `import` 语句找到的目录。两者通常同名，但不是一回事。
  - `src` layout：源码放在 `src/silq/`，而不是仓库根目录 `silq/`。
  - 可编辑安装（editable install）：安装的是指向源码的链接，而不是一份拷贝。
  - 锁文件（lockfile）：记录依赖解析的精确结果（版本 + hash），保证可复现。

- **方案 A（采用）`src/` layout vs 方案 B flat layout（`silq/` 放根目录）：**

  | | flat layout | src layout |
  | --- | --- | --- |
  | 从仓库根目录运行 `python` 时 | 根目录在 `sys.path` 上，**不安装也能 import** | 不安装就 import 不到 |
  | 测试实际导入的代码 | 可能是源码目录，绕过了打包配置 | 一定是安装后的包 |
  | 打包配置写错（漏文件、元数据错） | 测试照样绿，发布后才炸 | 测试立刻暴露 |
  | 便利性 | 稍高 | 必须先 `uv sync`（`uv run` 自动完成） |

  第 6 节有实测：裸解释器的 `sys.path[0]` 是 `''`（当前目录），但 `import silq` 仍然失败，这正是 src layout 的保护作用。

- **方案 A（采用）版本写两遍 + 测试守护 vs 方案 B `__version__ = importlib.metadata.version("silq")`（单一来源）：**
  方案 B 消除了重复，但每次 import 都要查元数据，而且未安装时会抛 `PackageNotFoundError`。更关键的是，方案 B 下 smoke test 变成了 `version("silq") == version("silq")` 的同义反复，失去了检测能力。方案 C 是完全不要 `__version__`，只测 `import silq` 成功，更小，但测试就只剩"能导入"一个弱信号。当前阶段选 A：重复只有一处，且有测试守护。

- **方案 A（采用）uv vs 方案 B `python -m venv` + `pip`：**
  本机实测 `python` 命令指向 Microsoft Store 占位程序（见第 7 节）；`py` launcher 能找到 3.14 和 uv 管理的 3.12。uv 可以自己下载、管理解释器，按 `.python-version` 选版本，并生成跨平台锁文件。venv + pip 能用，但没有锁文件，需要手动保证解释器版本。所以选 uv。

- **为什么当前选择更适合这个阶段：** 零运行时依赖、一个常量、一个测试。任何更多的结构（`domain/` 目录、CLI 入口、`py.typed`）现在都没有使用者。

- **将来什么时候可能需要改：** 有了第二个需要版本号的地方（如 trace 记录里写入运行时版本）时，可以考虑单一来源方案；对外发布类型提示时加 `py.typed`；需要类型检查时（预计 S02 引入类型较多后）配置 mypy 或 pyright。

## 6. 验证证据（不可虚构）

**环境探测（Windows PowerShell 5.1.26100.9818）：**

```powershell
python --version
py -0p
uv --version
uv python list --only-installed
```

```text
Python was not found; run without arguments to install from the Microsoft Store, ...
 -V:3.14[-64] *   C:\Users\<user>\AppData\Local\Python\pythoncore-3.14-64\python.exe
 -V:Astral\CPython3.12.15 C:\Users\<user>\AppData\Roaming\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe
uv 0.12.23 (46b84fd0b 2026-10-03 x86_64-pc-windows-msvc)
cpython-3.14.7-windows-x86_64-none   ...
cpython-3.12.15-windows-x86_64-none  ...
```

（用户目录名已替换为 `<user>`。）

**TDD 红灯（`__init__.py` 为空时）：**

```powershell
uv sync
uv run pytest -q
```

```text
>       assert silq.__version__ == version("silq")
               ^^^^^^^^^^^^^^^^
E       AttributeError: module 'silq' has no attribute '__version__'
FAILED tests/test_smoke.py::test_installed_package_version_matches_module_version
1 failed in 0.07s
```

红灯的内容就是预期的那个原因（属性不存在），而不是构建失败或收集错误。

**绿灯 + lint：**

```powershell
uv run pytest -v
uv run ruff check .
uv run ruff format --check .
```

```text
platform win32 -- Python 3.12.15, pytest-9.2.0, pluggy-1.7.0 -- C:\dev\silq\.venv\Scripts\python.exe
configfile: pyproject.toml
testpaths: tests
tests/test_smoke.py::test_installed_package_version_matches_module_version PASSED [100%]
============================== 1 passed in 0.02s ==============================
All checks passed!
17 files already formatted
```

"17 files" 的来源已核实：`ruff check --show-files` 只列出 `pyproject.toml`、`src/silq/__init__.py`、`tests/test_smoke.py`；`ruff format` 0.17.4 额外检查了 15 个 Markdown 文件中的 Python 代码块，没有修改任何文件。

**负面测试（版本漂移）：** 临时把 `pyproject.toml` 改为 `version = "0.2.0"`，运行后恢复。

```text
E       AssertionError: assert '0.1.0' == '0.2.0'
FAILED tests/test_smoke.py::test_installed_package_version_matches_module_version
DRIFT_EXIT=1
...（恢复后）
1 passed in 0.02s
RESTORED_EXIT=0
```

**src layout 实验：** 用 uv 管理的裸 3.12 解释器（不在 `.venv` 中，没有安装 silq），在仓库根目录运行：

```powershell
$bare = uv python find --no-project --system 3.12
& $bare -c "import sys; print(repr(sys.path[0])); import silq"
& $bare -c "import sys; sys.path.insert(0, 'src'); import silq; print(silq.__version__)"
```

```text
''
ModuleNotFoundError: No module named 'silq'
BARE_EXIT=1
0.1.0
SRC_ON_PATH_EXIT=0
```

当前目录（`''`）在 `sys.path` 上，`import silq` 仍然失败。只有安装或手动把 `src` 加到路径才能导入。

**干净重装：** 删除 `.venv` 后按锁文件严格重建。

```powershell
Remove-Item -Recurse -Force .venv
uv sync --locked
uv run pytest -q
uv run ruff check .
```

```text
Using CPython 3.12.15
Creating virtual environment at: .venv
Resolved 8 packages in 1ms
Installed 8 packages in 516ms
 + colorama==0.4.6
 + iniconfig==2.3.1
 + packaging==26.3
 + pluggy==1.7.0
 + pygments==2.21.0
 + pytest==9.2.0
 + ruff==0.17.4
 + silq==0.1.0 (from file:///C:/dev/silq)
SYNC_EXIT=0
1 passed in 0.01s
All checks passed!
```

另有一条 uv 警告 `Failed to hardlink files; falling back to full copy`：uv 缓存与项目不在同一文件系统时出现，只影响安装速度，不影响正确性。

- **通过：** pytest（1 passed）、ruff check、ruff format --check、`uv sync --locked`。
- **未配置：** 类型检查（mypy/pyright）**NOT CONFIGURED**；CI **NOT CONFIGURED**。
- **负面测试：** 版本漂移被捕获；未安装时 import 失败。
- **已知限制：** 目录不是 git 仓库；只有一个测试；`ruff` 只用默认规则集（E4/E7/E9/F）。

## 7. 工程师视角：故障模式与排查

**失败案例一：`python` 不是你以为的那个 Python。**
本机执行 `python --version` 得到的是 `Python was not found; run without arguments to install from the Microsoft Store`。`Get-Command python` 显示它位于 `...\WindowsApps\python.exe`，这是 Windows 的 "App execution alias" 占位程序，不是解释器。

- 为什么会发生：Windows 11 默认在 PATH 前部放这个占位程序，引导用户去应用商店安装。
- 后果：如果文档写 `python -m pytest`，在这台机器上会直接失败；在另一台机器上可能静默使用一个完全不同版本的 Python。
- 目前如何处理：所有命令都通过 `uv run` 执行，由 `.python-version` 决定解释器；pytest 输出首行 `Python 3.12.15 ... C:\dev\silq\.venv\Scripts\python.exe` 可以直接确认用的是哪一个。
- 还缺什么：没有自动检查拦截"有人绕过 uv 直接调用 `python`"。

**失败案例二：验证方法本身出错（本次实际踩到）。**
为了演示 src layout，我第一次用了 `uv run --no-project python -c "import silq"`，预期失败，结果却**成功了**（exit 0）。打印 `sys.executable` 后发现：`--no-project` 只是不读 `pyproject.toml`，但仍会使用当前目录下已存在的 `.venv`，而 silq 已经装在里面。改用 `uv python find --no-project --system 3.12` 找到的裸解释器后，才得到正确的 `ModuleNotFoundError`。

教训：当验证结果与预期不符时，**先怀疑观察方法，再怀疑系统**。这一点在后续 Agent 评估中非常重要：评估器（evaluator）本身也可能有 bug，一个"通过率 100%"的结果首先要问"这个评估器能不能失败"。上面的版本漂移负面测试就是在回答"这个测试能不能失败"。

## 8. 知识回顾（Teach-back）

1. 如果把 `src/silq/` 移到仓库根目录 `silq/`（flat layout），并且忘记在 `pyproject.toml` 里正确配置打包，`uv run pytest` 还会通过吗？为什么这对"测试结论可信"是个问题？
2. `tests/test_smoke.py` 为什么断言 `silq.__version__ == version("silq")`，而不是 `silq.__version__ == "0.1.0"`？请分别用"破坏行为"和"只改内部实现"两种假想改动来论证。

<details>
<summary>参考答案（先自己回答再看）</summary>

1. 取决于调用方式，而"取决于调用方式"本身就是问题所在（本题为推理，本步未实测 flat layout）。用 `python -m pytest` 时，Python 会把当前目录放进 `sys.path`，`import silq` 直接找到根目录下的源码，完全绕过安装步骤；用 `pytest` 入口脚本时则不一定。也就是说，同一份代码在不同命令下可能一绿一红。于是打包配置的错误（漏掉文件、元数据错误）不会被测试发现，直到别人安装发布包时才暴露。src layout 让"不安装就导入不到"，强制测试走和真实用户相同的路径。第 6 节的实验证明了这一点：当前目录在 `sys.path` 上，`import silq` 仍失败。
2. 破坏行为：把 `pyproject.toml` 的版本改成 0.2.0 而忘了改源码。`== "0.1.0"` 的写法仍然通过，等于什么都没测；`== version("silq")` 的写法失败（实测 `AssertionError: assert '0.1.0' == '0.2.0'`）。只改内部实现：把版本常量挪到 `_version.py` 再 re-export，两种写法都通过，所以两者都不绑定实现。只有第二种同时满足"能抓到破坏"和"不怕重构"。

</details>

**动手练习：** 在 PowerShell 中运行下面的命令，观察 editable install 的效果，然后自己解释为什么第二次输出变了，却**不需要**重新 `uv sync`：

```powershell
uv run python -c "import silq; print(silq.__version__, silq.__file__)"
# 手动把 src/silq/__init__.py 改成 __version__ = "9.9.9"，再运行：
uv run python -c "import silq; print(silq.__version__, silq.__file__)"
uv run pytest -q   # 预期：失败，'9.9.9' != '0.1.0'。看完记得改回 "0.1.0"
```

追加思考：如果反过来只改 `pyproject.toml` 的版本，为什么 `uv run` 会重新构建 silq？（提示：editable install 链接的是源码，而元数据是构建时生成的。）

## 9. 下一步（仅提议，未实施）

- Next: **S02** — `Event` identity, source and timezone-aware timestamp type（Event 的身份、来源与带时区时间戳类型）。
- 前置知识：Python `datetime` 的 naive 与 aware 区别；`zoneinfo`；为什么"存储用 UTC、展示用用户时区"。
- 待决定（S02 时讨论，本步不实施）：是否引入 Pydantic，还是先用 `dataclass(frozen=True)` + 显式校验。
- 建议（非 roadmap 步骤）：在 S02 之前执行 `git init` 并提交 S01，以便后续报告引用 commit hash。需要你的确认。
- 等待用户确认：**是**
