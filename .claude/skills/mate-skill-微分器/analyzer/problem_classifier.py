"""
微分问题识别和分类模块

负责分析和分类微分拆解问题，自动识别问题类型、变量、约束和优化目标。
"""

import json
import re
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class ProblemType(Enum):
    """问题类型"""
    CODE_PERFORMANCE = "code_performance"
    CONNECTIVITY = "connectivity"
    STATE_MANAGEMENT = "state_management"
    DATA_VISUALIZATION = "data_visualization"
    OPTIMIZATION = "optimization"
    ALGORITHM = "algorithm"
    PROBABILITY = "probability"
    BUSINESS_LOGIC = "business_logic"


class ProblemComplexity(Enum):
    """问题复杂度"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class ProblemCategory(Enum):
    """问题分类"""
    OPTIMIZATION_OBJECTIVE = "optimization_objective"
    RESOURCE_ALLOCATION = "resource_allocation"
    CONSTRAINT_MANIPULATION = "constraint_manipulation"
    SENSITIVITY_ANALYSIS = "sensitivity_analysis"
    BOUNDARY_DISCOVERY = "boundary_discovery"


@dataclass
class IdentifiedProblem:
    """识别到的问题"""
    problem_id: str
    name: str
    problem_type: ProblemType
    complexity: ProblemComplexity
    category: ProblemCategory
    description: str
    key_variables: List[str]
    relationships: List[Tuple[str, str, float]]  # (var1, var2, correlation)
    constraints: List[str]
    optimization_objectives: List[str]
    potential_optimizations: List[str]


class ProblemClassifier:
    """问题分类器"""

    # 代码性能关键词模式
    code_perf_patterns = {
        'rendering': ['列表渲染', '懒加载', '虚拟列表', '列表视图', 'listview', 'lazy list'],
        'chart': ['图表', '绘制', '渲染', '帧率', 'fps', '动画', '过渡', 'fl chart', '更新', '刷新'],
        'memory': ['内存', '缓存', '内存泄漏', 'memory leak', '占用', 'gc', '垃圾回收'],
        'performance': ['性能', '优化', '卡顿', '流畅', '慢', '延迟', 'timeout', '超时']
    }

    # 连接性关键词模式
    connectivity_patterns = {
        'bluetooth': ['蓝牙', 'bluetooth connection', 'ble', '低功耗蓝牙', '经典蓝牙', 'classic bluetooth',
                        '连接', 'connect', '断开', 'disconnect', '重连', 'reconnect',
                        '断线', '断线重连', '状态', 'status', 'stable', 'stable connection',
                        '不稳定', '连接稳定性', '带宽', 'bandwidth', '吞吐量', 'throughput'],
                        '配对', 'pairing', 'connection lost', '连接丢失', '超时', 'timeout'],
                        '扫描', 'scan', 'discover', 'discovery', '设备发现', 'device discovery'],
                        '信号', 'signal', '强度', 'rssi', '信号强度', 'signal strength'],
                        '传输', 'transfer', '数据传输', 'data transfer', '吞吐量', 'throughput'],
                        '连接池', 'connection pool'],
        'rssi': ['rssi', '信号', 'signal', 'signal strength', '信号强度', 'rssi值', 'rssi value',
                        '波动', 'fluctuation', '信号波动', '抖动', 'jitter',
                        '图表', 'chart', '更新', '刷新', '实时', 'realtime', '监控', 'monitor'],
                        '数据点', 'data point', 'data point', '数据点数', 'max data points'],
                        '阈值', 'threshold', 'throttle', '节流']
    }

    # 状态管理关键词模式
    state_patterns = {
        'persistence': ['持久化', 'persistence', '存储', 'storage', '缓存', 'cache',
                        'shared_preferences', 'sharedprefs', 'hive', 'sqflite', 'objectbox', '数据库', 'database',
                        '状态', 'state', 'state management', '状态管理', '管理', 'management'],
                        '订阅', 'subscribe', 'subscription', '通知', 'notify', 'observer'],
                        'riverpod', 'provider', 'state', 'notifier', 'stream', 'stream controller'],
                        'provider scope', 'scoped', '状态作用域', 'family', 'family', 'widget family'],
                        '重建', 'rebuild', 'dispose', 'dispose all']
    }

    # 优化问题关键词模式
    optimization_patterns = {
        'timing': ['时间', 'timing', '更新间隔', 'update interval', '频率', 'frequency', '周期', 'period',
                     '轮询', 'polling', '采样', 'sample', '采样率', 'sample rate',
                     '延迟', 'delay', 'debounce', '防抖', '节流', 'throttle'],
                     '缓存', 'cache', 'caching', 'memory cache', '内存缓存'],
                     '批处理', 'batch', 'batch processing', '批处理'],
                     '异步', 'async', '异步处理', '并发处理'],
                     '性能', 'performance', '优化', '提升', 'improve', 'improve performance']
    }

    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> None:
        """加载问题分类模式"""
        # 这里可以加载预定义的模式或从文件读取
        self.patterns = {
            'code_performance': {
                'lazy_list': ['ListView.builder', 'LazyListView'],
                'virtual_list': ['ListView.builder', 'VirtualListView'],
                'chart_update': ['setState', 'setState', 'stream update'],
                'memory_leak': ['内存', 'cache', 'leak']
            },
            'connectivity': {
                'protocol_type': ['protocol', 'bluetooth', 'ble', 'classic'],
                'rssi_monitoring': ['chart', 'update', 'refresh', 'interval', 'frequency'],
                'reconnection': ['重连', 'reconnect', 'retry', 'exponential', 'linear']
            },
            'optimization_objective': {
                'throughput': ['吞吐量', '带宽', 'bandwidth', '性能', 'performance'],
                'latency': ['延迟', '延迟', 'timeout', '超时'],
                'resource': ['资源', '内存', 'cpu', 'battery'],
                'quality': ['质量', '连接质量', '稳定性', 'stability']
            }
        }

    def classify_problem(self, description: str, problem_context: Optional[Dict] = None) -> IdentifiedProblem:
        """
        分类问题描述

        Args:
            description: 问题描述
            problem_context: 问题上下文（包含领域等）

        Returns:
            IdentifiedProblem 识别到的问题
        """
        description_lower = description.lower()

        # 1. 识别问题类型
        problem_type = self._identify_problem_type(description_lower)

        # 2. 识别复杂度
        complexity = self._assess_complexity(description_lower)

        # 3. 识别分类
        category = self._identify_category(description_lower, problem_type)

        # 4. 提取关键变量
        variables = self._extract_key_variables(description_lower, problem_type)

        # 5. 识别关系
        relationships = self._identify_relationships(description_lower, problem_type, variables)

        # 6. 识别约束
        constraints = self._identify_constraints(description_lower)

        # 7. 识别优化目标
        objectives = self._identify_optimization_objectives(description_lower, problem_type)

        # 8. 生成优化建议
        optimizations = self._generate_optimizations(description_lower, problem_type, variables, constraints)

        # 生成唯一 ID
        problem_id = f"problem_{self._generate_id()}"

        return IdentifiedProblem(
            problem_id=problem_id,
            name=description,
            problem_type=problem_type,
            complexity=complexity,
            category=category,
            description=description,
            key_variables=variables,
            relationships=relationships,
            constraints=constraints,
            optimization_objectives=objectives,
            potential_optimizations=optimizations
        )

    def _identify_problem_type(self, description: str) -> ProblemType:
        """识别问题类型"""
        # 检查各类别的关键词
        scores = {
            ProblemType.CODE_PERFORMANCE: self._match_keywords(description, self.code_perf_patterns.get('rendering', []), 5),
            ProblemType.CODE_PERFORMANCE: self._match_keywords(description, self.code_perf_patterns.get('chart', []), 5),
            ProblemType.CODE_PERFORMANCE: self._match_keywords(description, self.code_perf_patterns.get('memory', []), 5),
        ProblemType.CONNECTIVITY: self._match_keywords(description, self.connectivity_patterns, {}), 5),
        ProblemType.CONNECTIVITY: self._match_keywords(description, self.connectivity_patterns.get('rssi', []), 5),
            ProblemType.CONNECTIVITY: self._match_keywords(description, self.connectivity_patterns.get('reconnection', []), 5),
            ProblemType.STATE_MANAGEMENT: self._match_keywords(description, self.state_patterns.get('persistence', []), 5),
            ProblemType.OPTIMIZATION: self._match_keywords(description, self.optimization_patterns.get('timing', []), 5),
        }

        # 返回分数最高的类型
        max_score_type = max(scores.keys(), key=lambda k: scores[k])

        return max_score_type

    def _match_keywords(self, description: str, patterns: List[str], weight: int = 1) -> int:
        """匹配关键词"""
        score = 0
        for pattern in patterns:
            if pattern in description:
                score += weight

        return score

    def _assess_complexity(self, description: str) -> ProblemComplexity:
        """评估问题复杂度"""
        indicators = {
            'simple': ['简单', 'basic', 'easy', 'minor', 'small'],
            'moderate': ['中等', 'intermediate', 'medium', 'normal', 'standard'],
            'complex': ['复杂', '困难', 'hard', 'advanced', 'major', 'significant']
        }

        description_lower = description.lower()

        # 基于关键词的启发式评估
        if any(ind in description_lower for ind in indicators['simple']):
            return ProblemComplexity.SIMPLE
        elif any(ind in description_lower for ind in indicators['complex']):
            return ProblemComplexity.COMPLEX
        elif any(ind in description_lower for ind in indicators['moderate']):
            return ProblemComplexity.MODERATE
        else:
            return ProblemComplexity.EXPERT

    def _identify_category(self, description: str, problem_type: ProblemType) -> ProblemCategory:
        """识别问题分类"""
        # 根据问题类型返回默认分类
        category_map = {
            ProblemType.CODE_PERFORMANCE: ProblemCategory.OPTIMIZATION_OBJECTIVE,
            ProblemType.CONNECTIVITY: ProblemCategory.RESOURCE_ALLOCATION,
            ProblemType.STATE_MANAGEMENT: ProblemCategory.STATE_MANAGEMENT,
            ProblemType.DATA_VISUALIZATION: ProblemCategory.OPTIMIZATION_OBJECTIVE,
            ProblemType.OPTIMIZATION: ProblemCategory.OPTIMIZATION_OBJECTIVE,
        }

        return category_map.get(problem_type, ProblemCategory.OPTIMIZATION_OBJECTIVE)

    def _extract_key_variables(self, description: str, problem_type: ProblemType) -> List[str]:
        """提取关键变量"""
        variables = []

        # 根据问题类型提取特定变量
        if problem_type == ProblemType.CODE_PERFORMANCE:
            variables.extend(self._extract_code_perf_variables(description))
        elif problem_type == ProblemType.CONNECTIVITY:
            variables.extend(self._extract_connectivity_variables(description))
        elif problem_type == ProblemType.OPTIMIZATION:
            variables.extend(self._extract_optimization_variables(description))

        # 提取通用变量（数字、百分比、布尔、字符串）
        # 识别变量名
        variable_pattern = r'(?:\s*)(\w+)(\d+(?:\.\d+)'
        matches = re.findall(variable_pattern, description)

        for match in matches:
            var_name = match.group(2) if match.group(2) else match.group(1)
            variables.append(var_name)

        return list(set(variables))

    def _extract_code_perf_variables(self, description: str) -> List[str]:
        """提取代码性能变量"""
        return [
            var for var in self.code_perf_patterns.keys()
            if var in description
        ]

    def _extract_connectivity_variables(self, description: str) -> List[str]:
        """提取连接性变量"""
        return [
            var for var in self.connectivity_patterns.keys()
            if var in description
        ]

    def _extract_optimization_variables(self, description: str) -> List[str]:
        """提取优化变量"""
        variables = []

        if '频率' in description or 'period' in description:
            variables.append('update_interval')

        if '延迟' in description or 'debounce' in description:
            variables.append('debounce_delay')

        if '数据点' in description or '阈值' in description:
            variables.append('max_data_points')

        if '内存' in description or '缓存' in description:
            variables.append('cache_strategy')

        if '列表' in description and ('lazy' in description or '虚拟' in description):
            variables.append('list_rendering_mode')

        return variables

    def _identify_relationships(self, description: str, problem_type: ProblemType,
                           variables: List[str]) -> List[Tuple[str, str, float]]:
        """识别变量关系"""
        relationships = []

        # 简单规则：关键词相邻表示相关
        desc_words = re.findall(r'\b(\w+\b)', description, re.IGNORECASE)
        for words in desc_words:
            # 提取两个变量
            vars_in_words = [v for v in variables if v in words[0]]
            if len(vars_in_words) >= 2:
                # 默认中等正相关
                for v in vars_in_words:
                    relationships.append((v, vars_in_words[1], 0.5))
                break

        # 约束相关
        if any(var in description for var in ['min', 'max', '<=', '>=', 'timeout', 'interval']):
            # 识别边界对
            # 例如：timeout <= 30s 和 interval >= 1000ms
            relationships.append(('timeout', 'update_interval', 0.8))

        return relationships

    def _identify_constraints(self, description: str) -> List[str]:
        """识别约束条件"""
        constraints = []

        # 硬约束模式
        if '不' in description or '禁止' in description:
            if '不小于' in description:
                # 提取下界
                match = re.search(r'不小于\s*(\d+(?:\.\d+)', description)
                if match:
                    constraints.append(f"变量下限: {match.group(2)}")

        if '不大于' in description:
            # 提取上界
                match = re.search(r'不大于\s*(\d+(?:\.\d+)', description)
                if match:
                    constraints.append(f"变量上限: {match.group(2)}")

        # 枚举约束
        enum_matches = re.findall(r'(\b(?:或|和)(?:\d+(?:\.\d+))\b', description)
        for match in enum_matches:
            values = match.group(2).split('或')
            constraints.extend([f"枚举值: {value}" for value in values])

        return list(set(constraints))

    def _identify_optimization_objectives(self, description: str, problem_type: ProblemType) -> List[str]:
        """识别优化目标"""
        objectives = []

        # 根据问题类型提取目标
        if problem_type == ProblemType.CODE_PERFORMANCE:
            objectives.extend(['内存占用', '渲染帧率', '响应时间'])
        elif problem_type == ProblemType.CONNECTIVITY:
            objectives.extend(['连接成功率', '连接稳定性', '吞吐量', '带宽利用率'])
        elif problem_type == ProblemType.OPTIMIZATION:
            if '更新间隔' in description:
                objectives.append('平衡实时性和性能')
            if '数据点' in description:
                objectives.append('平衡数据新鲜度和内存')
            if '列表渲染' in description:
                objectives.append('优化列表渲染性能')

        return objectives

    def _generate_optimizations(self, description: str, problem_type: ProblemType,
                             variables: List[str], constraints: List[str]) -> List[str]:
        """生成优化建议"""
        optimizations = []

        # 基于约束生成建议
        if 'min' in str(constraints) or 'max' in str(constraints):
            for constraint in constraints:
                if 'min' in constraint and 'max' in constraint:
                    # 提取变量范围
                    match = re.search(r'min\s*(\d+(?:\.\d+).*max\s*(\d+(?:\.\d+))', constraint)
                    if match:
                        var = match.group(2)
                        optimizations.append(f"使用二分查找优化 {var}")

        # 基于变量生成建议
        for var in variables:
            if 'interval' in var:
                if problem_type == ProblemType.CONNECTIVITY and 'rssi' in description:
                    optimizations.append('考虑根据信号强度动态调整更新间隔')
                elif problem_type == ProblemType.OPTIMIZATION:
                    optimizations.append(f'使用 {var} 进行性能调优')

        # 生成默认优化建议
        if not optimizations:
            optimizations.append('建议使用性能分析工具（DevTools）')

        return list(set(optimizations))

    def _generate_id(self) -> str:
        """生成唯一 ID"""
        import time
        return f"prob_{int(time.time() * 1000000)}"
    def _load_patterns(self) -> None:
        """从文件加载问题分类模式"""
        # 这里可以加载预定义的模式或从配置文件读取
        pass
