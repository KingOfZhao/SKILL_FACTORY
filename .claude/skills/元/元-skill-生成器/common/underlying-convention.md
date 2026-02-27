# 所有 Skill 统一底层约定（执行任何 Skill 前**必须**第一步读取）

## 1. 强制执行顺序
1. 读取本文件（common/underlying-convention.md）
2. 执行 MCP 强关联检查与优先应用（必须检测 + 优先使用已连接 MCP）
3. 进行有限穷举（严格控制边界）
4. 执行核心功能（单一职责）
5. 输出前必须声明自身局限性并建议拆分 Skill（如果适用）

## 2. MCP 强关联检查与优先应用（核心规则）
- **步骤**：
  1. 识别 Skill 是否涉及外部能力（文件读写、网络请求、数据库操作、GitHub 操作、浏览器自动化、设备访问等）
  2. 通过关键词匹配 + 语义判断强关联 MCP 类型  
     示例：  
     - file / write / read / path → filesystem MCP  
     - api / github / repo / pr → GitHub MCP  
     - browser / web / dom / playwright → Playwright MCP  
     - database / sql / query → Postgres / Supabase 等 MCP  
  3. 如果检测到强关联：
     - **优先应用已连接的优质 MCP**：  
       如果对应 MCP 已连接（Claude 可自动发现其工具、资源、提示），则在执行核心功能时**强制优先使用**该 MCP 来实现操作（例如自动读写文件、调用 GitHub API、执行浏览器任务等）。  
       使用时应在输出中明确标注：“已使用 [MCP 名称] 执行 [具体操作]”。
     - **自动检测连接状态**：  
       如果未检测到对应 MCP 已连接，则立即回复清晰错误 + 强引导：  
       “本 Skill 需要 [具体 MCP 名称，例如 filesystem MCP] 来完成核心功能。目前未检测到该 MCP 已连接。  
       请在终端执行以下命令添加（或在 Claude Code 设置 > MCP 中手动添加）：  
       claude mcp add [mcp-name] --transport http [url 或 localhost:port]  
       示例：claude mcp add filesystem --transport http http://localhost:你的端口  
       是否继续无 MCP 模式（仅输出描述性建议，不实际执行外部操作）？（y/n）”
  4. 如果用户确认继续无 MCP 模式，则降级为“纯描述 + 手动操作建议”输出，并在 Limitations 中声明：“完整功能依赖 [MCP 名称] 已连接，目前处于降级模式。”
- **禁止**：Skill 自身不得尝试安装、启动或修改任何 MCP server（安全风险）
- **目标**：最大化利用已连接 MCP，实现结构化、可执行输出；未连接时不卡死，提供明确下一步行动。

## 3. 禁止事项（核心保护规则）
- **严禁**在运行过程中修改、追加、覆盖本文件 underlying-convention.md
- **严禁**修改自身 SKILL.md、description.md 等元文件
- 任何对底层约定或能力定义的优化/修复，**只能**通过用户指定的“修复/优化 Skill”来完成
- 违反以上规则 → 立即停止并报告：“检测到自我修改企图，已终止”

## 4. 通用最佳实践（所有 Skill 必须遵守）
- 单一职责原则：一个 Skill 只解决一个明确问题域
- 文件夹命名：纯英文 kebab-case（小写字母 + 连字符，例如 skill-generator、flutter-layout-builder）  
  - 推荐元 Skill 使用 meta- 前缀（meta-skill-optimizer）或 元- 前缀（元-skill-optimizer）  
  - 强烈建议避免中文文件夹名（兼容性更好）  
  - 避免 "er" 后缀（如 optimizer 而非 优化er）
- SKILL.md 控制在 400 行以内
- 所有脚本必须 JSON 输入输出 + 全面错误处理（try/except）
- 生成器类 Skill：输出自动存入 待应用-skill/
- 在 README.md 或 Limitations 中记录自身已知缺陷/局限（参考优质实践）

## 5. 强制质量要求：10分钟可验证原则（分层适用）

- **适用范围**：**非元 Skill**  
  （即普通任务型 Skill，不以“元-”开头，且不属于生成器、元认知、结构化认知、穷举器、profiler 等元级类别）

  必须严格遵守“10分钟验证”条件，即：  
  一个中等经验的开发者能够在 10 分钟内，通过低成本、明确的操作，独立判断输出是否正确、是否达到预期质量。

  具体要求：
  - 输出必须采用可直接对比/运行/检查的格式（diff、代码文件、JSON、报告、构建物等）
  - 提供 ≤ 5 步的快速验证路径（总耗时 ≤ 10 分钟）
  - 优先包含自带校验机制（校验脚本、checksum、成功标志、样例对比等）
  - 失败场景也应在短时间内明显可判（清晰报错、缺失关键部分）
  - SKILL.md 或 README 中**必须**包含一个独立的“快速验证指南”小节，列出最快 1–3 种检查方式及预期结果

- **豁免范围**：**元 Skill**  
  （名称以“元-”开头，或明确为生成器、元认知、结构化认知、穷举器、profiler 等元级 Skill）

  不强制遵守“10分钟验证原则”。  
  输出以可阅读、可后续应用、结构化认知积累为主要目标（模板、流程、proposal、checkpoint、建议树等），其价值在于体系化、可扩展性，而非立即动手验证。

**判断依据**（生成器应自动识别并标记）：
- Skill 文件夹名称是否以“元-”开头
- SKILL.md 的 name 或 description 是否包含“元”“meta”“generator”“enumerator”“profiler”等关键词

违反适用范围规则的 Skill 被视为不合格，应优先通过修复/优化 Skill 改进，或拆分成更小的、可独立验证的子 Skill。

目的：平衡元层设计自由度与普通 Skill 的可信度、可快速迭代性。

## 6. 本约定为只读约定
本文件内容由人类（赵先生）或专用修复 Skill 维护。Skill 自身无权更改。

永久有效，所有 Skill 必须严格遵守。

## 7. 机器可读规则块（新增 - 供检查器、优化器等元 Skill 解析使用）

```yaml
rules:
  skill_type:
    meta_prefix: ["元-", "meta-"]
    meta_keywords: ["生成器", "generator", "enumerator", "profiler", "检查器", "扫描器", "穷举器", "修复器", "优化器"]
    non_meta: "普通任务型 Skill"

  naming:
    pattern: "^[a-z0-9]+(-[a-z0-9]+)*$"
    forbidden_suffix: ["er", "器"]
    recommended_meta_prefix: "元-"

  skill_md:
    max_lines: 400

  validation:
    enabled_for: "non_meta_only"
    must_have_section: "10 分钟快速验证指南|快速验证指南"
    max_steps: 5
    max_time_minutes: 10
    must_have_verify_mechanism: true

  mcp:
    must_check: true
    must_use_if_connected: true

  skill_chain:
    full_chain:
      - name: "问题穷举器"
        next: "生成器"
      - name: "生成器"
        next: "扫描器"
      - name: "扫描器"
        next: "检查器"
      - name: "检查器"
        next: "优化器"
      - name: "优化器"
        next: null

    auto_trigger:
      after_generator: ["扫描器", "检查器", "优化器"]

  optimizer_modes:
    auto_apply:
      description: "自动应用 Skill 优化（危险模式，慎用）"
      requires_confirmation: true
      generates_diff: true
    dry_run:
      description: "仅预览所有修改（默认模式）"
      requires_confirmation: false
      generates_diff: false
```