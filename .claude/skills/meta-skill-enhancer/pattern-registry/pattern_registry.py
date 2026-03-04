"""
模式积累引擎

负责记录和积累跨领域通用的设计模式、架构模式和最佳实践模式。
"""

import json
from typing import List, Dict, Set, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(Enum):
    """模式类别枚举"""
    ARCHITECTURAL = "architectural"
    UI = "ui"
    STATE_MANAGEMENT = "state-management"
    DATA = "data"
    ERROR_HANDLING = "error-handling"
    TESTING = "testing"
    PERFORMANCE = "performance"
    SECURITY = "security"
    NETWORKING = "networking"
    STORAGE = "storage"
    BLUETOOTH = "bluetooth"
    REACTIVE = "reactive"


class PatternComplexity(Enum):
    """模式复杂度"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class PatternFrequency(Enum):
    """模式使用频率"""
    COMMON = "common"
    FREQUENT = "frequent"
    OCCASIONAL = "occasional"
    RARE = "rare"


@dataclass
class Pattern:
    """模式定义"""
    id: str
    name: str
    category: PatternCategory
    complexity: PatternComplexity
    frequency: PatternFrequency = PatternFrequency.COMMON
    description: str
    problem: str
    solution: str
    implementation_example: Optional[str] = None
    applicable_domains: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    related_patterns: List[str] = field(default_factory=list)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    code_templates: Dict[str, str] = field(default_factory=dict)
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_used_at: Optional[str] = None
    usage_count: int = 0
    success_rate: float = 0.0  # 使用成功率 (0.0-1.0)
    community_validation: bool = False
    source_type: str = "discovered"  # discovered, official, community


@dataclass
class PatternRelationship:
    """模式关系"""
    pattern_id_1: str
    pattern_id_2: str
    relationship_type: str  # "composes", "extends", "complements", "conflicts_with"
    description: str


class PatternRegistry:
    """模式注册表"""

    def __init__(self, registry_file: str = "pattern_registry.json"):
        self.registry_file = registry_file
        self.patterns: Dict[str, Pattern] = {}
        self.relationships: List[PatternRelationship] = []
        self.domain_stats: Dict[str, int] = {}  # 领域模式统计

        self._load_registry()

    def register_pattern(self, pattern: Pattern) -> None:
        """注册新模式"""
        self.patterns[pattern.id] = pattern

        # 更新领域统计
        for domain in pattern.applicable_domains:
            self.domain_stats[domain] = self.domain_stats.get(domain, 0) + 1

        # 保存注册表
        self._save_registry()

        print(f"[模式注册表] 已注册模式: {pattern.name} (ID: {pattern.id})")

    def add_relationship(self, pattern_id_1: str, pattern_id_2: str,
                       relationship_type: str, description: str) -> None:
        """添加模式关系"""
        relationship = PatternRelationship(
            pattern_id_1=pattern_id_1,
            pattern_id_2=pattern_id_2,
            relationship_type=relationship_type,
            description=description
        )

        self.relationships.append(relationship)
        self._save_registry()

        print(f"[模式注册表] 已添加关系: {pattern_id_1} -{relationship_type}-> {pattern_id_2}")

    def update_pattern_usage(self, pattern_id: str, success: bool = True) -> None:
        """更新模式使用统计"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            pattern.usage_count += 1

            # 更新成功率
            if success:
                current_rate = pattern.success_rate
                pattern.success_rate = (current_rate * (pattern.usage_count - 1) + 1) / pattern.usage_count
            else:
                current_rate = pattern.success_rate
                pattern.success_rate = (current_rate * (pattern.usage_count - 1)) / pattern.usage_count

            pattern.last_used_at = datetime.now().isoformat()

            self._save_registry()

    def search_patterns(self, query: str, domain: Optional[str] = None,
                    category: Optional[PatternCategory] = None) -> List[Pattern]:
        """搜索模式"""
        results = []

        query_lower = query.lower()

        for pattern_id, pattern in self.patterns.items():
            # 域名过滤
            if domain and domain not in pattern.applicable_domains:
                continue

            # 类别过滤
            if category and pattern.category != category:
                continue

            # 关键词匹配
            match_score = 0
            if query_lower in pattern.name.lower():
                match_score += 10
            if query_lower in pattern.description.lower():
                match_score += 5
            if query_lower in pattern.problem.lower():
                match_score += 3

            # 标签匹配
            for tag in pattern.tags:
                if query_lower in tag.lower():
                    match_score += 2

            if match_score > 0:
                # 计算综合评分
                frequency_score = self._get_frequency_score(pattern.frequency)
                complexity_score = self._get_complexity_score(pattern.complexity)
                validation_score = 10 if pattern.community_validation else 0

                total_score = match_score + frequency_score + complexity_score + validation_score

                results.append({
                    'pattern': pattern,
                    'score': total_score
                })

        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)

        return [r['pattern'] for r in results[:20]]  # 返回前 20 个

    def get_trending_patterns(self, domain: Optional[str] = None,
                           limit: int = 10) -> List[Pattern]:
        """获取热门模式（基于使用频率和成功率）"""
        patterns_list = list(self.patterns.values())

        # 域名过滤
        if domain:
            patterns_list = [p for p in patterns_list if domain in p.applicable_domains]

        # 排序：成功率优先，然后是使用频率
        patterns_list.sort(
            key=lambda p: (p.success_rate, p.usage_count),
            reverse=True
        )

        return patterns_list[:limit]

    def get_recommended_patterns(self, context: Dict) -> List[Pattern]:
        """基于上下文推荐模式"""
        domain = context.get('domain', '')
        task_type = context.get('task_type', '')
        complexity = context.get('complexity', 'intermediate')

        recommendations = []

        for pattern_id, pattern in self.patterns.items():
            # 域名匹配
            if domain not in pattern.applicable_domains:
                continue

            # 复杂度匹配
            pattern_complexity_str = pattern.complexity.value
            if complexity and complexity not in pattern_complexity_str:
                continue

            # 任务类型匹配
            if task_type:
                task_type_matched = False
                if task_type in pattern.tags:
                    task_type_matched = True
                if task_type in pattern.name.lower():
                    task_type_matched = True

                if not task_type_matched:
                    continue

            # 计算推荐评分
            score = pattern.success_rate * 100 + pattern.usage_count * 10

            if pattern.community_validation:
                score += 50

            recommendations.append({
                'pattern': pattern,
                'score': score
            })

        # 按评分排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)

        return [r['pattern'] for r in recommendations[:10]]

    def analyze_pattern_composition(self, pattern_ids: List[str]) -> Dict:
        """分析模式组合的兼容性和效果"""
        analysis = {
            'selected_patterns': [],
            'composition_score': 0,
            'potential_conflicts': [],
            'synergy_score': 0,
            'recommendations': []
        }

        for pattern_id in pattern_ids:
            if pattern_id in self.patterns:
                pattern = self.patterns[pattern_id]
                analysis['selected_patterns'].append(pattern)

                # 检查冲突
                conflicts = self._get_conflicts(pattern_id, pattern_ids)
                if conflicts:
                    analysis['potential_conflicts'].extend(conflicts)

        # 计算组合评分
        if analysis['selected_patterns']:
            avg_success = sum(p.success_rate for p in analysis['selected_patterns']) / len(analysis['selected_patterns'])
            avg_usage = sum(p.usage_count for p in analysis['selected_patterns']) / len(analysis['selected_patterns'])

            analysis['composition_score'] = avg_success * 0.6 + avg_usage * 0.4

            # 检查协同效应
            synergy = self._check_synergy(pattern_ids)
            analysis['synergy_score'] = synergy

        # 生成建议
        if analysis['potential_conflicts']:
            analysis['recommendations'].append("注意：发现潜在冲突，建议调整模式选择")
        if analysis['synergy_score'] > 0.7:
            analysis['recommendations'].append("模式组合具有良好的协同效应")
        if analysis['composition_score'] < 0.5:
            analysis['recommendations'].append("建议考虑替代模式以提高成功率")

        return analysis

    def auto_discover_patterns(self, practices: List) -> List[Pattern]:
        """从最佳实践中自动发现模式"""
        discovered_patterns = []

        for practice in practices:
            # 分析实践，提取潜在模式

            # 1. 检测架构模式
            if 'architecture' in str(practice).lower() or 'clean' in str(practice).lower():
                pattern_id = f"auto_architecture_{practice.get('id', '')}"
                if pattern_id not in self.patterns:
                    pattern = Pattern(
                        id=pattern_id,
                        name=f"架构模式: {practice.get('title', '')}",
                        category=PatternCategory.ARCHITECTURAL,
                        complexity=PatternComplexity.INTERMEDIATE,
                        description="从最佳实践中发现的架构模式",
                        problem="如何组织应用架构",
                        solution="采用 Clean Architecture / MVVM 等架构模式",
                        applicable_domains=["flutter", "android", "ios", "web"],
                        tags=["architecture", "clean", "mvvm"],
                        code_templates={
                            "flutter": "// Clean Architecture 示例\nclass Provider {\n  // ...\n}",
                            "android": "// MVVM 示例\nclass ViewModel {\n  // ...\n}"
                        }
                    )
                    discovered_patterns.append(pattern)

            # 2. 检测状态管理模式
            if 'state' in str(practice).lower() or 'riverpod' in str(practice).lower():
                pattern_id = f"auto_state_{practice.get('id', '')}"
                if pattern_id not in self.patterns:
                    pattern = Pattern(
                        id=pattern_id,
                        name=f"状态管理模式: {practice.get('title', '')}",
                        category=PatternCategory.STATE_MANAGEMENT,
                        complexity=PatternComplexity.BASIC,
                        description="从最佳实践中发现的状态管理模式",
                        problem="如何管理应用状态",
                        solution="使用 Riverpod / Bloc / Provider 等状态管理库",
                        applicable_domains=["flutter"],
                        tags=["state-management", "riverpod", "bloc"]
                    )
                    discovered_patterns.append(pattern)

            # 3. 检测错误处理模式
            if 'error' in str(practice).lower() or 'exception' in str(practice).lower():
                pattern_id = f"auto_error_{practice.get('id', '')}"
                if pattern_id not in self.patterns:
                    pattern = Pattern(
                        id=pattern_id,
                        name=f"错误处理模式: {practice.get('title', '')}",
                        category=PatternCategory.ERROR_HANDLING,
                        complexity=PatternComplexity.BASIC,
                        description="从最佳实践中发现的错误处理模式",
                        problem="如何优雅地处理错误",
                        solution="使用 Try-Catch / Error Boundary / Result 类型等",
                        applicable_domains=["flutter", "android", "ios", "web"],
                        tags=["error-handling", "exception", "try-catch"]
                    )
                    discovered_patterns.append(pattern)

        # 注册发现的模式
        for pattern in discovered_patterns:
            self.register_pattern(pattern)

        return discovered_patterns

    def get_domain_statistics(self) -> Dict:
        """获取领域统计信息"""
        return {
            'total_patterns': len(self.patterns),
            'patterns_by_domain': dict(self.domain_stats),
            'patterns_by_category': self._get_patterns_by_category(),
            'trending_patterns': [p.name for p in self.get_trending_patterns(limit=5)],
            'most_used_patterns': sorted(
                self.patterns.values(),
                key=lambda p: p.usage_count,
                reverse=True
            )[:10],
            'successful_patterns': sorted(
                [p for p in self.patterns.values() if p.success_rate > 0.8],
                key=lambda p: p.success_rate,
                reverse=True
            )[:10]
        }

    def generate_pattern_report(self) -> str:
        """生成模式报告"""
        stats = self.get_domain_statistics()

        report_lines = [
            "# 模式注册表报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            f"总模式数: {stats['total_patterns']}",
            "",
            "## 按领域统计",
        ]

        for domain, count in stats['patterns_by_domain'].items():
            report_lines.append(f"- {domain}: {count} 个模式")

        report_lines.extend([
            "",
            "## 按类别统计",
        ])

        for category, patterns in stats['patterns_by_category'].items():
            report_lines.append(f"- {category.value}: {len(patterns)} 个模式")

        report_lines.extend([
            "",
            "## 热门模式（基于使用频率和成功率）",
            "",
        ])

        for pattern_name in stats['trending_patterns']:
            report_lines.append(f"- {pattern_name}")

        report_lines.extend([
            "",
            "## 成功模式（成功率 > 80%）",
            "",
        ])

        for pattern in stats['successful_patterns']:
            report_lines.append(f"- {pattern.name} (成功率: {pattern.success_rate:.2%}, 使用次数: {pattern.usage_count})")

        return "\n".join(report_lines)

    def _get_frequency_score(self, frequency: PatternFrequency) -> int:
        """获取频率评分"""
        scores = {
            PatternFrequency.COMMON: 10,
            PatternFrequency.FREQUENT: 8,
            PatternFrequency.OCCASIONAL: 5,
            PatternFrequency.RARE: 2
        }
        return scores.get(frequency, 5)

    def _get_complexity_score(self, complexity: PatternComplexity) -> int:
        """获取复杂度评分"""
        scores = {
            PatternComplexity.BASIC: 5,
            PatternComplexity.INTERMEDIATE: 10,
            PatternComplexity.ADVANCED: 15,
            PatternComplexity.EXPERT: 20
        }
        return scores.get(complexity, 10)

    def _get_conflicts(self, pattern_id: str, pattern_ids: List[str]) -> List[str]:
        """获取模式冲突"""
        conflicts = []

        for rel in self.relationships:
            if rel.pattern_id_1 == pattern_id and rel.pattern_id_2 in pattern_ids:
                conflicts.append(f"{rel.pattern_id_2}: {rel.description}")
            elif rel.pattern_id_2 == pattern_id and rel.pattern_id_1 in pattern_ids:
                conflicts.append(f"{rel.pattern_id_1}: {rel.description}")

        return conflicts

    def _check_synergy(self, pattern_ids: List[str]) -> float:
        """检查模式协同效应"""
        if len(pattern_ids) < 2:
            return 0.0

        synergy_score = 0.0
        checked_pairs = set()

        for i, id1 in enumerate(pattern_ids):
            for id2 in pattern_ids[i+1:]:
                pair_key = tuple(sorted([id1, id2]))

                if pair_key in checked_pairs:
                    continue

                checked_pairs.add(pair_key)

                if id1 in self.patterns and id2 in self.patterns:
                    pattern1 = self.patterns[id1]
                    pattern2 = self.patterns[id2]

                    # 检查互补关系
                    for rel in self.relationships:
                        if (rel.pattern_id_1 == id1 and rel.pattern_id_2 == id2 and
                            rel.relationship_type == "complements"):
                            synergy_score += 0.3
                        elif (rel.pattern_id_2 == id1 and rel.pattern_id_1 == id2 and
                              rel.relationship_type == "complements"):
                            synergy_score += 0.3

        # 归一化到 0-1
        return min(synergy_score / (len(pattern_ids) * (len(pattern_ids) - 1) / 2), 1.0)

    def _get_patterns_by_category(self) -> Dict[PatternCategory, List[Pattern]]:
        """按类别分组模式"""
        categories: Dict[PatternCategory, List[Pattern]] = {}

        for pattern in self.patterns.values():
            if pattern.category not in categories:
                categories[pattern.category] = []
            categories[pattern.category].append(pattern)

        return categories

    def _load_registry(self) -> None:
        """加载注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                patterns_data = data.get('patterns', {})
                for pattern_id, pattern_dict in patterns_data.items():
                    self.patterns[pattern_id] = Pattern(**pattern_dict)

                self.relationships = [
                    PatternRelationship(**rel) for rel in data.get('relationships', [])
                ]

                self.domain_stats = data.get('domain_stats', {})

                print(f"[模式注册表] 已从 {self.registry_file} 加载 {len(self.patterns)} 个模式")
        except FileNotFoundError:
            print(f"[模式注册表] 文件不存在，创建新注册表: {self.registry_file}")
            self._initialize_default_patterns()

    def _initialize_default_patterns(self) -> None:
        """初始化默认模式"""
        # 添加一些通用模式
        default_patterns = [
            Pattern(
                id="mvvm_pattern",
                name="MVVM (Model-View-ViewModel)",
                category=PatternCategory.ARCHITECTURAL,
                complexity=PatternComplexity.INTERMEDIATE,
                description="将应用分为 Model、View、ViewModel 三个部分",
                problem="如何组织代码结构，提高可测试性",
                solution="MVVM 架构将业务逻辑、视图逻辑和数据层分离",
                applicable_domains=["flutter", "android", "ios"],
                tags=["architecture", "mvvm", "separation"],
                source_type="official",
                community_validation=True
            ),
            Pattern(
                id="repository_pattern",
                name="Repository Pattern",
                category=PatternCategory.ARCHITECTURAL,
                complexity=PatternComplexity.BASIC,
                description="抽象数据访问层",
                problem="如何统一管理数据访问逻辑",
                solution="Repository 模式提供统一的数据访问接口",
                applicable_domains=["flutter", "android", "ios", "web"],
                tags=["data", "repository", "abstraction"],
                source_type="official",
                community_validation=True
            ),
            Pattern(
                id="observer_pattern",
                name="Observer Pattern",
                category=PatternCategory.STATE_MANAGEMENT,
                complexity=PatternComplexity.BASIC,
                description="定义对象之间的一对多依赖",
                problem="如何自动通知多个对象的状态变化",
                solution="Observer 模式让对象订阅并接收通知",
                applicable_domains=["flutter", "android", "ios", "web"],
                tags=["state", "observer", "notification"],
                source_type="official",
                community_validation=True
            ),
            Pattern(
                id="singleton_pattern",
                name="Singleton Pattern",
                category=PatternCategory.ARCHITECTURAL,
                complexity=PatternComplexity.BASIC,
                description="确保类只有一个实例",
                problem="如何控制资源的唯一访问",
                solution="Singleton 模式确保类只有一个实例并提供全局访问点",
                applicable_domains=["flutter", "android", "ios", "web"],
                tags=["architecture", "singleton", "pattern"],
                source_type="official",
                community_validation=True
            )
        ]

        for pattern in default_patterns:
            self.register_pattern(pattern)

    def _save_registry(self) -> None:
        """保存注册表"""
        output = {
            'version': '2.0',
            'last_updated': datetime.now().isoformat(),
            'total_patterns': len(self.patterns),
            'patterns': {pid: p.__dict__ for pid, p in self.patterns.items()},
            'relationships': [r.__dict__ for r in self.relationships],
            'domain_stats': self.domain_stats
        }

        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
