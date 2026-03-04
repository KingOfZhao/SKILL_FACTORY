"""
参考文件夹管理系统

负责管理和维护参考案例文件夹，
支持自动扫描、索引和查询。
"""

import json
import os
import re
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


class CaseType(Enum):
    """案例类型"""
    BLUETOOTH = "bluetooth"
    RSSI_CHART = "rssi_chart"
    STATE_MANAGEMENT = "state_management"
    PERFORMANCE = "performance"
    ALGORITHM = "algorithm"
    PROBABILITY = "probability"
    OPTIMIZATION = "optimization"
    LOGIC_MATH = "logic_math"
    PHYSICS = "physics"


class CaseMetadata:
    """案例元数据"""
    case_id: str
    name: str
    case_type: CaseType
    sub_problem: str
    created_at: str
    updated_at: str
    author: str
    difficulty: str  # beginner, intermediate, advanced, expert
    tags: List[str]
    summary: str
    file_path: str
    has_variables: bool
    has_formulas: bool
    has_constraints: bool
    has_bounds: bool
    has_optimization_goal: bool
    has_solution_strategy: bool
    has_implementation: bool
    has_examples: bool
    references: List[str]
    verified: bool = False


@dataclass
class CaseIndex:
    """案例索引"""
    cases_by_type: Dict[CaseType, List[CaseMetadata]] = {}
    cases_by_tags: Dict[str, List[str]] = {}
    cases_by_difficulty: Dict[str, List[str]] = {}
    total_cases: int = 0
    last_updated: str

    @classmethod
    def load(cls, index_file: str = "cases/micro-diff-index.json") -> None:
        """加载索引"""
        if not os.path.exists(index_file):
            print(f"[参考文件夹] 索引文件不存在: {index_file}")
            return

        with open(index_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cls.total_cases = data.get('total_cases', 0)
            cls.cases_by_type = {CaseType(k): v for k, v in data.get('cases_by_type', {}).items()}
            cls.cases_by_tags = {k: v for k, v in data.get('cases_by_tags', {}).items()}
            cls.last_updated = data.get('last_updated', '')

        print(f"[参考文件夹] 已加载 {cls.total_cases} 个案例索引")

    @classmethod
    def scan_directory(cls, base_dir: str = "references/micro-diff-cases/") -> List[CaseMetadata]:
        """扫描参考案例目录"""
        cases = []
        base_path = Path(base_dir)

        if not base_path.exists():
            return cases

        for case_file in base_path.rglob('**/*.md'):
            try:
                case_path = str(case_file)
                case_id = case_path.replace(str(base_path), '').replace('/', '_')

                # 读取案例文件
                with open(case_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 提取元数据
                case_info = cls._extract_case_info(content, case_id)

                if case_info:
                    cases.append(case_info)

            except Exception as e:
                print(f"[参考文件夹] 处理文件失败 {case_file}: {e}")

        print(f"[参考文件夹] 扫描完成，发现 {len(cases)} 个案例")
        return cases

    @classmethod
    def _extract_case_info(cls, content: str, case_id: str) -> Optional[CaseMetadata]:
        """从案例文件中提取元数据"""
        try:
            # 检查必需章节
            has_description = '# 问题描述' in content
            has_variables = '# 变量分析' in content
            has_constraints = '# 约束条件' in content
            has_optimization = '# 优化目标' in content
            has_strategy = '# 求解策略' in content
            has_formulas = '# 核心公式' in content
            has_solution = '# 微分拆解方案' in content

            if not all([has_description, has_variables, has_constraints, has_optimization]):
                print(f"[参考文件夹] 案例缺少必需章节: {case_id}")
                return None

            # 提取名称
            name_match = re.search(r'^#\s*(.+?)\s*$', content, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else case_id

            # 提取标签
            tags_match = re.findall(r'tags?:\s*([^\n]+)', content)
            tags = [tag.strip() for tag in tags_match]

            # 提取类型和难度
            type_match = re.search(r'类型：(\w+)', content)
            case_type = cls._parse_case_type(type_match.group(1) if type_match else CaseType.OPTIMIZATION)

            diff_match = re.search(r'难度：(\w+)', content)
            difficulty = diff_match.group(1).strip() if diff_match else 'intermediate'

            # 提取创建时间
            created_match = re.search(r'创建日期：([^\n]+)', content)
            created_at = created_match.group(1).strip() if created_match else datetime.now().isoformat()

            # 检查完整性
            has_implementation = '## 实际代码示例' in content or '### 实际代码示例' in content
            has_examples = has_implementation or ('## 实现示例' in content or '### 实现示例' in content)

            # 提取引用
            refs_match = re.findall(r'\[([^\]]+)\]', content)
            references = refs_match

            return CaseMetadata(
                case_id=case_id,
                name=name,
                case_type=case_type,
                sub_problem="",
                created_at=created_at,
                updated_at=created_at,
                author="system",
                difficulty=difficulty,
                tags=tags,
                summary=cls._generate_summary(content),
                file_path=case_path,
                has_variables=True,
                has_formulas=True,
                has_constraints=True,
                has_bounds=has_bounds or has_optimization,
                has_optimization_goal=has_optimization,
                has_solution_strategy=has_strategy,
                has_implementation=has_implementation,
                has_examples=has_examples,
                references=references,
                verified=False
            )

        except Exception as e:
            print(f"[参考文件夹] 提取失败 {case_id}: {e}")
            return None

    @classmethod
    def _parse_case_type(cls, type_str: str) -> CaseType:
        """解析案例类型"""
        type_lower = type_str.lower()

        type_mapping = {
            'bluetooth': CaseType.BLUETOOTH,
            'rssi': CaseType.RSSI_CHART,
            'state': CaseType.STATE_MANAGEMENT,
            'performance': CaseType.PERFORMANCE,
            'algorithm': CaseType.ALGORITHM,
            'probability': CaseType.PROBABILITY,
            'optimization': CaseType.OPTIMIZATION
        }

        for key, case_type in type_mapping.items():
            if key in type_lower:
                return case_type

        return CaseType.OPTIMIZATION

    @classmethod
    def _generate_summary(cls, content: str) -> str:
        """生成摘要"""
        lines = content.split('\n')[:5]  # 取前 5 行作为摘要
        return ' '.join(lines).strip()

    @classmethod
    def save_index(cls, index_file: str = "cases/micro-diff-index.json") -> None:
        """保存索引"""
        index_data = {
            'total_cases': cls.total_cases,
            'cases_by_type': {k.value: [case.__dict__ for case in v]
                               for k, v in cls.cases_by_type.items()},
            'cases_by_tags': cls.cases_by_tags,
            'cases_by_difficulty': cls.cases_by_difficulty,
            'last_updated': cls.last_updated,
            'version': '1.0'
        }

        os.makedirs(os.path.dirname(index_file), exist_ok=True)

        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        print(f"[参考文件夹] 索引已保存到 {index_file}")

    @classmethod
    def search_cases(cls, query: str, case_type: Optional[CaseType] = None,
                    difficulty: Optional[str] = None,
                    tags: Optional[List[str]] = None) -> List[CaseMetadata]:
        """搜索案例"""
        results = cls.cases_by_type.get(CaseType.OPTIMIZATION, []) if case_type else []

        for case_list in cls.cases_by_type.values():
            results.extend(case_list)

        # 过滤
        if difficulty:
            results = [c for c in results if c.difficulty == difficulty]

        if tags:
            query_lower = query.lower()
            results = [c for c in results
                          if any(tag.lower() in query_lower for tag in c.tags)]

        return results

    @classmethod
    def get_trending_cases(cls, limit: int = 10) -> List[CaseMetadata]:
        """获取热门案例（基于更新时间）"""
        all_cases = []

        for case_list in cls.cases_by_type.values():
            all_cases.extend(case_list)

        all_cases.sort(key=lambda c: c.updated_at, reverse=True)

        return all_cases[:limit]

    @classmethod
    def get_cases_by_difficulty(cls, difficulty: str) -> List[CaseMetadata]:
        """按难度获取案例"""
        return cls.cases_by_difficulty.get(difficulty, [])

    @classmethod
    def verify_case(cls, case_id: str) -> bool:
        """验证案例完整性"""
        if case_id not in cls.cases_by_tags:
            return False

        # 找到案例
        for case_list in cls.cases_by_type.values():
            for case in case_list:
                if case.case_id == case_id:
                    case.verified = True
                    return True

        return False


class ReferenceFolderManager:
    """参考文件夹管理器"""

    def __init__(self, base_dir: str = "references/micro-diff-cases"):
        self.base_dir = base_dir
        self.index_file = "cases/micro-diff-index.json"

    def initialize(self) -> None:
        """初始化参考文件夹系统"""
        print("[参考文件夹] 初始化微分参考系统...")

        # 创建基础目录结构
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "cases"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "bluetooth"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "rssi-chart"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "state-management"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "performance"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "algorithm"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "probability"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "optimization"), exist_ok=True)

        # 加载索引
        CaseIndex.load(self.index_file)

        print(f"[参考文件夹] 初始化完成")

    def scan_cases(self) -> None:
        """扫描案例"""
        print(f"[参考文件夹] 扫描案例目录: {self.base_dir}")

        cases = CaseIndex.scan_directory(self.base_dir)
        CaseIndex.save_index(self.index_file)

    def search(self, query: str, **filters) -> List[CaseMetadata]:
        """搜索案例"""
        return CaseIndex.search_cases(
            query=query,
            case_type=filters.get('case_type'),
            difficulty=filters.get('difficulty'),
            tags=filters.get('tags')
        )

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            'total_cases': self.total_cases,
            'cases_by_type': {k.value: len(v) for k, v in self.cases_by_type.items()},
            'cases_by_difficulty': self.cases_by_difficulty,
            'trending_cases': len(CaseIndex.get_trending_cases(limit=10))
        }

    def create_case_template(self, case_type: CaseType, title: str) -> str:
        """创建案例模板"""
        template = f"""---
# {title}

## 问题描述
简要描述要解决的具体问题。

## 变量分析
### 关键变量
列出所有识别的变量。

### 变量关系
描述变量之间的关系（正相关、负相关、独立等）。

## 约束条件
### 显式约束
必须满足的硬性约束。

### 隐式约束
隐含的约束或实际限制。

## 优化目标
明确要优化的目标函数（最大化或最小化）。

## 求解策略
选择的求解策略和方法。

## 微分拆解方案
### 核心公式
主要微分方程或公式。

## 边界分析
变量取值范围的分析。

## 敏感性分析
分析解对变量微小变化的敏感度。

## 优化建议
基于拆解结果的优化建议。

## 实现示例
### 伪代码
展示核心实现的伪代码。

### 实际代码示例
Flutter/Dart 实现示例。

## 参考资源
相关文档、论文、库的链接。

---

**案例类型**: {case_type.value}

**标签**:
# 微分拆解
# 优化
# 变量
# 约束
# {case_type.value}
---

*请基于上述模板填充内容。*
"""

        return template

    def verify_all_cases(self) -> Dict[str, List[str]]:
        """验证所有案例"""
        issues = []

        for case_list in self.cases_by_type.values():
            for case in case_list:
                if not case.has_formulas or not case.has_constraints:
                    issues.append(f"案例 {case.case_id}: 缺少必需章节")

        return {
            'total_cases': self.total_cases,
            'verified_cases': len([c for c_list in self.cases_by_type.values() for c in c_list if c.verified]),
            'issues': issues
        }
