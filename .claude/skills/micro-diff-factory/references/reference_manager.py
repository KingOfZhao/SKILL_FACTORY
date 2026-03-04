"""
参考案例管理器

管理微积参考案例的索引、查询、评分等功能

功能：
1. 案例索引和扫描
2. 案例查询和搜索
3. 案例质量评分
4. 案例验证和标记
5. 案例模板生成
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
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


class CaseDifficulty(Enum):
    """案例难度"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class CaseMetadata:
    """案例元数据"""
    file_path: str
    case_type: CaseType
    title: str
    difficulty: CaseDifficulty
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    is_verified: bool = False
    quality_score: float = 0.0
    word_count: int = 0
    code_blocks_count: int = 0
    sections: List[str] = field(default_factory=list)


@dataclass
class QualityScoreBreakdown:
    """质量评分细分"""
    structure_score: float      # 结构完整性 (0-1)
    content_score: float       # 内容质量 (0-1)
    code_score: float          # 代码质量 (0-1)
    documentation_score: float # 文档质量 (0-1)
    completeness_score: float  # 完整性 (0-1)
    overall_score: float       # 总体评分 (0-1)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "structure_score": self.structure_score,
            "content_score": self.content_score,
            "code_score": self.code_score,
            "documentation_score": self.documentation_score,
            "completeness_score": self.completeness_score,
            "overall_score": self.overall_score
        }


class ReferenceManager:
    """参考案例管理器"""

    # 必需的章节
    REQUIRED_SECTIONS = [
        "问题描述",
        "变量分析",
        "微分拆解方案",
        "求解策略",
        "约束条件",
        "优化建议"
    ]

    # 可选的加分章节
    BONUS_SECTIONS = [
        "代码集成示例",
        "预期效果",
        "总结",
        "下一步"
    ]

    def __init__(self, base_path: str):
        """
        初始化参考管理器

        Args:
            base_path: 参考案例库的根路径
        """
        self.base_path = Path(base_path)
        self.cases: Dict[str, CaseMetadata] = {}
        self.index_file = self.base_path / "case_index.json"

        # 加载现有索引
        self._load_index()

    def _load_index(self):
        """加载案例索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)

                for file_path, case_data in index_data.items():
                    case = CaseMetadata(
                        file_path=file_path,
                        case_type=CaseType(case_data["case_type"]),
                        title=case_data["title"],
                        difficulty=CaseDifficulty(case_data["difficulty"]),
                        tags=case_data["tags"],
                        created_at=datetime.fromisoformat(case_data["created_at"]),
                        updated_at=datetime.fromisoformat(case_data["updated_at"]),
                        is_verified=case_data.get("is_verified", False),
                        quality_score=case_data.get("quality_score", 0.0),
                        word_count=case_data.get("word_count", 0),
                        code_blocks_count=case_data.get("code_blocks_count", 0),
                        sections=case_data.get("sections", [])
                    )
                    self.cases[file_path] = case

    def _save_index(self):
        """保存案例索引"""
        index_data = {}
        for file_path, case in self.cases.items():
            index_data[file_path] = {
                "case_type": case.case_type.value,
                "title": case.title,
                "difficulty": case.difficulty.value,
                "tags": case.tags,
                "created_at": case.created_at.isoformat(),
                "updated_at": case.updated_at.isoformat(),
                "is_verified": case.is_verified,
                "quality_score": case.quality_score,
                "word_count": case.word_count,
                "code_blocks_count": case.code_blocks_count,
                "sections": case.sections
            }

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

    def scan_directory(self, force_rescan: bool = False) -> int:
        """
        扫描参考案例目录，更新索引

        Args:
            force_rescan: 是否强制重新扫描所有文件

        Returns:
            新发现的案例数量
        """
        new_cases = 0

        # 遍历所有 .md 文件
        for md_file in self.base_path.rglob("*.md"):
            if md_file.name == "case_index.json":
                continue

            file_path = str(md_file)

            # 如果索引中已存在且不强制重新扫描，跳过
            if not force_rescan and file_path in self.cases:
                # 检查文件是否被修改
                if md_file.stat().st_mtime <= self.cases[file_path].updated_at.timestamp():
                    continue

            # 解析案例
            case = self._parse_case(md_file)
            if case:
                self.cases[file_path] = case
                new_cases += 1

        # 保存索引
        self._save_index()

        return new_cases

    def _parse_case(self, file_path: Path) -> Optional[CaseMetadata]:
        """
        解析案例文件

        Args:
            file_path: 案例文件路径

        Returns:
            案例元数据，解析失败返回 None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取标题
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else file_path.stem

            # 提取类型（从文件路径或内容）
            case_type = self._extract_case_type(content, str(file_path))

            # 提取难度
            difficulty = self._extract_difficulty(content)

            # 提取标签
            tags = self._extract_tags(content)

            # 提取章节
            sections = self._extract_sections(content)

            # 统计字数
            word_count = len(content.split())

            # 统计代码块数量
            code_blocks_count = len(re.findall(r'```[\s\S]*?```', content))

            # 计算质量评分
            quality_score = self._calculate_quality_score(
                content,
                sections,
                word_count,
                code_blocks_count
            )

            return CaseMetadata(
                file_path=str(file_path),
                case_type=case_type,
                title=title,
                difficulty=difficulty,
                tags=tags,
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                updated_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                quality_score=quality_score,
                word_count=word_count,
                code_blocks_count=code_blocks_count,
                sections=sections
            )

        except Exception as e:
            print(f"解析案例失败 {file_path}: {e}")
            return None

    def _extract_case_type(self, content: str, file_path: str) -> CaseType:
        """提取案例类型"""
        # 从文件路径提取
        for case_type in CaseType:
            if case_type.value in file_path.lower():
                return case_type

        # 从内容关键词提取
        content_lower = content.lower()

        if any(kw in content_lower for kw in ["bluetooth", "蓝牙", "connect"]):
            return CaseType.BLUETOOTH
        elif any(kw in content_lower for kw in ["rssi", "chart", "图表"]):
            return CaseType.RSSI_CHART
        elif any(kw in content_lower for kw in ["performance", "性能", "optimization"]):
            return CaseType.PERFORMANCE
        elif any(kw in content_lower for kw in ["algorithm", "算法", "dp", "动态规划"]):
            return CaseType.ALGORITHM
        elif any(kw in content_lower for kw in ["probability", "概率", "随机"]):
            return CaseType.PROBABILITY
        elif any(kw in content_lower for kw in ["physics", "物理", "力学"]):
            return CaseType.PHYSICS
        elif any(kw in content_lower for kw in ["logic", "逻辑", "math"]):
            return CaseType.LOGIC_MATH
        else:
            return CaseType.OPTIMIZATION

    def _extract_difficulty(self, content: str) -> CaseDifficulty:
        """提取案例难度"""
        content_lower = content.lower()

        if "expert" in content_lower or "专家" in content or "高级" in content:
            return CaseDifficulty.EXPERT
        elif "advanced" in content_lower or "进阶" in content_lower:
            return CaseDifficulty.ADVANCED
        elif "intermediate" in content_lower or "中级" in content_lower:
            return CaseDifficulty.INTERMEDIATE
        else:
            return CaseDifficulty.BEGINNER

    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        # 从关键词部分提取
        tags = []

        # 查找关键词部分
        keywords_match = re.search(r'关键词[:：]\s*(.+)', content)
        if keywords_match:
            keywords_text = keywords_match.group(1)
            tags.extend([kw.strip() for kw in keywords_text.split(',')])
        else:
            # 从内容中提取常见技术关键词
            common_keywords = [
                "bluetooth", "rssi", "chart", "performance", "optimization",
                "cache", "memory", "render", "scroll", "lazy", "virtual",
                "animation", "state", "provider", "riverpod", "bloc",
                "connectivity", "reconnection", "timeout", "adaptive",
                "gradient", "descent", "simulated", "annealing", "particle",
                "swarm", "constraint", "variable", "relationship"
            ]
            content_lower = content.lower()
            tags = [kw for kw in common_keywords if kw in content_lower]

        return tags

    def _extract_sections(self, content: str) -> List[str]:
        """提取章节标题"""
        sections = []

        # 匹配 Markdown 二级标题
        section_matches = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        sections.extend(section_matches)

        # 匹配 Markdown 三级标题
        sub_section_matches = re.findall(r'^###\s+(.+)$', content, re.MULTILINE)
        sections.extend(sub_section_matches)

        return sections

    def _calculate_quality_score(self,
                                 content: str,
                                 sections: List[str],
                                 word_count: int,
                                 code_blocks_count: int) -> float:
        """
        计算案例质量评分

        Args:
            content: 案例内容
            sections: 章节列表
            word_count: 字数
            code_blocks_count: 代码块数量

        Returns:
            质量评分 (0-1)
        """
        # 1. 结构完整性评分
        structure_score = self._calculate_structure_score(sections)

        # 2. 内容质量评分
        content_score = self._calculate_content_score(content, word_count)

        # 3. 代码质量评分
        code_score = self._calculate_code_score(content, code_blocks_count)

        # 4. 文档质量评分
        documentation_score = self._calculate_documentation_score(content)

        # 5. 完整性评分
        completeness_score = self._calculate_completeness_score(
            content, sections, code_blocks_count
        )

        # 计算加权总分
        weights = {
            "structure": 0.2,
            "content": 0.25,
            "code": 0.25,
            "documentation": 0.15,
            "completeness": 0.15
        }

        overall_score = (
            structure_score * weights["structure"] +
            content_score * weights["content"] +
            code_score * weights["code"] +
            documentation_score * weights["documentation"] +
            completeness_score * weights["completeness"]
        )

        return round(overall_score, 2)

    def _calculate_structure_score(self, sections: List[str]) -> float:
        """计算结构完整性评分"""
        # 检查必需章节是否存在
        present_sections = 0
        for required_section in self.REQUIRED_SECTIONS:
            if any(required_section in section for section in sections):
                present_sections += 1

        # 检查加分章节
        bonus_sections = 0
        for bonus_section in self.BONUS_SECTIONS:
            if any(bonus_section in section for section in sections):
                bonus_sections += 1

        # 计算评分
        base_score = present_sections / len(self.REQUIRED_SECTIONS)
        bonus_score = bonus_sections / len(self.BONUS_SECTIONS) * 0.2

        return min(1.0, base_score + bonus_score)

    def _calculate_content_score(self, content: str, word_count: int) -> float:
        """计算内容质量评分"""
        # 字数评分（理想范围：500-2000 字）
        if word_count < 200:
            return 0.3
        elif word_count < 500:
            return 0.6
        elif word_count < 2000:
            return 1.0
        elif word_count < 5000:
            return 0.8
        else:
            return 0.6  # 太长也可能冗余

    def _calculate_code_score(self, content: str, code_blocks_count: int) -> float:
        """计算代码质量评分"""
        # 代码块数量评分（理想范围：3-10 个）
        if code_blocks_count == 0:
            return 0.2  # 没有代码示例
        elif code_blocks_count < 3:
            return 0.6
        elif code_blocks_count <= 10:
            return 1.0
        else:
            return 0.8  # 代码过多

    def _calculate_documentation_score(self, content: str) -> float:
        """计算文档质量评分"""
        score = 0.0

        # 检查是否有公式
        if re.search(r'```[a-z]*\n.*=\s*\n.*\n```', content, re.MULTILINE):
            score += 0.2

        # 检查是否有图表说明
        if any(kw in content.lower() for kw in ["图", "图表", "可视化"]):
            score += 0.2

        # 检查是否有预期效果部分
        if "预期效果" in content or "expected" in content.lower():
            score += 0.2

        # 检查是否有总结部分
        if "总结" in content or "总结" in content:
            score += 0.2

        # 检查是否有代码注释
        if re.search(r'//.*|/\*[\s\S]*?\*/', content):
            score += 0.2

        return min(1.0, score)

    def _calculate_completeness_score(self,
                                     content: str,
                                     sections: List[str],
                                     code_blocks_count: int) -> float:
        """计算完整性评分"""
        score = 0.0

        # 检查问题描述的完整性
        if "问题描述" in content and len(re.search(r'问题描述[\s\S]+?(?=##|$)', content).group(0)) > 100:
            score += 0.3

        # 检查变量的定义
        if "变量定义" in content or "变量分析" in content:
            variable_section = re.search(r'变量(?:定义|分析)[\s\S]+?(?=##|$)', content)
            if variable_section and len(variable_section.group(0)) > 50:
                score += 0.2

        # 检查约束条件
        if "约束条件" in content:
            score += 0.2

        # 检查求解策略
        if "求解策略" in content or "优化建议" in content:
            score += 0.3

        return min(1.0, score)

    def get_quality_breakdown(self, file_path: str) -> Optional[QualityScoreBreakdown]:
        """
        获取案例的质量评分细分

        Args:
            file_path: 案例文件路径

        Returns:
            质量评分细分，案例不存在返回 None
        """
        if file_path not in self.cases:
            return None

        case = self.cases[file_path]

        # 重新计算各项评分
        structure_score = self._calculate_structure_score(case.sections)
        content_score = self._calculate_content_score("", case.word_count)
        code_score = self._calculate_code_score("", case.code_blocks_count)
        documentation_score = 0.5  # 需要重新读取内容计算
        completeness_score = self._calculate_completeness_score(
            "", case.sections, case.code_blocks_count
        )

        overall_score = case.quality_score

        return QualityScoreBreakdown(
            structure_score=round(structure_score, 2),
            content_score=round(content_score, 2),
            code_score=round(code_score, 2),
            documentation_score=round(documentation_score, 2),
            completeness_score=round(completeness_score, 2),
            overall_score=round(overall_score, 2)
        )

    def verify_case(self, file_path: str) -> bool:
        """
        标记案例为已验证

        Args:
            file_path: 案例文件路径

        Returns:
            是否成功标记
        """
        if file_path not in self.cases:
            return False

        self.cases[file_path].is_verified = True
        self._save_index()
        return True

    def search_cases(self,
                    case_type: Optional[CaseType] = None,
                    difficulty: Optional[CaseDifficulty] = None,
                    tags: Optional[List[str]] = None,
                    min_quality: float = 0.0) -> List[CaseMetadata]:
        """
        搜索案例

        Args:
            case_type: 案例类型
            difficulty: 案例难度
            tags: 标签列表
            min_quality: 最低质量评分

        Returns:
            匹配的案例列表
        """
        results = []

        for case in self.cases.values():
            # 类型过滤
            if case_type and case.case_type != case_type:
                continue

            # 难度过滤
            if difficulty and case.difficulty != difficulty:
                continue

            # 标签过滤
            if tags:
                if not any(tag in case.tags for tag in tags):
                    continue

            # 质量过滤
            if case.quality_score < min_quality:
                continue

            results.append(case)

        # 按质量评分排序
        results.sort(key=lambda c: c.quality_score, reverse=True)

        return results

    def get_trending_cases(self, limit: int = 10) -> List[CaseMetadata]:
        """
        获取热门案例（最近更新的高质量案例）

        Args:
            limit: 返回数量限制

        Returns:
            热门案例列表
        """
        # 按更新时间和质量评分排序
        sorted_cases = sorted(
            self.cases.values(),
            key=lambda c: (c.updated_at, c.quality_score),
            reverse=True
        )

        return sorted_cases[:limit]

    def create_case_template(self, case_type: CaseType, title: str) -> str:
        """
        生成案例模板

        Args:
            case_type: 案例类型
            title: 案例标题

        Returns:
            Markdown 格式的案例模板
        """
        template = f"""---
# {title}

## 问题描述
[详细描述要解决的问题，包括现状、痛点等]

## 变量分析

### 相关变量
- `variable_1` (Type): 变量描述
- `variable_2` (Type): 变量描述

### 优化目标
- 目标1描述
- 目标2描述

## 微分拆解方案

### 变量定义
[定义关键变量及其取值范围]

### 微分分析
[对变量进行微分分析]

## 求解策略

### 策略一：[策略名称]
[详细描述第一种求解策略]

#### 代码示例
```dart
// 示例代码
```

### 策略二：[策略名称]
[详细描述第二种求解策略]

## 约束条件

### 1. 硬约束
- 约束1
- 约束2

### 2. 潜约束
- 约束1
- 约束2

## 优化建议

### 短期优化（1-2 周）
1. 优化点1
2. 优化点2

### 中期优化（3-4 周）
1. 优化点1
2. 优化点2

### 长期优化（3-6 月）
1. 优化点1
2. 优化点2

## 预期效果

### 量化指标
- 指标1: 从 X → 目标 Y
- 指标2: 从 X → 目标 Y

### 用户体验提升
- 提升点1描述
- 提升点2描述

## 总结

### 核心创新
1. 创新点1
2. 创新点2

### 可扩展性
[描述可扩展的方向]

---

**案例类型**: `{case_type.value}`
**难度**: `[待评估]`
**关键词**: [关键词1, 关键词2, 关键词3]

---

**维护者**: Claude Code Skill Factory Team
**版本**: 1.0.0
"""
        return template


# 示例使用
if __name__ == "__main__":
    manager = ReferenceManager(
        base_path="/Users/administruter/Desktop/skill_factory/.claude/skills/micro-diff-factory/references/micro-diff-cases"
    )

    # 扫描目录
    print("扫描参考案例目录...")
    new_cases = manager.scan_directory()
    print(f"发现 {new_cases} 个新案例")

    # 显示所有案例
    print("\n所有案例:")
    for file_path, case in manager.cases.items():
        print(f"  {case.title} ({case.case_type.value})")
        print(f"    难度: {case.difficulty.value}, 质量评分: {case.quality_score:.2f}")
        print(f"    标签: {', '.join(case.tags)}")

    # 搜索案例
    print("\n搜索性能相关案例:")
    performance_cases = manager.search_cases(
        case_type=CaseType.PERFORMANCE,
        min_quality=0.5
    )
    for case in performance_cases:
        print(f"  {case.title} - 评分: {case.quality_score:.2f}")

    # 获取热门案例
    print("\n热门案例:")
    trending = manager.get_trending_cases(5)
    for case in trending:
        print(f"  {case.title} - 更新: {case.updated_at.strftime('%Y-%m-%d')}, 评分: {case.quality_score:.2f}")

    # 查看质量评分细分
    if manager.cases:
        first_case = next(iter(manager.cases.values()))
        print(f"\n{first_case.title} 的质量评分细分:")
        breakdown = manager.get_quality_breakdown(first_case.file_path)
        if breakdown:
            for key, value in breakdown.to_dict().items():
                print(f"  {key}: {value:.2f}")
