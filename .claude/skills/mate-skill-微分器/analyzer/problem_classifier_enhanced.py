"""
增强版问题分类器（修复版）

基于微分拆解框架的智能问题识别和分类

改进：
1. 增强问题类型识别能力（支持更多领域）
2. 添加变量依赖关系分析
3. 实现约束求解器
4. 提供微分拆解模板生成
5. 支持多种输入格式（文本、JSON、YAML）
"""

import json
import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime


class ProblemDomain(Enum):
    """问题领域"""
    BLUETOOTH = "bluetooth"
    RSSI_CHART = "rssi_chart"
    PERFORMANCE = "performance"
    ALGORITHM = "algorithm"
    PROBABILITY = "probability"
    PHYSICS = "physics"
    UI_UX = "ui_ux"
    NETWORK = "network"
    DATABASE = "database"
    API = "api"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    OPTIMIZATION = "optimization"
    GENERAL = "general"


class ProblemComplexity(Enum):
    """问题复杂度"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class OptimizationCategory(Enum):
    """优化类别"""
    PERFORMANCE = "performance"
    MEMORY = "memory"
    CONNECTIVITY = "connectivity"
    STABILITY = "stability"
    USER_EXPERIENCE = "user_experience"
    RESOURCE_UTILIZATION = "resource_utilization"


@dataclass
class VariableDependency:
    """变量依赖关系"""
    source: str
    target: str
    dependency_type: str
    strength: float
    description: str


@dataclass
class Constraint:
    """约束条件"""
    name: str
    constraint_type: str
    description: str
    expression: str
    violation_penalty: float


@dataclass
class DecompositionResult:
    """微分拆解结果"""
    problem_type: ProblemDomain
    complexity: ProblemComplexity
    variables: Dict[str, Dict]
    constraints: List[Constraint]
    optimization_objectives: List[str]
    variable_dependencies: List[VariableDependency]
    solving_strategies: List[str]
    recommended_approach: str
    confidence_score: float


class EnhancedProblemClassifier:
    """增强版问题分类器"""

    def __init__(self):
        self.domain_keywords = {
            ProblemDomain.BLUETOOTH: {
                "primary": ["bluetooth", "蓝牙", "connect", "连接", "reconnect", "重连", "disconnect", "断开", "pair", "配对", "scan", "扫描", "device", "设备"],
                "secondary": ["rssi", "signal", "信号", "gatt", "ble", "low energy", "低功耗"],
                "tertiary": ["timeout", "超时", "buffer", "缓冲区", "profile", "配置文件"]
            },
            ProblemDomain.RSSI_CHART: {
                "primary": ["chart", "图表", "graph", "plot", "曲线", "折线图", "实时", "real-time"],
                "secondary": ["rssi", "signal", "strength", "信号强度", "update", "更新", "refresh", "刷新", "fps", "帧率", "卡顿"],
                "tertiary": ["data point", "数据点", "culling", "裁剪", "batch", "批量", "render", "渲染", "gradient", "渐变"]
            },
            ProblemDomain.PERFORMANCE: {
                "primary": ["performance", "性能", "optimize", "优化", "slow", "慢", "卡顿", "freeze", "卡死", "crash", "崩溃"],
                "secondary": ["memory", "内存", "leak", "泄漏", "heap", "堆", "gc", "垃圾回收", "fps", "帧率"],
                "tertiary": ["render", "渲染", "layout", "布局", "lazy", "懒加载", "virtual", "虚拟化", "cache", "缓存", "pool", "对象池"]
            },
            ProblemDomain.ALGORITHM: {
                "primary": ["algorithm", "算法", "sort", "排序", "search", "搜索", "traversal", "遍历", "tree", "树"],
                "secondary": ["complexity", "复杂度", "time", "时间", "space", "空间", "O(n)", "O(log n)", "O(1)"],
                "tertiary": ["divide", "分治", "divide and conquer", "动态规划", "dp", "greedy", "贪心", "backtrack", "回溯"]
            },
            ProblemDomain.PROBABILITY: {
                "primary": ["probability", "概率", "random", "随机", "distribution", "分布", "统计", "statistics"],
                "secondary": ["expectation", "期望", "variance", "方差", "std", "标准差", "sample", "样本"],
                "tertiary": ["markov", "马尔可夫", "monte carlo", "蒙特卡洛", "bayes", "贝叶斯", "conditional", "条件"]
            },
            ProblemDomain.PHYSICS: {
                "primary": ["physics", "物理", "mechanics", "力学", "kinematics", "运动学", "dynamics", "动力学"],
                "secondary": ["force", "力", "velocity", "速度", "acceleration", "加速度", "mass", "质量", "energy", "能量"],
                "tertiary": ["momentum", "动量", "angular", "角动量", "torque", "力矩", "friction", "摩擦"]
            },
            ProblemDomain.UI_UX: {
                "primary": ["ui", "界面", "interface", "design", "设计", "layout", "布局", "component", "组件", "widget", "控件"],
                "secondary": ["responsive", "响应式", "adaptive", "自适应", "dark mode", "深色模式", "animation", "动画"],
                "tertiary": ["transition", "过渡", "gesture", "手势", "navigation", "导航", "theme", "主题"]
            },
            ProblemDomain.NETWORK: {
                "primary": ["network", "网络", "http", "https", "request", "请求", "response", "响应"],
                "secondary": ["latency", "延迟", "timeout", "超时", "retry", "重试", "circuit breaker", "熔断"],
                "tertiary": ["cache", "缓存", "cdn", "content delivery", "cdn", "compression", "压缩", "websocket", "ws"]
            },
            ProblemDomain.DATABASE: {
                "primary": ["database", "数据库", "db", "sql", "query", "查询", "transaction", "事务"],
                "secondary": ["index", "索引", "migration", "迁移", "replication", "复制", "sharding", "分片"],
                "tertiary": ["orm", "object-relational-mapping", "nosql", "key-value", "key-value", "document", "文档", "graph"]
            },
            ProblemDomain.API: {
                "primary": ["api", "接口", "rest", "graphql", "rpc", "endpoint", "端点"],
                "secondary": ["authentication", "认证", "authorization", "授权", "rate limit", "限流", "pagination", "分页"],
                "tertiary": ["version", "版本", "backward compatibility", "向后兼容", "api gateway", "网关", "middleware", "中间件"]
            },
            ProblemDomain.SECURITY: {
                "primary": ["security", "安全", "authentication", "认证", "authorization", "授权", "encryption", "加密"],
                "secondary": ["jwt", "token", "session", "会话", "csrf", "xss", "注入"],
                "tertiary": ["oauth", "sso", "ssl", "tls", "https", "certificate", "证书", "crl"]
            },
            ProblemDomain.DEPLOYMENT: {
                "primary": ["deployment", "部署", "ci/cd", "docker", "kubernetes", "container"],
                "secondary": ["pipeline", "流水线", "build", "构建", "release", "发布", "version control", "版本控制"],
                "tertiary": ["rollback", "回滚", "canary", "灰度发布", "blue-green", "蓝绿发布"]
            },
            ProblemDomain.TESTING: {
                "primary": ["test", "测试", "testing", "qa", "quality assurance", "质量保证"],
                "secondary": ["unit test", "单元测试", "integration test", "集成测试", "e2e test", "端到端测试", "automation", "自动化"],
                "tertiary": ["mock", "stub", "fixture", "test data", "测试数据", "coverage", "覆盖率"]
            },
            ProblemDomain.OPTIMIZATION: {
                "primary": ["optimization", "优化", "tune", "调优", "profile", "性能分析"],
                "secondary": ["bottleneck", "瓶颈", "hotspot", "热点", "memory leak", "内存泄漏", "cpu usage", "cpu使用"],
                "tertiary": ["caching", "缓存", "lazy loading", "懒加载", "code splitting", "代码分割", "tree shaking", "摇树优化"]
            },
            ProblemDomain.GENERAL: {
                "primary": ["general", "通用", "misc", "其他", "else", "other"],
                "secondary": ["feature", "功能", "requirement", "需求", "spec", "规格"],
                "tertiary": ["bug", "bug", "issue", "问题", "fix", "修复", "improvement", "改进"]
            }
        }

    def classify_problem(self, description: str, context: Optional[Dict] = None) -> DecompositionResult:
        """
        智能分类问题并进行微分拆解

        Args:
            description: 问题描述
            context: 上下文信息（可选）

        Returns:
            微分拆解结果
        """
        # 1. 问题分类
        problem_domain, confidence = self._classify_domain(description)

        # 2. 确定复杂度
        complexity = self._determine_complexity(description, problem_domain)

        # 3. 提取变量
        variables = self._extract_variables(description, problem_domain)

        # 4. 识别约束
        constraints = self._identify_constraints(description, problem_domain)

        # 5. 分析优化目标
        optimization_objectives = self._identify_optimization_goals(description, problem_domain)

        # 6. 分析变量依赖关系
        variable_dependencies = self._analyze_variable_dependencies(variables)

        # 7. 推荐求解策略
        solving_strategies = self._recommend_solving_strategies(problem_domain, complexity)

        # 8. 推荐方法路径
        recommended_approach = self._recommend_approach(problem_domain, complexity)

        # 计算置信度
        confidence_score = self._calculate_confidence(confidence, len(variables), len(constraints))

        return DecompositionResult(
            problem_type=problem_domain,
            complexity=complexity,
            variables=variables,
            constraints=constraints,
            optimization_objectives=optimization_objectives,
            variable_dependencies=variable_dependencies,
            solving_strategies=solving_strategies,
            recommended_approach=recommended_approach,
            confidence_score=confidence_score
        )

    def _classify_domain(self, description: str) -> Tuple[ProblemDomain, float]:
        """分类问题领域"""
        description_lower = description.lower()

        # 计算每个领域的得分
        scores = {}

        for domain, keywords in self.domain_keywords.items():
            # 主关键词权重 3.0
            primary_score = sum(3.0 for kw in keywords.get("primary", []) if kw in description_lower)
            # 次关键词权重 1.5
            secondary_score = sum(1.5 for kw in keywords.get("secondary", []) if kw in description_lower)
            # 第三关键词权重 0.5
            tertiary_score = sum(0.5 for kw in keywords.get("tertiary", []) if kw in description_lower)

            total_score = primary_score + secondary_score + tertiary_score
            scores[domain] = total_score

        # 返回最高分的领域
        best_domain = max(scores, key=scores.get)

        # 计算置信度（归一化到 0-1）
        max_score = max(scores.values()) if scores else 1.0
        confidence = scores[best_domain] / max_score if max_score > 0 else 0.5

        return best_domain, confidence

    def _determine_complexity(self, description: str, domain: ProblemDomain) -> ProblemComplexity:
        """确定问题复杂度"""
        description_lower = description.lower()

        # 复杂度关键词
        complexity_keywords = {
            ProblemComplexity.SIMPLE: ["简单", "single", "basic", "基础", "quick", "快速", "minimal", "最小"],
            ProblemComplexity.MODERATE: ["中等", "normal", "standard", "常规", "average", "平均", "moderate", "适度"],
            ProblemComplexity.COMPLEX: ["复杂", "complex", "multiple", "多", "multiple step", "多步", "advanced", "高级", "challenging", "困难"],
            ProblemComplexity.EXPERT: ["专家", "expert", "极难", "extremely hard", "extremely difficult", "最难"]
        }

        # 搜索复杂度关键词
        for complexity, keywords in complexity_keywords.items():
            for kw in keywords:
                if kw in description_lower:
                    return complexity

        # 默认中等
        return ProblemComplexity.MODERATE

    def _extract_variables(self, description: str, domain: ProblemDomain) -> Dict[str, Dict]:
        """提取变量"""
        variables = {}
        description_lower = description.lower()

        # 根据领域提取变量模板
        if domain == ProblemDomain.BLUETOOTH:
            variables = {
                "connection_timeout": {
                    "name": "连接超时",
                    "type": "continuous",
                    "unit": "seconds",
                    "min_value": 1.0,
                    "max_value": 60.0,
                    "default_value": 10.0,
                    "description": "蓝牙连接超时时间"
                },
                "reconnect_delay": {
                    "name": "重连延迟",
                    "type": "continuous",
                    "unit": "seconds",
                    "min_value": 0.5,
                    "max_value": 30.0,
                    "default_value": 2.0,
                    "description": "重连尝试之间的延迟"
                },
                "max_retries": {
                    "name": "最大重试次数",
                    "type": "integer",
                    "unit": "count",
                    "min_value": 0,
                    "max_value": 10,
                    "default_value": 3,
                    "description": "最大重连尝试次数"
                },
                "rssi_threshold": {
                    "name": "RSSI 阈值",
                    "type": "integer",
                    "unit": "dBm",
                    "min_value": -100,
                    "max_value": -20,
                    "default_value": -70,
                    "description": "最小可接受的信号强度"
                }
            }

        elif domain == ProblemDomain.RSSI_CHART:
            variables = {
                "update_interval": {
                    "name": "更新间隔",
                    "type": "integer",
                    "unit": "milliseconds",
                    "min_value": 100,
                    "max_value": 2000,
                    "default_value": 500,
                    "description": "数据更新间隔"
                },
                "max_data_points": {
                    "name": "最大数据点",
                    "type": "integer",
                    "unit": "count",
                    "min_value": 10,
                    "max_value": 1000,
                    "default_value": 300,
                    "description": "图表最大显示的数据点数"
                },
                "cache_size": {
                    "name": "缓存大小",
                    "type": "integer",
                    "unit": "MB",
                    "min_value": 10,
                    "max_value": 500,
                    "default_value": 50,
                    "description": "数据缓存大小"
                }
            }

        elif domain == ProblemDomain.PERFORMANCE:
            variables = {
                "target_fps": {
                    "name": "目标帧率",
                    "type": "float",
                    "unit": "frames/sec",
                    "min_value": 30,
                    "max_value": 120,
                    "default_value": 60,
                    "description": "目标帧率"
                },
                "max_memory_mb": {
                    "name": "最大内存",
                    "type": "float",
                    "unit": "MB",
                    "min_value": 50,
                    "max_value": 500,
                    "default_value": 200,
                    "description": "最大内存占用"
                },
                "render_time_budget": {
                    "name": "渲染时间预算",
                    "type": "integer",
                    "unit": "milliseconds",
                    "min_value": 5,
                    "max_value": 100,
                    "default_value": 16,
                    "description": "每帧最大渲染时间"
                }
            }

        # 通用变量（适用于所有领域）
        common_variables = {
            "problem_statement": {
                "name": "问题描述",
                "type": "text",
                "description": "原始问题描述"
            }
        }

        # 合并变量
        variables.update(common_variables)

        return variables

    def _identify_constraints(self, description: str, domain: ProblemDomain) -> List[Constraint]:
        """识别约束"""
        constraints = []
        description_lower = description.lower()

        # 硬约束
        if "必须" in description_lower or "要求" in description_lower:
            if "不超过" in description_lower or "最多" in description_lower:
                constraints.append(Constraint(
                    name="最大值约束",
                    constraint_type="hard",
                    description="存在最大值限制",
                    expression="value <= max_value",
                    violation_penalty=1.0
                ))
            if "至少" in description_lower or "最少" in description_lower:
                constraints.append(Constraint(
                    name="最小值约束",
                    constraint_type="hard",
                    description="存在最小值限制",
                    expression="value >= min_value",
                    violation_penalty=1.0
                ))

        # 软约束
        if "最好" in description_lower or "尽可能" in description_lower or "优化" in description_lower:
            constraints.append(Constraint(
                name="优化目标",
                constraint_type="soft",
                description="需要优化的目标",
                expression="minimize(metric)",
                violation_penalty=0.5
            ))

        # 边界约束
        if "在" in description_lower or "范围" in description_lower:
            constraints.append(Constraint(
                name="边界约束",
                constraint_type="boundary",
                description="值的取值范围",
                expression="min_value <= value <= max_value",
                violation_penalty=0.3
            ))

        return constraints

    def _identify_optimization_goals(self, description: str, domain: ProblemDomain) -> List[str]:
        """识别优化目标"""
        goals = []
        description_lower = description.lower()

        if domain == ProblemDomain.BLUETOOTH:
            if "稳定" in description_lower or "不断开" in description_lower:
                goals.append("稳定性提升")
            if "快" in description_lower or "速度" in description_lower:
                goals.append("连接速度优化")
            if "省电" in description_lower or "低功耗" in description_lower:
                goals.append("功耗优化")

        elif domain == ProblemDomain.RSSI_CHART:
            if "流畅" in description_lower or "卡顿" in description_lower:
                goals.append("流畅度提升")
            if "内存" in description_lower:
                goals.append("内存优化")
            if "实时" in description_lower or "低延迟" in description_lower:
                goals.append("实时性提升")

        elif domain == ProblemDomain.PERFORMANCE:
            if "fps" in description_lower or "帧率" in description_lower:
                goals.append("FPS 提升")
            if "内存" in description_lower or "泄漏" in description_lower:
                goals.append("内存优化")
            if "启动" in description_lower or "加载" in description_lower:
                goals.append("启动时间优化")
            if "响应" in description_lower or "交互" in description_lower:
                goals.append("交互响应优化")

        # 通用优化目标
        if "优化" in description_lower:
            goals.append("整体性能优化")

        return goals

    def _analyze_variable_dependencies(self, variables: Dict[str, Dict]) -> List[VariableDependency]:
        """分析变量依赖关系"""
        dependencies = []
        variable_names = list(variables.keys())

        # 简单依赖分析
        if "connection_timeout" in variable_names and "reconnect_delay" in variable_names:
            dependencies.append(VariableDependency(
                source="connection_timeout",
                target="reconnect_delay",
                dependency_type="partial",
                strength=0.6,
                description="较长的超时可能需要更长的重连延迟"
            ))

        if "max_data_points" in variable_names and "cache_size" in variable_names:
            dependencies.append(VariableDependency(
                source="max_data_points",
                target="cache_size",
                dependency_type="inverse",
                strength=0.8,
                description="更多的数据点需要更大的缓存"
            ))

        if "target_fps" in variable_names and "render_time_budget" in variable_names:
            dependencies.append(VariableDependency(
                source="target_fps",
                target="render_time_budget",
                dependency_type="functional",
                strength=0.9,
                description="更高的目标 FPS 需要更短的渲染时间预算"
            ))

        return dependencies

    def _recommend_solving_strategies(self, domain: ProblemDomain, complexity: ProblemComplexity) -> List[str]:
        """推荐求解策略"""
        strategies = []

        if domain == ProblemDomain.BLUETOOTH:
            if complexity == ProblemComplexity.SIMPLE:
                strategies.extend(["fixed_timeout", "simple_retry"])
            elif complexity == ProblemComplexity.MODERATE:
                strategies.extend(["exponential_backoff", "adaptive_timeout"])
            elif complexity in [ProblemComplexity.COMPLEX, ProblemComplexity.EXPERT]:
                strategies.extend(["exponential_backoff", "adaptive_timeout", "smart_reconnection"])

        elif domain == ProblemDomain.RSSI_CHART:
            strategies.extend(["adaptive_update_interval", "dynamic_data_culling", "batch_rendering"])

        elif domain == ProblemDomain.PERFORMANCE:
            if complexity == ProblemComplexity.SIMPLE:
                strategies.extend(["const_optimization", "lazy_loading"])
            elif complexity == ProblemComplexity.MODERATE:
                strategies.extend(["caching", "object_pooling"])
            elif complexity in [ProblemComplexity.COMPLEX, ProblemComplexity.EXPERT]:
                strategies.extend(["caching", "object_pooling", "code_splitting", "tree_shaking"])

        # 通用策略
        if not strategies:
            strategies.extend(["gradient_descent", "iterative_refinement"])

        return strategies

    def _recommend_approach(self, domain: ProblemDomain, complexity: ProblemComplexity) -> str:
        """推荐方法路径"""
        if complexity == ProblemComplexity.SIMPLE:
            return "直接实施（单一技能调用）"
        elif complexity == ProblemComplexity.MODERATE:
            return "分步实施（2-3 个技能调用）"
        else:
            return "微分拆解 + 多技能组合（完整链路）"

    def _calculate_confidence(self, domain_confidence: float, variable_count: int, constraint_count: int) -> float:
        """计算整体置信度"""
        # 领域置信度权重 0.4
        # 变量数量权重 0.3
        # 约束数量权重 0.3

        base_confidence = domain_confidence
        variable_bonus = min(0.3, variable_count / 10)
        constraint_bonus = min(0.3, constraint_count / 5)

        return min(1.0, base_confidence + variable_bonus + constraint_bonus)

    def generate_decomposition_report(self, result: DecompositionResult) -> str:
        """生成微分拆解报告（Markdown 格式）"""
        report = f"""# 问题微分拆解报告

## 问题分类

| 属性 | 值 |
|------|------|
| 问题领域 | {result.problem_type.value} |
| 复杂度 | {result.complexity.value} |
| 置信度 | {result.confidence_score:.2f} |

## 变量分析

识别到 {len(result.variables)} 个变量：

"""

        for var_name, var_info in result.variables.items():
            report += f"""
### {var_info['name']}
- **类型**: {var_info.get('type', 'unknown')}
- **单位**: {var_info.get('unit', 'N/A')}
- **取值范围**: {var_info.get('min_value', 'N/A')} - {var_info.get('max_value', 'N/A')}
- **默认值**: {var_info.get('default_value', 'N/A')}
- **描述**: {var_info.get('description', '')}
"""

        report += f"""

## 约束条件

识别到 {len(result.constraints)} 个约束：

"""

        for i, constraint in enumerate(result.constraints, 1):
            report += f"{i}. **{constraint.name}** ({constraint.constraint_type})\n"
            report += f"   - 描述: {constraint.description}\n"
            report += f"   - 表达式: `{constraint.expression}`\n"
            report += f"   - 违反惩罚: {constraint.violation_penalty}\n"

        report += f"""

## 变量依赖关系

识别到 {len(result.variable_dependencies)} 个依赖：

"""

        for i, dep in enumerate(result.variable_dependencies, 1):
            report += f"{i}. {dep.source} → {dep.target}\n"
            report += f"   - 类型: {dep.dependency_type}\n"
            report += f"   - 强度: {dep.strength:.1f}\n"
            report += f"   - 描述: {dep.description}\n"

        report += f"""

## 优化目标

目标: {', '.join(result.optimization_objectives) if result.optimization_objectives else '未明确'}

## 推荐求解策略

推荐策略: {', '.join(result.solving_strategies)}

## 推荐方法路径

{result.recommended_approach}

---

**生成时间**: {datetime.now().isoformat()}
**分类器版本**: enhanced-v1.1
"""
        return report

    def export_decomposition_to_json(self, result: DecompositionResult, output_path: str):
        """导出为 JSON 格式"""
        export_data = {
            "problem_type": result.problem_type.value,
            "complexity": result.complexity.value,
            "confidence_score": result.confidence_score,
            "variables": result.variables,
            "constraints": [
                {
                    "name": c.name,
                    "type": c.constraint_type,
                    "description": c.description,
                    "expression": c.expression,
                    "violation_penalty": c.violation_penalty
                }
                for c in result.constraints
            ],
            "optimization_objectives": result.optimization_objectives,
            "variable_dependencies": [
                {
                    "source": d.source,
                    "target": d.target,
                    "dependency_type": d.dependency_type,
                    "strength": d.strength,
                    "description": d.description
                }
                for d in result.variable_dependencies
            ],
            "solving_strategies": result.solving_strategies,
            "recommended_approach": result.recommended_approach
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


# 示例使用
if __name__ == "__main__":
    classifier = EnhancedProblemClassifier()

    # 示例 1: 蓝牙连接优化
    print("=" * 60)
    print("示例 1: 蓝牙连接稳定性优化")
    print("=" * 60)

    result1 = classifier.classify_problem(
        "蓝牙连接不稳定，经常断开，需要实现指数退避重连策略"
    )

    print(classifier.generate_decomposition_report(result1))

    # 示例 2: RSSI 图表性能优化
    print("\n" + "=" * 60)
    print("示例 2: RSSI 实时图表性能优化")
    print("=" * 60)

    result2 = classifier.classify_problem(
        "RSSI 实时图表更新太频繁导致界面卡顿，需要实现自适应更新间隔和动态数据点裁剪策略"
    )

    print(classifier.generate_decomposition_report(result2))

    # 示例 3: 导出 JSON
    print("\n" + "=" * 60)
    print("示例 3: 导出 JSON 格式")
    print("=" * 60)

    classifier.export_decomposition_to_json(
        result1,
        "/tmp/decomposition_result_1.json"
    )
    print("JSON 已导出到: /tmp/decomposition_result_1.json")

    classifier.export_decomposition_to_json(
        result2,
        "/tmp/decomposition_result_2.json"
    )
    print("JSON 已导出到: /tmp/decomposition_result_2.json")
