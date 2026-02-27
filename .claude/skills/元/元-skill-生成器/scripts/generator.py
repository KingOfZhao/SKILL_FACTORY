# scripts/generator.py
# MCP-Aware Skill 生成器 的核心引擎脚本
# 版本：与 SKILL.md v1.2 对应
# 功能：接收用户需求 → 执行 6 步流程 → 生成 Skill + 结构化认知精炼

import os
import json
from typing import Dict, Any, Tuple, List

# 模拟的辅助函数（实际可由 LLM 在运行时填充更智能逻辑）
def check_mcp_association(desc: str) -> bool:
    """简单关键词检测强关联 MCP"""
    keywords = ["api", "database", "real-time", "github", "file system", "external", "live data", "websocket"]
    return any(k in desc.lower() for k in keywords)

def perform_enumeration(desc: str) -> Dict[str, List[str]]:
    """有限横向纵向穷举（这里是简化版，实际可让 LLM 更深度展开）"""
    # 根据 desc 动态生成，当前为占位示例
    return {
        "inputs": ["用户自然语言描述", "代码片段", "错误日志", "参考文档/截图"],
        "processes": ["分析需求", "参考最佳实践", "生成代码/内容", "验证格式", "优化建议"],
        "outputs": ["单文件内容", "完整项目结构", "diff 格式", "建议的配套 Skill 列表"],
        "mcp_needed": [] if not check_mcp_association(desc) else ["文件系统 MCP", "网络 MCP"]
    }

def generate_skill_name(original_request: str) -> str:
    """从用户输入生成 kebab-case 的 Skill 名称"""
    # 简化处理，实际可更智能
    words = original_request.lower().split()[:4]
    return "-".join(words).replace("生成", "generator").replace("skill", "").strip("-")

def create_skill_structure(target_dir: str, desc: str, enumeration: Dict, mcp_associated: bool):
    """创建 Skill 文件夹及核心文件（这里是模拟，实际写入文件）"""
    os.makedirs(target_dir, exist_ok=True)

    # 示例：写入 SKILL.md、description.md、common/ 等
    # 实际中会根据模板 + 注入 enumeration 内容
    print(f"创建目录: {target_dir}")
    print("  - SKILL.md (已注入穷举结果)")
    print("  - description.md (含局限声明)")
    print("  - common/underlying-convention.md (链接或复制)")
    if mcp_associated:
        print("  ※ 检测到 MCP 关联，已在 SKILL.md 中提示")

def extract_structured_patterns(generated_content: str) -> Dict:
    """从生成的 Skill 内容中提取新重叠模式（简化模拟）"""
    # 实际应解析文件内容，这里返回示例
    return {
        "new_process_pattern": "需求解析 → 模板填充 → 输出校验",
        "new_output_pattern": "带局限声明的 README + 拆分建议列表"
    }

def append_to_overlaps(new_patterns: Dict):
    """追加到 overlaps/common-overlaps.md"""
    path = "../overlaps/common-overlaps.md"
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n## 本次生成新增认知\n")
        for k, v in new_patterns.items():
            f.write(f"- {k}: {v}\n")
    print(f"已追加新模式到 {path}")

def generate_cognition_proposal(new_patterns: Dict, original_desc: str):
    """生成更新提案文件"""
    path = "../overlaps/cognition-update-proposal.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 本次生成认知更新提案\n\n")
        f.write(f"原始需求：{original_desc}\n\n")
        f.write("建议未来模板优化的点：\n")
        for k, v in new_patterns.items():
            f.write(f"- 在 reference/templates 中增加 {k} 模板：{v}\n")
    print(f"提案文件已生成：{path}")

def check_scope_and_suggest_splits(original_request: str, generated_skill_name: str) -> Tuple[bool, List[str]]:
    """
    检查是否疑似 scope creep，并给出拆分建议
    （当前为规则版，实际可让 LLM 更智能判断）
    """
    creep_indicators = [
        "完整系统", "端到端", "全流程", "一站式", "从头到尾", "整套", "pipeline",
        "自动化全部", "生成+测试+部署"
    ]

    detected = any(ind in original_request.lower() for ind in creep_indicators)

    if not detected:
        return False, []

    base_name = generated_skill_name.replace("-generator", "").strip()

    suggestions = [
        f"{base_name}-analyzer       : 只负责需求分析与问题拆解",
        f"{base_name}-generator      : 只负责核心内容/代码生成",
        f"{base_name}-validator      : 负责格式/质量校验",
        f"{base_name}-tester         : 单元测试 / 集成测试",
        f"{base_name}-optimizer      : 性能/可读性优化",
        f"{base_name}-deploy-helper  : 打包/部署/发布辅助"
    ]

    return True, suggestions


# 主入口函数（Claude 等环境通常会调用这个）
def main(user_input: str):
    print("=== Skill 生成流程开始 ===")
    print(f"用户需求：{user_input}\n")

    # Step 1: MCP 检查
    mcp_associated = check_mcp_association(user_input)
    if mcp_associated:
        print("⚠️ 检测到可能的强关联 MCP，已记录提示")

    # Step 2: 穷举
    enumeration = perform_enumeration(user_input)
    print("穷举结果概览：", json.dumps(enumeration, indent=2, ensure_ascii=False))

    # Step 3: 生成 Skill 名称 & 目标路径
    skill_name = generate_skill_name(user_input)
    target_dir = f"../待应用-skill/{skill_name}"

    # Step 4: 创建 Skill 结构
    create_skill_structure(target_dir, user_input, enumeration, mcp_associated)

    # Step 5: Scope 检查 & 拆分建议
    scope_creep_detected, suggestions = check_scope_and_suggest_splits(user_input, skill_name)
    if scope_creep_detected:
        print("\n⚠️ 警告：检测到潜在 scope creep，已生成单一职责 Skill。")
        print("建议额外创建以下配套 Skill 来完整实现原始需求：")
        for s in suggestions:
            print(f"  - {s}")

    # Step 6: 结构化认知精炼
    # 模拟已生成的内容（实际应读取 target_dir 中的文件）
    simulated_generated_content = "生成的 SKILL.md + README 等内容..."
    new_patterns = extract_structured_patterns(simulated_generated_content)

    append_to_overlaps(new_patterns)
    generate_cognition_proposal(new_patterns, user_input)

    print("\n=== 生成完成 ===")
    print(f"Skill 已保存至：{target_dir}")
    print("结构化认知已更新至 overlaps/")


# 方便本地测试 / 调试
if __name__ == "__main__":
    # 示例调用（实际环境中由 LLM 传入 user_input）
    example_input = "帮我生成一个 Flutter 完整 App 开发 Skill"
    main(example_input)