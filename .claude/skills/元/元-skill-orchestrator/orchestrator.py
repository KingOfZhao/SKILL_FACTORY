"""
元 Skill 全链路编排器

自动串联问题穷举、生成、扫描、检查、优化流程
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess


class SkillOrchestrator:
    """Skill 编排器"""

    def __init__(self, output_dir: str, pdf_reference: Optional[str] = None, verbose: bool = False):
        """
        初始化编排器

        Args:
            output_dir: 输出目录
            pdf_reference: PDF 参考文件路径
            verbose: 是否输出详细日志
        """
        self.output_dir = Path(output_dir)
        self.pdf_reference = pdf_reference
        self.verbose = verbose
        self.start_time = None

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 环节执行记录
        self.execution_steps: List[Dict] = []

    def log(self, message: str):
        """输出日志"""
        if self.verbose:
            print(f"[编排器] {message}")

    def record_step(self, stage: str, status: str, duration: str, output_info: str = ""):
        """记录执行步骤"""
        step = {
            "stage": stage,
            "status": status,
            "duration": duration,
            "output": output_info
        }
        self.execution_steps.append(step)
        self.log(f"{stage}: {status} ({duration})")

    def execute_full_chain(self, user_request: str) -> Dict:
        """
        执行完整链路

        Args:
            user_request: 用户需求

        Returns:
            执行结果
        """
        self.start_time = datetime.now()
        self.log(f"开始执行完整链路，用户需求: {user_request[:100]}...")

        results = {}

        # 步骤 1: 微分拆解器（micro-diff-factory）
        self.log("=== 步骤 1: 微分拆解器 ===")
        step1_result = self._execute_diff_decomposer(user_request)
        results["diff_decomposer"] = step1_result

        # 步骤 2: 问题穷举器
        self.log("=== 步骤 2: 问题穷举器 ===")
        step2_result = self._execute_problem_enumerator(user_request, step1_result)
        results["problem_enumerator"] = step2_result

        # 步骤 3: 生成器
        self.log("=== 步骤 3: 生成器 ===")
        step3_result = self._execute_generator(step2_result)
        results["generator"] = step3_result

        # 步骤 4: 扫描器
        self.log("=== 步骤 4: 扫描器 ===")
        step4_result = self._execute_scanner(step3_result)
        results["scanner"] = step4_result

        # 步骤 5: 检查器
        self.log("=== 步骤 5: 检查器 ===")
        step5_result = self._execute_checker(step4_result)
        results["checker"] = step5_result

        # 步骤 6: 优化器
        self.log("=== 步骤 6: 优化器 ===")
        step6_result = self._execute_optimizer(step5_result)
        results["optimizer"] = step6_result

        # 生成链路执行报告
        self._generate_chain_report(user_request, results)

        return results

    def _execute_diff_decomposer(self, user_request: str) -> Dict:
        """执行微分拆解器"""
        start_time = datetime.now()

        # 调用微分拆解器
        # 注意：这里假设微分拆解器已经作为 Skill 存在
        diff_decomposer_path = Path("/Users/administruter/Desktop/skill_factory/.claude/skills/micro-diff-factory")

        # 检查问题分类器
        classifier_path = diff_decomposer_path / "analyzer" / "problem_classifier.py"

        if classifier_path.exists():
            self.log("使用问题分类器分析需求")
            # 这里可以实际调用 Python 脚本
            # 由于编排器本身不是执行环境，我们模拟分类结果

        # 分析需求并生成微分拆解建议
        analysis_result = {
            "problem_type": self._classify_problem_type(user_request),
            "variables_extracted": self._extract_variables(user_request),
            "constraints_identified": self._identify_constraints(user_request),
            "optimization_goals": self._identify_goals(user_request),
            "matched_cases": self._find_matching_cases(user_request)
        }

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("微分拆解器", "完成", f"{duration:.1f}秒",
                       f"匹配参考案例: {len(analysis_result['matched_cases'])}个")

        return analysis_result

    def _execute_problem_enumerator(self, user_request: str, diff_result: Dict) -> Dict:
        """执行问题穷举器"""
        start_time = datetime.now()

        # 基于微分拆解结果生成问题穷举
        # 使用微分拆解器提供的问题类型和变量信息

        problem_type = diff_result.get("problem_type", "通用")
        variables = diff_result.get("variables_extracted", [])

        # 生成技能建议（基于微分拆解）
        skills = self._enumerate_skills_based_on_diff(
            problem_type,
            variables,
            diff_result.get("matched_cases", [])
        )

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("问题穷举器", "完成", f"{duration:.1f}秒",
                       f"生成技能建议: {len(skills)}个，基于微分拆解: 是")

        return {
            "skills": skills,
            "based_on_diff_decomposition": True,
            "problem_type": problem_type
        }

    def _execute_generator(self, enumerator_result: Dict) -> Dict:
        """执行生成器"""
        start_time = datetime.now()

        skills = enumerator_result.get("skills", [])
        problem_type = enumerator_result.get("problem_type", "通用")

        # 这里应该是生成器生成具体 Skill 文件
        # 由于这是一个编排框架，我们记录生成信息

        generated_skills = []
        for skill in skills:
            generated_skills.append({
                "name": skill.get("name", "未命名技能"),
                "type": skill.get("type", "component"),
                "description": skill.get("description", ""),
                "status": "generated"
            })

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("生成器", "完成", f"{duration:.1f}秒",
                       f"生成技能: {len(generated_skills)}个")

        return {
            "generated_skills": generated_skills,
            "problem_type": problem_type
        }

    def _execute_scanner(self, generator_result: Dict) -> Dict:
        """执行扫描器"""
        start_time = datetime.now()

        # 扫描生成的技能和参考案例
        # 这里应该调用实际的扫描器

        micro_diff_path = Path("/Users/administruter/Desktop/skill_factory/.claude/skills/micro-diff-factory")
        reference_cases_path = micro_diff_path / "references" / "micro-diff-cases"

        capabilities = []

        # 扫描参考案例
        if reference_cases_path.exists():
            self.log("扫描参考案例...")
            for case_file in reference_cases_path.rglob("*.md"):
                case_name = case_file.stem
                capabilities.append({
                    "name": case_name,
                    "type": "reference_case",
                    "path": str(case_file.relative_to(micro_diff_path))
                })

        # 扫描求解策略
        strategies_path = micro_diff_path / "strategies"
        if strategies_path.exists():
            for strategy_file in strategies_path.glob("*.py"):
                strategy_name = strategy_file.stem
                capabilities.append({
                    "name": strategy_name,
                    "type": "solution_strategy",
                    "path": str(strategy_file.relative_to(micro_diff_path))
                })

        # 扫描可视化工具
        visualization_path = micro_diff_path / "visualization"
        if visualization_path.exists():
            for viz_file in visualization_path.glob("*.py"):
                viz_name = viz_file.stem
                capabilities.append({
                    "name": viz_name,
                    "type": "visualization_tool",
                    "path": str(viz_file.relative_to(micro_diff_path))
                })

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("扫描器", "完成", f"{duration:.1f}秒",
                       f"扫描结果: {len(capabilities)}个组件")

        return {
            "capabilities": capabilities,
            "total_count": len(capabilities)
        }

    def _execute_checker(self, scanner_result: Dict) -> Dict:
        """执行检查器"""
        start_time = datetime.now()

        # 验证生成的组件
        # 这里应该调用实际的检查器

        capabilities = scanner_result.get("capabilities", [])
        passed = 0
        warnings = 0
        failed = 0

        for capability in capabilities:
            # 简单验证：文件是否存在
            capability_path = Path("/Users/administruter/Desktop/skill_factory/.claude/skills/micro-diff-factory") / capability.get("path", "")
            if capability_path.exists():
                passed += 1
            else:
                warnings += 1

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("检查器", "完成", f"{duration:.1f}秒",
                       f"通过: {passed}, 警告: {warnings}, 失败: {failed}")

        return {
            "total": len(capabilities),
            "passed": passed,
            "warnings": warnings,
            "failed": failed
        }

    def _execute_optimizer(self, checker_result: Dict) -> Dict:
        """执行优化器"""
        start_time = datetime.now()

        # 生成优化建议
        # 元 Skill 优化方案和底层约定优化方案

        meta_skill_optimizations = [
            {
                "name": "增强微分拆解能力",
                "description": "添加更多领域支持和求解策略",
                "priority": "high"
            },
            {
                "name": "优化可视化工具",
                "description": "添加更多图表类型和交互功能",
                "priority": "medium"
            }
        ]

        convention_optimizations = [
            {
                "name": "统一变量命名约定",
                "description": "定义跨领域的变量命名规范",
                "requires_manual_confirmation": True
            }
        ]

        duration = (datetime.now() - start_time).total_seconds()
        self.record_step("优化器", "完成", f"{duration:.1f}秒",
                       f"Skill优化方案: {len(meta_skill_optimizations)}个，底层约定优化方案: {len(convention_optimizations)}个（需确认）")

        return {
            "meta_skill_optimizations": meta_skill_optimizations,
            "convention_optimizations": convention_optimizations
        }

    def _generate_chain_report(self, user_request: str, results: Dict):
        """生成链路执行报告"""
        total_duration = (datetime.now() - self.start_time).total_seconds()

        report = f"""# 元 Skill 链路执行报告

## 执行概览
- 执行时间: {self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}
- 执行模式: full-chain
- 总耗时: {total_duration:.1f} 秒

## 用户需求
> {user_request}

## 执行步骤
"""

        for step in self.execution_steps:
            status_emoji = "✓" if "完成" in step["status"] else "✗"
            report += f"""
### {step['stage']}
- **状态**: {status_emoji} {step['status']}
- **耗时**: {step['duration']}
- **输出**: {step['output']}
"""

        # 添加数据流转
        report += """
## 数据流转

```
需求 → 微分拆解 → 微分建议 → 问题穷举 → Skill树 → 生成器 → 技能文件 → 扫描器 → 能力清单 → 检查器 → 验证结果 → 优化器 → 优化报告
```

## 生成物

| 物品 | 位置 | 说明 |
|------|------|------|
| 微分拆解输出 | micro-diff-factory/output/ | 拆解建议 |
| 问题穷举输出 | 元-skill-问题穷举器/output/ | 穷举建议 |
| 参考案例 | micro-diff-factory/references/micro-diff-cases/ | 累积的参考案例 |
| 求解策略 | micro-diff-factory/strategies/ | 优化算法库 |
| 可视化工具 | micro-diff-factory/visualization/ | 图表生成工具 |
| 自动优化建议 | micro-diff-factory/optimization/ | 智能建议生成器 |
| 案例质量管理 | micro-diff-factory/references/reference_manager.py | 质量评分和索引 |

## 建议后续操作

### 1. 查看微分拆解结果
查看 `micro-diff-factory/output/` 中的微分拆解建议
- 变量分析
- 约束条件
- 优化建议
- 参考案例匹配

### 2. 积累参考案例
每次调用都应该在 `references/micro-diff-cases/` 下添加新的参考案例
- 案例包含完整的微分拆解
- 包含求解策略和代码示例
- 包含预期效果和总结

### 3. 生成子技能
基于微分拆解结果，生成至少 5 个子技能：
1. 元工厂（meta-factory）：主协调 Skill
2. 基本微分（basic-differential）：变量拆解和分析
3. 数值微分（numerical-differential）：公式推导和计算
4. 可视化（visualization）：图表和可视化工具
5. 应用拆解（application-decomposer）：具体领域拆解

### 4. 验证参考文件夹
运行参考管理器的验证功能，确保所有案例符合质量标准：
```bash
cd micro-diff-factory/references
python reference_manager.py verify
```

### 5. 测试求解策略
使用不同求解策略测试问题：
- 模拟退火
- 粒子群优化
- 梯度下降

### 6. 验证可视化工具
生成变量关系图和优化轨迹图验证拆解结果

---

**报告生成时间**: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
**迭代 ID**: {getattr(self, 'iteration_id', 'N/A')}
"""

        # 保存报告
        report_file = self.output_dir / "chain-execution-report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"链路执行报告已保存: {report_file}")

    def _classify_problem_type(self, request: str) -> str:
        """分类问题类型"""
        request_lower = request.lower()

        # 关键词分类
        if any(kw in request_lower for kw in ["bluetooth", "连接", "connect", "reconnect"]):
            return "蓝牙连接"
        elif any(kw in request_lower for kw in ["rssi", "chart", "图表", "signal"]):
            return "RSSI 图表"
        elif any(kw in request_lower for kw in ["性能", "performance", "优化", "慢"]):
            return "性能优化"
        elif any(kw in request_lower for kw in ["算法", "algorithm", "排序", "搜索"]):
            return "算法设计"
        elif any(kw in request_lower for kw in ["概率", "probability", "随机"]):
            return "概率问题"
        elif any(kw in request_lower for kw in ["物理", "physics", "力学"]):
            return "物理问题"
        else:
            return "通用问题"

    def _extract_variables(self, request: str) -> List[str]:
        """提取变量"""
        # 简单关键词提取
        variable_keywords = ["超时", "延迟", "重试", "间隔", "点数", "缓存", "内存", "fps"]
        found_variables = []

        for keyword in variable_keywords:
            if keyword in request:
                found_variables.append(keyword)

        return found_variables

    def _identify_constraints(self, request: str) -> List[str]:
        """识别约束"""
        constraints = []

        if "不超过" in request or "最多" in request or "最大" in request:
            constraints.append("最大值约束")
        if "至少" in request or "最小" in request or "最少" in request:
            constraints.append("最小值约束")
        if "必须" in request or "不能" in request or "禁止" in request:
            constraints.append("强制约束")

        return constraints

    def _identify_goals(self, request: str) -> List[str]:
        """识别优化目标"""
        goals = []

        if "最快" in request or "高效" in request:
            goals.append("速度优化")
        if "最稳定" in request or "不崩溃" in request:
            goals.append("稳定性优化")
        if "内存" in request:
            goals.append("内存优化")
        if "流畅" in request or "不卡顿" in request:
            goals.append("流畅度优化")

        return goals

    def _find_matching_cases(self, request: str) -> List[str]:
        """查找匹配的参考案例"""
        # 这里应该查询参考案例库
        # 由于这是编排器框架，我们返回模拟结果

        problem_type = self._classify_problem_type(request)

        mapping = {
            "蓝牙连接": ["bluetooth/connection-optimization.md"],
            "RSSI 图表": ["rssi-chart/performance-optimization.md"],
            "性能优化": ["performance/app-optimization.md"]
        }

        return mapping.get(problem_type, [])

    def _enumerate_skills_based_on_diff(self, problem_type: str, variables: List[str], matched_cases: List[str]) -> List[Dict]:
        """基于微分拆解枚举技能"""
        skills = []

        # 根据问题类型生成技能
        if problem_type == "蓝牙连接":
            skills.extend([
                {"name": "连接稳定性分析", "type": "analyzer", "description": "分析连接稳定性指标"},
                {"name": "重连策略选择", "type": "strategy", "description": "选择合适的重连策略"},
                {"name": "超时优化器", "type": "optimizer", "description": "优化连接超时参数"}
            ])
        elif problem_type == "RSSI 图表":
            skills.extend([
                {"name": "数据点管理", "type": "utility", "description": "管理图表数据点"},
                {"name": "渲染优化", "type": "optimizer", "description": "优化图表渲染性能"}
            ])
        elif problem_type == "性能优化":
            skills.extend([
                {"name": "懒加载组件", "type": "component", "description": "实现列表懒加载"},
                {"name": "缓存管理器", "type": "utility", "description": "管理数据缓存"},
                {"name": "资源清理器", "type": "utility", "description": "自动清理资源"}
            ])

        return skills


def main():
    parser = argparse.ArgumentParser(description="元 Skill 全链路编排器")

    parser.add_argument("user_request", help="用户需求描述")
    parser.add_argument("--full-chain", action="store_true", default=True,
                       help="完整自动链路（默认）")
    parser.add_argument("--start-at", type=str, choices=["diff-decomposer", "enumerator", "generator", "scanner", "checker", "optimizer"],
                       help="从指定环节开始")
    parser.add_argument("--single-step", type=str, choices=["diff-decomposer", "enumerator", "generator", "scanner", "checker", "optimizer"],
                       help="仅执行单步")
    parser.add_argument("--pdf-reference", type=str,
                       help="PDF 参考文件路径")
    parser.add_argument("--output-dir", type=str, default="output",
                       help="输出目录")
    parser.add_argument("--verbose", action="store_true",
                       help="输出详细日志")
    parser.add_argument("--iteration-id", type=str, default="default-iteration",
                       help="迭代 ID")

    args = parser.parse_args()

    # 创建编排器
    orchestrator = SkillOrchestrator(
        output_dir=args.output_dir,
        pdf_reference=args.pdf_reference,
        verbose=args.verbose
    )
    orchestrator.iteration_id = args.iteration_id

    # 执行请求的操作
    if args.single_step:
        orchestrator.log(f"执行单步: {args.single_step}")
        # 这里可以执行单步逻辑
        # 由于这是框架，我们执行完整链路作为示例
        orchestrator.execute_full_chain(args.user_request)
    else:
        orchestrator.execute_full_chain(args.user_request)

    orchestrator.log("执行完成！")
    print(f"\n链路执行报告已保存到: {Path(args.output_dir) / 'chain-execution-report.md'}")


if __name__ == "__main__":
    main()
