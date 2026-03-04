"""
自动优化建议生成器

基于问题特征和参考案例库，自动生成优化建议

功能：
1. 问题分析
2. 策略推荐
3. 参数建议
4. 优化路径规划
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
from pathlib import Path


class OptimizationType(Enum):
    """优化类型"""
    PERFORMANCE = "performance"
    MEMORY = "memory"
    CONNECTIVITY = "connectivity"
    STABILITY = "stability"
    USER_EXPERIENCE = "user_experience"
    RESOURCE_UTILIZATION = "resource_utilization"


class SuggestionPriority(Enum):
    """建议优先级"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class VariableSuggestion:
    """变量建议"""
    variable_name: str
    current_value: Optional[float]
    suggested_value: float
    reason: str
    expected_improvement: str


@dataclass
class StrategySuggestion:
    """策略建议"""
    strategy_name: str
    description: str
    priority: SuggestionPriority
    implementation_complexity: str  # simple, moderate, complex
    expected_benefit: str
    prerequisites: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    code_example: Optional[str] = None


@dataclass
class OptimizationSuggestion:
    """优化建议"""
    problem_type: str
    optimization_types: List[OptimizationType]
    strategy_suggestions: List[StrategySuggestion]
    variable_suggestions: List[VariableSuggestion]
    implementation_plan: List[str]
    estimated_effort: str
    expected_improvement: str


class OptimizationSuggestionGenerator:
    """自动优化建议生成器"""

    def __init__(self, reference_cases_path: str):
        """
        初始化优化建议生成器

        Args:
            reference_cases_path: 参考案例库路径
        """
        self.reference_cases_path = Path(reference_cases_path)
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict:
        """加载优化模式"""
        patterns_file = self.reference_cases_path / "patterns.json"

        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 默认模式库
        return {
            "bluetooth_connection": {
                "keywords": ["bluetooth", "connection", "connect", "reconnect", "disconnect", "timeout"],
                "variables": ["connection_timeout", "reconnect_delay", "max_retries"],
                "strategies": [
                    "exponential_backoff_reconnection",
                    "adaptive_timeout",
                    "smart_reconnection",
                    "signal_quality_monitoring"
                ],
                "optimization_types": ["connectivity", "stability", "user_experience"]
            },
            "rssi_chart": {
                "keywords": ["rssi", "chart", "graph", "plot", "signal", "strength"],
                "variables": ["update_interval", "max_data_points", "cache_size", "fps"],
                "strategies": [
                    "adaptive_update_interval",
                    "dynamic_data_culling",
                    "batch_rendering",
                    "object_pooling"
                ],
                "optimization_types": ["performance", "user_experience"]
            },
            "list_rendering": {
                "keywords": ["list", "scroll", "render", "lazy", "virtual"],
                "variables": ["item_count", "item_extent", "cache_extent", "page_size"],
                "strategies": [
                    "lazy_loading",
                    "item_extent_optimization",
                    "automatic_keep_alive",
                    "page_based_loading"
                ],
                "optimization_types": ["performance", "user_experience"]
            },
            "memory_management": {
                "keywords": ["memory", "leak", "dispose", "cleanup", "cache"],
                "variables": ["cache_size", "memory_limit", "gc_frequency"],
                "strategies": [
                    "resource_cleanup",
                    "weak_references",
                    "memory_monitoring",
                    "cache_management"
                ],
                "optimization_types": ["memory", "performance"]
            }
        }

    def generate_suggestions(self,
                             problem_description: str,
                             current_variables: Dict[str, float],
                             constraints: Optional[Dict] = None) -> OptimizationSuggestion:
        """
        生成优化建议

        Args:
            problem_description: 问题描述
            current_variables: 当前变量值
            constraints: 约束条件

        Returns:
            优化建议
        """
        # 1. 分析问题类型
        problem_type = self._classify_problem(problem_description)

        # 2. 确定优化类型
        optimization_types = self._determine_optimization_types(problem_type)

        # 3. 生成策略建议
        strategy_suggestions = self._generate_strategy_suggestions(
            problem_type,
            problem_description
        )

        # 4. 生成变量建议
        variable_suggestions = self._generate_variable_suggestions(
            problem_type,
            current_variables
        )

        # 5. 生成实施计划
        implementation_plan = self._generate_implementation_plan(
            strategy_suggestions,
            variable_suggestions
        )

        # 6. 估算工作量和预期改进
        estimated_effort, expected_improvement = self._estimate_effort_and_benefit(
            strategy_suggestions,
            variable_suggestions
        )

        return OptimizationSuggestion(
            problem_type=problem_type,
            optimization_types=optimization_types,
            strategy_suggestions=strategy_suggestions,
            variable_suggestions=variable_suggestions,
            implementation_plan=implementation_plan,
            estimated_effort=estimated_effort,
            expected_improvement=expected_improvement
        )

    def _classify_problem(self, description: str) -> str:
        """分类问题类型"""
        description_lower = description.lower()

        max_score = 0
        best_match = "general"

        for pattern_name, pattern_data in self.patterns.items():
            score = 0

            # 关键词匹配
            for keyword in pattern_data.get("keywords", []):
                if keyword in description_lower:
                    score += 1

            # 变量匹配
            for variable in pattern_data.get("variables", []):
                if variable in description_lower:
                    score += 2

            if score > max_score:
                max_score = score
                best_match = pattern_name

        return best_match

    def _determine_optimization_types(self, problem_type: str) -> List[OptimizationType]:
        """确定优化类型"""
        pattern_data = self.patterns.get(problem_type, {})

        optimization_types_str = pattern_data.get("optimization_types", [])

        optimization_types = []
        for type_str in optimization_types_str:
            try:
                optimization_types.append(OptimizationType(type_str))
            except ValueError:
                pass

        return optimization_types

    def _generate_strategy_suggestions(self,
                                       problem_type: str,
                                       description: str) -> List[StrategySuggestion]:
        """生成策略建议"""
        suggestions = []

        # 蓝牙连接优化建议
        if problem_type == "bluetooth_connection":
            suggestions.extend(self._bluetooth_connection_strategies())

        # RSSI 图表优化建议
        elif problem_type == "rssi_chart":
            suggestions.extend(self._rssi_chart_strategies())

        # 列表渲染优化建议
        elif problem_type == "list_rendering":
            suggestions.extend(self._list_rendering_strategies())

        # 内存管理优化建议
        elif problem_type == "memory_management":
            suggestions.extend(self._memory_management_strategies())

        # 通用优化建议
        else:
            suggestions.extend(self._general_optimization_strategies())

        return suggestions

    def _bluetooth_connection_strategies(self) -> List[StrategySuggestion]:
        """蓝牙连接优化策略"""
        return [
            StrategySuggestion(
                strategy_name="exponential_backoff_reconnection",
                description="使用指数退避策略进行重连，避免网络风暴，提高重连成功率",
                priority=SuggestionPriority.HIGH,
                implementation_complexity="moderate",
                expected_benefit="重连成功率提升 20-30%，减少不必要的连接尝试",
                prerequisites=["实现重连管理器", "记录重连历史"],
                risks=["初始连接可能较慢", "需要平衡重连延迟"],
                code_example="""```dart
Duration _calculateReconnectDelay(int attempt) {
  final baseDelay = const Duration(seconds: 1);
  return Duration(
    milliseconds: (baseDelay.inMilliseconds * pow(2, min(attempt - 1, 4)).toInt()
  );
}
```"""
            ),
            StrategySuggestion(
                strategy_name="adaptive_timeout",
                description="根据历史连接时间动态调整连接超时设置",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="moderate",
                expected_benefit="适应不同网络环境，连接成功率提升 10-15%",
                prerequisites=["记录连接超时历史", "实现超时计算算法"],
                risks=["需要足够的历史数据"],
                code_example="""```dart
Duration calculateConnectionTimeout() {
  if (_timeoutHistory.isEmpty) {
    return const Duration(seconds: 10);
  }
  final avg = _timeoutHistory.fold(Duration.zero, (sum, d) => sum + d) / _timeoutHistory.length;
  return avg;
}
```"""
            ),
            StrategySuggestion(
                strategy_name="signal_quality_monitoring",
                description="监控 RSSI 信号质量，基于信号波动调整重连策略",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="complex",
                expected_benefit="避免在不稳定连接上浪费时间，整体效率提升 15-20%",
                prerequisites=["实现 RSSI 监控", "分析信号波动"],
                risks=["增加了复杂度", "需要测试不同信号环境"],
                code_example="""```dart
bool isSignalStable(List<int> rssiHistory) {
  if (rssiHistory.length < 10) return true;
  final avg = rssiHistory.reduce((a, b) => a + b) / rssiHistory.length;
  final variance = rssiHistory.map((r) => pow(r - avg, 2)).reduce((a, b) => a + b) / rssiHistory.length;
  return variance < 100; // 阈值可调整
}
```"""
            )
        ]

    def _rssi_chart_strategies(self) -> List[StrategySuggestion]:
        """RSSI 图表优化策略"""
        return [
            StrategySuggestion(
                strategy_name="adaptive_update_interval",
                description="根据设备性能和 FPS 动态调整数据更新间隔",
                priority=SuggestionPriority.HIGH,
                implementation_complexity="moderate",
                expected_benefit="图表流畅度提升 40-50%，减少掉帧",
                prerequisites=["FPS 监控", "实现自适应算法"],
                risks=["需要平衡实时性和性能"],
                code_example="""```dart
void reportFps(int fps) {
  if (fps < 45) {
    _updateInterval = min(_updateInterval + 100, 2000);
  } else if (fps > 55) {
    _updateInterval = max(_updateInterval - 50, 200);
  }
}
```"""
            ),
            StrategySuggestion(
                strategy_name="dynamic_data_culling",
                description="分层降采样：近期数据高密度，历史数据低密度",
                priority=SuggestionPriority.HIGH,
                implementation_complexity="complex",
                expected_benefit="内存占用降低 60-70%，保持数据趋势可见性",
                prerequisites=["实现数据分层逻辑", "优化数据结构"],
                risks=["需要仔细设计降采样策略"],
                code_example="""```dart
List<FlSpot> cullDataPoints(List<FlSpot> points) {
  // 最近 10 秒：高密度
  // 最近 60 秒：中密度
  // 更早：低密度
  // 实现分层降采样
}
```"""
            ),
            StrategySuggestion(
                strategy_name="batch_rendering",
                description="批量收集数据点，减少渲染调用次数",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="simple",
                expected_benefit="渲染性能提升 20-30%，减少 UI 线程压力",
                prerequisites=["实现批量缓冲区", "控制批量大小"],
                risks=["可能增加延迟"],
                code_example="""```dart
void addDataPoint(FlSpot point) {
  _batchBuffer.add(point);
  if (_batchBuffer.length >= batchSize) {
    _flushBatch();
  }
}
```"""
            )
        ]

    def _list_rendering_strategies(self) -> List[StrategySuggestion]:
        """列表渲染优化策略"""
        return [
            StrategySuggestion(
                strategy_name="lazy_loading",
                description="使用 ListView.builder 懒加载列表项，只渲染可见项",
                priority=SuggestionPriority.HIGH,
                implementation_complexity="simple",
                expected_benefit="列表滚动流畅度提升 50-60%，内存占用降低 70-80%",
                prerequisites=["重构列表实现", "实现分页加载"],
                risks=["需要处理滚动加载逻辑"],
                code_example="""```dart
ListView.builder(
  itemCount: devices.length,
  itemBuilder: (context, index) {
    return DeviceListItem(device: devices[index]);
  },
)
```"""
            ),
            StrategySuggestion(
                strategy_name="item_extent_optimization",
                description="指定 itemExtent 或 prototypeItem，避免计算高度",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="simple",
                expected_benefit="渲染性能提升 15-20%",
                prerequisites=["确定固定高度", "或使用 prototypeItem"],
                risks=["列表项高度必须一致"],
                code_example="""```dart
ListView.builder(
  itemExtent: 80,
  // 或
  prototypeItem: ListTile(title: Text('Prototype')),
  itemCount: devices.length,
  itemBuilder: (context, index) { ... },
)
```"""
            ),
            StrategySuggestion(
                strategy_name="automatic_keep_alive",
                description="使用 AutomaticKeepAliveClientMixin 保持列表项状态",
                priority=SuggestionPriority.LOW,
                implementation_complexity="simple",
                expected_benefit="滚动时保持状态，用户体验提升",
                prerequisites=["修改列表项为 StatefulWidget"],
                risks=["略微增加内存占用"],
                code_example="""```dart
class DeviceListItem extends StatefulWidget {
  // ...
}
class _DeviceListItemState extends State<DeviceListItem>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;
  // ...
}
```"""
            )
        ]

    def _memory_management_strategies(self) -> List[StrategySuggestion]:
        """内存管理优化策略"""
        return [
            StrategySuggestion(
                strategy_name="resource_cleanup",
                description="在 dispose 中正确清理所有资源（Stream、Timer、Controller）",
                priority=SuggestionPriority.HIGH,
                implementation_complexity="simple",
                expected_benefit="避免内存泄漏，应用稳定性大幅提升",
                prerequisites=["实现 dispose 方法", "跟踪所有资源"],
                risks=["容易遗漏某些资源"],
                code_example="""```dart
@override
void dispose() {
  for (final subscription in _subscriptions) {
    subscription.cancel();
  }
  _timers.forEach((t) => t.cancel());
  _controllers.forEach((c) => c.close());
  super.dispose();
}
```"""
            ),
            StrategySuggestion(
                strategy_name="cache_management",
                description="实现智能缓存策略，定期清理过期缓存",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="moderate",
                expected_benefit="内存占用降低 30-40%，保持缓存有效性",
                prerequisites=["实现缓存管理器", "设置过期时间"],
                risks=["需要平衡缓存大小和命中率"],
                code_example="""```dart
class CacheManager {
  final int maxSize;
  final Duration ttl;

  void cleanExpiredCache() {
    final now = DateTime.now();
    _cache.removeWhere((key, value) =>
      now.difference(value.createdAt) > ttl
    );
  }
}
```"""
            )
        ]

    def _general_optimization_strategies(self) -> List[StrategySuggestion]:
        """通用优化策略"""
        return [
            StrategySuggestion(
                strategy_name="const_constructors",
                description="尽可能使用 const 构造函数，减少 Widget 重建",
                priority=SuggestionPriority.MEDIUM,
                implementation_complexity="simple",
                expected_benefit="减少 20-30% 的重建开销",
                prerequisites=["识别可 const 的组件"],
                risks=["可能需要调整组件设计"],
                code_example="""```dart
// 优化前
Container(
  padding: EdgeInsets.all(16),
  child: Text('Hello'),
)

// 优化后
const Padding(
  padding: EdgeInsets.all(16),
  child: Text('Hello'),
)
```"""
            ),
            StrategySuggestion(
                strategy_name="repaint_boundary",
                description="使用 RepaintBoundary 隔离频繁重绘的区域",
                priority=SuggestionPriority.LOW,
                implementation_complexity="simple",
                expected_benefit="减少不必要的重绘，性能提升 10-15%",
                prerequisites=["识别频繁重绘的 Widget"],
                risks=["增加 Widget 树深度"],
                code_example="""```dart
RepaintBoundary(
  child: AnimatedContainer(
    duration: Duration(milliseconds: 300),
    // ...
  ),
)
```"""
            )
        ]

    def _generate_variable_suggestions(self,
                                       problem_type: str,
                                       current_variables: Dict[str, float]) -> List[VariableSuggestion]:
        """生成变量建议"""
        suggestions = []

        # 蓝牙连接变量建议
        if problem_type == "bluetooth_connection":
            suggestions.extend(self._bluetooth_connection_variables(current_variables))

        # RSSI 图表变量建议
        elif problem_type == "rssi_chart":
            suggestions.extend(self._rssi_chart_variables(current_variables))

        # 列表渲染变量建议
        elif problem_type == "list_rendering":
            suggestions.extend(self._list_rendering_variables(current_variables))

        return suggestions

    def _bluetooth_connection_variables(self, current: Dict[str, float]) -> List[VariableSuggestion]:
        """蓝牙连接变量建议"""
        suggestions = []

        if "connection_timeout" in current:
            timeout = current["connection_timeout"]
            if timeout < 10:
                suggestions.append(VariableSuggestion(
                    variable_name="connection_timeout",
                    current_value=timeout,
                    suggested_value=15.0,
                    reason="当前超时时间过短，可能导致连接成功率低",
                    expected_improvement="连接成功率提升 10-15%"
                ))
            elif timeout > 30:
                suggestions.append(VariableSuggestion(
                    variable_name="connection_timeout",
                    current_value=timeout,
                    suggested_value=20.0,
                    reason="当前超时时间过长，影响用户体验",
                    expected_improvement="连接等待时间缩短 30-40%"
                ))

        if "reconnect_delay" in current:
            delay = current["reconnect_delay"]
            if delay < 2:
                suggestions.append(VariableSuggestion(
                    variable_name="reconnect_delay",
                    current_value=delay,
                    suggested_value=3.0,
                    reason="重连延迟过短，可能造成网络风暴",
                    expected_improvement="避免频繁重连，网络效率提升"
                ))

        return suggestions

    def _rssi_chart_variables(self, current: Dict[str, float]) -> List[VariableSuggestion]:
        """RSSI 图表变量建议"""
        suggestions = []

        if "update_interval" in current:
            interval = current["update_interval"]
            if interval < 300:
                suggestions.append(VariableSuggestion(
                    variable_name="update_interval",
                    current_value=interval,
                    suggested_value=500.0,
                    reason="更新频率过高，可能导致卡顿",
                    expected_improvement="图表流畅度提升 20-30%"
                ))

        if "max_data_points" in current:
            max_points = current["max_data_points"]
            if max_points > 500:
                suggestions.append(VariableSuggestion(
                    variable_name="max_data_points",
                    current_value=max_points,
                    suggested_value=300.0,
                    reason="数据点过多，影响渲染性能",
                    expected_improvement="渲染速度提升 30-40%"
                ))

        return suggestions

    def _list_rendering_variables(self, current: Dict[str, float]) -> List[VariableSuggestion]:
        """列表渲染变量建议"""
        suggestions = []

        if "page_size" in current:
            page_size = current["page_size"]
            if page_size > 50:
                suggestions.append(VariableSuggestion(
                    variable_name="page_size",
                    current_value=page_size,
                    suggested_value=20.0,
                    reason="每页加载过多，影响初始加载速度",
                    expected_improvement="初始加载时间缩短 40-50%"
                ))

        return suggestions

    def _generate_implementation_plan(self,
                                      strategy_suggestions: List[StrategySuggestion],
                                      variable_suggestions: List[VariableSuggestion]) -> List[str]:
        """生成实施计划"""
        plan = []

        # 按优先级排序策略建议
        high_priority_strategies = [
            s for s in strategy_suggestions
            if s.priority == SuggestionPriority.HIGH
        ]
        medium_priority_strategies = [
            s for s in strategy_suggestions
            if s.priority == SuggestionPriority.MEDIUM
        ]
        low_priority_strategies = [
            s for s in strategy_suggestions
            if s.priority == SuggestionPriority.LOW
        ]

        # 第一阶段：高优先级策略
        if high_priority_strategies:
            plan.append("## 第一阶段：高优先级优化 (1-2 周)")
            for strategy in high_priority_strategies:
                plan.append(f"- {strategy.strategy_name}: {strategy.description}")
                plan.append(f"  复杂度: {strategy.implementation_complexity}")
                plan.append(f"  预期收益: {strategy.expected_benefit}")
            plan.append("")

        # 第二阶段：变量调整
        if variable_suggestions:
            plan.append("## 第二阶段：参数调优 (1 周)")
            for var_suggestion in variable_suggestions:
                plan.append(f"- {var_suggestion.variable_name}: {var_suggestion.current_value} → {var_suggestion.suggested_value}")
                plan.append(f"  原因: {var_suggestion.reason}")
                plan.append(f"  预期: {var_suggestion.expected_improvement}")
            plan.append("")

        # 第三阶段：中优先级策略
        if medium_priority_strategies:
            plan.append("## 第三阶段：中优先级优化 (2-3 周)")
            for strategy in medium_priority_strategies:
                plan.append(f"- {strategy.strategy_name}: {strategy.description}")
                plan.append(f"  复杂度: {strategy.implementation_complexity}")
                plan.append(f"  预期收益: {strategy.expected_benefit}")
            plan.append("")

        # 第四阶段：低优先级策略
        if low_priority_strategies:
            plan.append("## 第四阶段：低优先级优化 (可选)")
            for strategy in low_priority_strategies:
                plan.append(f"- {strategy.strategy_name}: {strategy.description}")
            plan.append("")

        return plan

    def _estimate_effort_and_benefit(self,
                                    strategy_suggestions: List[StrategySuggestion],
                                    variable_suggestions: List[VariableSuggestion]) -> Tuple[str, str]:
        """估算工作量和预期改进"""
        # 估算工作量
        complexity_scores = {
            "simple": 1,
            "moderate": 3,
            "complex": 5
        }

        total_complexity = sum(
            complexity_scores.get(s.implementation_complexity, 3)
            for s in strategy_suggestions
        ) + len(variable_suggestions)

        if total_complexity < 5:
            effort = "1-2 周"
        elif total_complexity < 15:
            effort = "3-4 周"
        elif total_complexity < 30:
            effort = "1-2 月"
        else:
            effort = "3-6 月"

        # 估算预期改进
        high_priority_count = sum(
            1 for s in strategy_suggestions
            if s.priority == SuggestionPriority.HIGH
        )

        if high_priority_count >= 2:
            improvement = "显著提升 (预期改进 50%+)"
        elif high_priority_count >= 1:
            improvement = "明显提升 (预期改进 20-50%)"
        else:
            improvement = "适度提升 (预期改进 10-20%)"

        return effort, improvement


# 示例使用
if __name__ == "__main__":
    generator = OptimizationSuggestionGenerator(
        reference_cases_path="/Users/administruter/Desktop/skill_factory/.claude/skills/micro-diff-factory/references/micro-diff-cases"
    )

    # 示例 1: 蓝牙连接优化建议
    print("=" * 60)
    print("蓝牙连接优化建议")
    print("=" * 60)
    suggestion1 = generator.generate_suggestions(
        problem_description="蓝牙连接不稳定，经常断开，重连成功率低",
        current_variables={
            "connection_timeout": 5.0,
            "reconnect_delay": 1.0,
            "max_retries": 2
        }
    )

    print(f"问题类型: {suggestion1.problem_type}")
    print(f"优化类型: {[t.value for t in suggestion1.optimization_types]}")
    print(f"预计工作量: {suggestion1.estimated_effort}")
    print(f"预期改进: {suggestion1.expected_improvement}")
    print("\n策略建议:")
    for s in suggestion1.strategy_suggestions:
        print(f"\n  [{s.priority.value}] {s.strategy_name}")
        print(f"  描述: {s.description}")
        print(f"  预期收益: {s.expected_benefit}")
        print(f"  复杂度: {s.implementation_complexity}")

    print("\n" + "=" * 60)
    print("RSSI 图表优化建议")
    print("=" * 60)
    suggestion2 = generator.generate_suggestions(
        problem_description="RSSI 图表更新太频繁，导致界面卡顿，内存占用高",
        current_variables={
            "update_interval": 100.0,
            "max_data_points": 1000.0,
            "fps": 30.0
        }
    )

    print(f"问题类型: {suggestion2.problem_type}")
    print(f"优化类型: {[t.value for t in suggestion2.optimization_types]}")
    print(f"预计工作量: {suggestion2.estimated_effort}")
    print(f"预期改进: {suggestion2.expected_improvement}")
    print("\n实施计划:")
    for line in suggestion2.implementation_plan:
        print(line)
