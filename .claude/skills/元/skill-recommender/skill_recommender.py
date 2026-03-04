"""
技能推荐引擎（Skill Recommendation Engine）

基于问题类型和上下文，自动推荐最优的技能组合

功能：
1. 基于问题域分析推荐最相关技能
2. 考虑技能之间的依赖关系
3. 提供技能组合的执行路径
4. 生成推荐报告
"""

import json
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime


class ProblemDomain(Enum):
    """问题领域"""
    BLUETOOTH = "bluetooth"
    RSSI = "rssi"
    PERFORMANCE = "performance"
    ALGORITHM = "algorithm"
    NETWORK = "network"
    DATABASE = "database"
    UI_UX = "ui_ux"
    SECURITY = "security"
    TESTING = "testing"
    OPTIMIZATION = "optimization"
    GENERAL = "general"


class SkillType(Enum):
    """技能类型"""
    META_SKILL = "meta_skill"
    APPLICATION_SKILL = "application_skill"
    UTILITY = "utility"


@dataclass
class Skill:
    """技能"""
    name: str
    type: SkillType
    category: str
    description: str
    path: str
    domain: ProblemDomain  # 这里可以导入
    capabilities: List[str]


@dataclass
class SkillRecommendation:
    """技能推荐"""
    skills: List[Skill]
    reasoning: str
    confidence: float = 0.0
    execution_order: List[str] = field(default_factory=list)  # 技能调用顺序
    estimated_duration: float = 0.0  # 预估总执行时间（分钟）


class SkillRecommender:
    """技能推荐引擎"""

    def __init__(self, skills_db_path: str):
        """
        初始化推荐引擎

        Args:
            skills_db_path: 技能数据库路径
        """
        self.skills_db_path = Path(skills_db_path)

        # 技能数据库（从 scan_results 加载）
        self.all_skills: Dict[str, Skill] = {}
        self.skills_by_domain: Dict[str, List[Skill]] = {}
        self.skills_by_category: Dict[str, List[Skill]] = {}
        self.skill_dependencies: Dict[str, Set[str]] = {}  # 技能依赖关系
        self.load_skills_database()

    def load_skills_database(self):
        """加载技能数据库"""
        scan_results = Path("/Users/administruter/Desktop/skill_factory/.claude/skills/元/元-skill-扫描器/output")

        if not scan_results.exists():
            print("警告：未找到扫描结果，使用默认技能库")
            return

        # 加载扫描结果
        with open(scan_results / "skill-catalog.json", 'r', encoding='utf-8') as f:
            scan_data = json.load(f)

        # 构建 all_skills 字典
        for skill_data in scan_data.get("skills_list", []):
            # 解析领域
            skill_name_lower = skill_data.get("name", "").lower()
            skill_desc_lower = skill_data.get("description", "").lower()
            skill_category = skill_data.get("category", "").lower()

            # 智能领域匹配
            domain = ProblemDomain.GENERAL
            if any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["bluetooth", "蓝牙", "连接", "设备", "scan"]):
                domain = ProblemDomain.BLUETOOTH
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["rssi", "signal", "信号", "图表", "chart", "实时"]):
                domain = ProblemDomain.RSSI
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["性能", "优化", "快", "慢", "卡顿", "内存", "fps"]):
                domain = ProblemDomain.PERFORMANCE
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["算法", "排序", "搜索", "tree", "dp", "分治", "动态规划"]):
                domain = ProblemDomain.ALGORITHM
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["网络", "http", "请求", "api", "接口"]):
                domain = ProblemDomain.NETWORK
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["数据库", "db", "sql", "查询"]):
                domain = ProblemDomain.DATABASE
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["ui", "界面", "design", "布局", "组件", "widget"]):
                domain = ProblemDomain.UI_UX
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["安全", "认证", "加密", "token"]):
                domain = ProblemDomain.SECURITY
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["测试", "qa", "质量", "单元测试"]):
                domain = ProblemDomain.TESTING
            elif any(kw in skill_name_lower or kw in skill_desc_lower for kw in ["优化", "调优", "微服务", "异步", "缓存"]):
                domain = ProblemDomain.OPTIMIZATION
            elif "问题穷举" in skill_name_lower or "generator" in skill_name_lower:
                domain = ProblemDomain.GENERAL  # 使用 GENERAL 作为问题分析
            elif "扫描器" in skill_name_lower:
                domain = ProblemDomain.GENERAL
            elif "检查器" in skill_name_lower:
                domain = ProblemDomain.GENERAL
            elif "优化器" in skill_name_lower:
                domain = ProblemDomain.OPTIMIZATION

            skill = Skill(
                name=skill_data.get("name", ""),
                type=SkillType.META_SKILL if skill_data.get("type") == "meta" else SkillType.APPLICATION_SKILL,
                category=skill_data.get("category", ""),
                description=skill_data.get("description", ""),
                path=skill_data.get("path", ""),
                domain=domain,
                capabilities=[]  # 这里可以解析 SKILL.md 来获取能力
            )
            self.all_skills[skill.name] = skill

            # 按领域分类（使用枚举值）
            self.skills_by_domain.setdefault(domain.value, []).append(skill)

            # 按类别分类
            category = skill_data.get("category", "")
            self.skills_by_category.setdefault(category, []).append(skill)

        print(f"加载了 {len(self.all_skills)} 个技能")

    def _build_skill_dependencies(self):
        """构建技能依赖关系"""
        # 解析 SKILL.md 文件提取依赖
        for skill_name, skill in self.all_skills.items():
            skill_file = Path(skill.path) / "SKILL.md"
            if skill_file.exists():
                dependencies = self._extract_dependencies_from_skillmd(skill_file)
                self.skill_dependencies[skill_name] = dependencies

    def _extract_dependencies_from_skillmd(self, skill_file: Path) -> Set[str]:
        """从 SKILL.md 提取依赖"""
        dependencies = set()
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单提取：查找 "requires" 或 "依赖" 关键词
                if "requires:" in content or "依赖:" in content:
                    # 提取所需的技能名称
                    lines = content.split('\n')
                    for line in lines:
                        if "requires:" in line or "依赖:" in line:
                            # 提取技能名称
                            words = line.split()
                            for word in words:
                                if word.strip() and word not in ["requires:", "依赖:"]:
                                    dependencies.add(word.strip().lower().strip('"'))

        except Exception as e:
            print(f"警告：无法解析 {skill_file} 的依赖关系: {e}")

        return dependencies

    def recommend_skills(self, problem_description: str, problem_domain: str = None) -> SkillRecommendation:
        """
        基于问题推荐技能组合

        Args:
            problem_description: 问题描述
            problem_domain: 问题领域（可选）

        Returns:
            技能推荐
        """
        # 确定问题领域
        if problem_domain is None:
            problem_domain = self._infer_problem_domain(problem_description)

        # 获取候选技能
        candidate_skills = self._get_domain_specific_skills(problem_domain)

        # 如果没有找到特定领域的技能，则回退到推荐的元技能
        used_fallback = False
        if not candidate_skills:
            # 根据问题类型推荐合适的元技能
            candidate_skills = self._get_recommended_meta_skills(problem_domain, problem_description)
            used_fallback = True

        all_candidates = []
        all_candidates.extend(candidate_skills)

        # 添加通用工具技能
        utility_skills = self._get_utility_skills()
        all_candidates.extend(utility_skills)

        # 排序技能（按相关性）- 但如果使用回退的元技能，则不重新排序
        if used_fallback:
            ranked_skills = all_candidates
        else:
            ranked_skills = self._rank_skills_by_relevance(all_candidates, problem_description)

        # 生成执行顺序
        execution_order = [skill.name for skill in ranked_skills]

        # 计算置信度和预估时间
        confidence = self._calculate_confidence(ranked_skills, problem_description)
        estimated_duration = self._estimate_execution_time(ranked_skills)

        return SkillRecommendation(
            skills=ranked_skills[:5],  # 推荐前 5 个
            reasoning=f"基于问题领域 '{problem_domain}' 的技能推荐：{', '.join([s.name for s in ranked_skills[:5]])}",
            confidence=confidence,
            execution_order=execution_order,
            estimated_duration=estimated_duration
        )

    def _infer_problem_domain(self, description: str) -> str:
        """推断问题领域"""
        description_lower = description.lower()

        # 简单关键词匹配
        domain_keywords = {
            "bluetooth": ["bluetooth", "蓝牙", "连接", "设备", "scan"],
            "rssi": ["rssi", "signal", "信号", "图表", "chart", "实时"],
            "performance": ["性能", "优化", "快", "慢", "卡顿", "内存", "fps"],
            "algorithm": ["算法", "排序", "搜索", "tree", "dp", "分治", "动态规划"],
            "network": ["网络", "http", "请求", "api", "接口"],
            "database": ["数据库", "db", "sql", "查询"],
            "ui": ["ui", "界面", "design", "布局", "组件", "widget"],
            "security": ["安全", "认证", "加密", "token"],
            "testing": ["测试", "qa", "质量", "单元测试"],
            "optimization": ["优化", "调优", "微服务", "异步", "缓存"]
        }

        best_domain = None
        best_score = 0

        for domain, keywords in domain_keywords.items():
            score = sum(1.0 for kw in keywords if kw in description_lower)
            if score > best_score:
                best_score = score
                best_domain = domain

        return best_domain if best_domain else "general"

    def _get_domain_specific_skills(self, domain: str) -> List[Skill]:
        """获取领域相关技能"""
        if domain in self.skills_by_domain:
            return self.skills_by_domain[domain]
        else:
            return []

    def _get_utility_skills(self) -> List[Skill]:
        """获取通用工具技能"""
        utility_skills = []
        for skill in self.all_skills.values():
            if skill.category == "utility":
                utility_skills.append(skill)
        return utility_skills

    def _get_recommended_meta_skills(self, domain: str, problem_description: str) -> List[Skill]:
        """
        根据领域和问题描述推荐合适的元技能

        当没有特定领域技能时，返回推荐的元技能组合
        """
        recommended = []

        # 根据问题类型推荐不同的元技能组合
        problem_lower = problem_description.lower()

        # 总是添加问题穷举器作为第一步
        for skill in self.all_skills.values():
            if "问题穷举" in skill.name:
                recommended.append(skill)
                break

        # 如果问题涉及优化、性能、不稳定等
        optimization_keywords = ["优化", "性能", "不稳定", "卡顿", "慢", "快", "改进", "退避", "超时"]
        if any(kw in problem_lower for kw in optimization_keywords):
            # 优化器优先
            for skill in self.all_skills.values():
                if "优化器" in skill.name:
                    recommended.append(skill)
                    break

        # 如果问题涉及生成、创建、实现
        generation_keywords = ["生成", "创建", "实现", "开发", "构建", "需要"]
        if any(kw in problem_lower for kw in generation_keywords):
            # 生成器优先
            for skill in self.all_skills.values():
                if "生成器" in skill.name:
                    recommended.append(skill)
                    break

        # 添加其他推荐的元技能
        meta_skill_order = ["检查器", "扫描器", "修复器"]
        for skill_name in meta_skill_order:
            for skill in self.all_skills.values():
                if skill_name in skill.name and skill not in recommended:
                    recommended.append(skill)
                    break

        return recommended

    def _rank_skills_by_relevance(self, skills: List[Skill], query: str) -> List[Skill]:
        """根据相关性排序技能"""
        scores = []
        for skill in skills:
            score = self._calculate_skill_relevance(skill, query)
            scores.append((score, skill))

        # 按分数降序
        scores.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scores]

    def _calculate_skill_relevance(self, skill: Skill, query: str) -> float:
        """计算技能相关性分数"""
        score = 0.0

        # 1. 领域匹配 (权重 3.0)
        if skill.domain == ProblemDomain.GENERAL:
            # 通用技能权重较低
            score += 0.5

        # 2. 名称关键词匹配 (权重 2.0)
        query_lower = query.lower()
        if any(kw in skill.name.lower() for kw in query_lower.split()):
            score += 2.0

        # 3. 类别匹配 (权重 1.5)
        if skill.category in query_lower:
            score += 1.5

        # 4. 技能能力匹配 (权重 1.0)
        # 解析技能描述中的能力关键词
        for capability in skill.capabilities:
            if capability.lower() in query_lower:
                score += 1.0

        return min(10.0, score)  # 最大分数 10.0

    def _calculate_confidence(self, skills: List[Skill], query: str) -> float:
        """计算推荐置信度"""
        if not skills:
            return 0.5

        # 基于技能数量计算（更多技能 = 更高置信度）
        skill_count_factor = min(len(skills) / 10.0, 1.0)

        # 基于相关性分数计算
        avg_relevance = sum(self._calculate_skill_relevance(s, query) for s in skills) / len(skills)

        return min(1.0, (avg_relevance * 0.6 + skill_count_factor * 0.4))

    def _estimate_execution_time(self, skills: List[Skill]) -> float:
        """预估执行时间（分钟）"""
        # 基础时间：每个技能平均 2 分钟
        base_time = len(skills) * 2.0

        # 元技能权重系数：1.5
        # 应用技能权重系数：1.0
        # 工具技能权重系数：0.5

        # 计算权重
        time_estimate = base_time * (
            sum(1.5 if s.type == SkillType.META_SKILL else 1.0 for s in skills) +
            sum(1.0 if s.category == "utility" else 0.5 for s in skills)
        )

        return time_estimate

    def generate_recommendation_report(self, recommendation: SkillRecommendation, output_path: str = None) -> str:
        """生成推荐报告（Markdown 格式）"""
        report = f"""# 技能推荐报告

## 问题分析
- 问题描述: [问题描述文本]
- 问题领域: [推断的领域]

## 推荐技能

推荐 {len(recommendation.skills)} 个技能：

"""

        for i, skill in enumerate(recommendation.skills):
            report += f"""### {i+1}. {skill.name}
- **类型**: {skill.type.value}
- **类别**: {skill.category}
- **路径**: {skill.path}
- **描述**: {skill.description}
- **能力**: {', '.join(skill.capabilities)}

"""

        report += f"""## 执行顺序

{', '.join(recommendation.execution_order)}

## 推荐理由

{recommendation.reasoning}

## 置信度和预估

- **置信度**: {recommendation.confidence:.2f}
- **预估执行时间**: {recommendation.estimated_duration:.1f} 分钟

## 依赖检查
"""

        # 检查技能依赖
        report += "技能依赖关系分析：\n\n"
        for i, skill in enumerate(recommendation.skills):
            dependencies = self.skill_dependencies.get(skill.name, set())
            if dependencies:
                report += f"- {skill.name} 依赖于：{', '.join(dependencies)}\n"
            else:
                report += f"- {skill.name}: 无直接依赖\n"

        # 检查循环依赖
        report += "\n循环依赖检测：\n"
        has_cycle = self._check_circular_dependencies(recommendation.skills)
        if has_cycle:
            report += "⚠ 警告：检测到循环依赖\n"
        else:
            report += "✓ 无循环依赖\n"

        return report

    def _check_circular_dependencies(self, skills: List[Skill]) -> bool:
        """检查循环依赖"""
        # 构建依赖图
        graph = {}
        for skill in skills:
            deps = self.skill_dependencies.get(skill.name, set())
            graph[skill.name] = deps

        # DFS 检测循环
        visited = set()
        for start in graph.keys():
            if self._dfs_detect_cycle(start, graph, visited):
                return True

        return False

    def _dfs_detect_cycle(self, node: str, graph: Dict[str, Set[str]], visited: Set[str]) -> bool:
        """DFS 检测循环"""
        if node in visited:
            return True

        visited.add(node)
        for neighbor in graph.get(node, []):
            if self._dfs_detect_cycle(neighbor, graph, visited):
                return True

        return False

    def export_recommendations_to_json(self, recommendations: List[SkillRecommendation], output_path: str):
        """导出推荐为 JSON 格式"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "recommendations": [
                {
                    "skills": [
                        {
                            "name": s.name,
                            "type": s.type.value,
                            "category": s.category,
                            "domain": s.domain.value,
                            "path": s.path
                        }
                        for s in rec.skills
                    ],
                    "reasoning": rec.reasoning,
                    "confidence": rec.confidence,
                    "estimated_duration": rec.estimated_duration,
                    "execution_order": rec.execution_order
                }
                for rec in recommendations
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    def optimize_skill_combination(self, skills: List[Skill]) -> List[Skill]:
        """优化技能组合顺序"""
        # 1. 分析技能依赖关系
        # 2. 调整顺序以最小化重试次数
        return skills


# 示例使用
if __name__ == "__main__":
    recommender = SkillRecommender("/Users/administruter/Desktop/skill_factory/.claude/skills")

    print("=" * 60)
    print("技能推荐引擎 - 示例")
    print("=" * 60)

    # 示例 1: 蓝牙连接优化
    print("\n蓝牙连接优化推荐：")
    recommendation1 = recommender.recommend_skills(
        "蓝牙连接不稳定，需要实现指数退避和自适应超时策略"
    )

    print(recommender.generate_recommendation_report(recommendation1))

    # 示例 2: RSSI 图表性能优化
    print("\n\nRSSI 图表性能优化推荐：")
    recommendation2 = recommender.recommend_skills(
        "RSSI 图表卡顿，需要实现自适应更新间隔和数据点裁剪"
    )

    print(recommender.generate_recommendation_report(recommendation2))

    # 示例 3: 导出 JSON
    print("\n\n导出 JSON 格式：")
    recommender.export_recommendations_to_json(
        [recommendation1, recommendation2],
        "/tmp/skill_recommendations.json"
    )
    print("JSON 已导出到: /tmp/skill_recommendations.json")
