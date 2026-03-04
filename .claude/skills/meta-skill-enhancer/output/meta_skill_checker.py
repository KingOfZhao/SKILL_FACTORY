"""
检查器验证工具

负责验证生成的 Skills 是否符合元 Skill 体系的约定、
最佳实践应用和模式使用情况。
"""

import json
import os
import re
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationRule:
    """验证规则"""
    rule_id: str
    name: str
    category: str  # structure, best-practices, patterns, documentation, consistency
    description: str
    severity: str  # critical, major, minor, warning
    check_function: str
    auto_fixable: bool = False


@dataclass
class ValidationResult:
    """验证结果"""
    rule_id: str
    rule_name: str
    passed: bool
    severity: str
    message: str
    location: Optional[str] = None  # 文件路径、行号等
    suggested_fix: Optional[str] = None


@dataclass
class SkillValidationReport:
    """技能验证报告"""
    skill_name: str
    skill_path: str
    validation_time: str
    total_rules: int
    passed_rules: int
    failed_rules: int
    critical_issues: int
    major_issues: int
    minor_issues: int
    warnings: int
    results: List[ValidationResult]
    best_practices_compliance: float  # 0.0-1.0
    pattern_usage_score: float  # 0.0-1.0
    overall_score: float  # 0.0-1.0
    recommendations: List[str]


class MetaSkillChecker:
    """元 Skill 检查器"""

    def __init__(self, config: Dict):
        self.config = config
        self.rules: List[ValidationRule] = []
        self.underlying_convention_path = config.get('underlying_convention_path', '')
        self.pattern_registry_path = config.get('pattern_registry_path', '')
        self.domain_knowledge_path = config.get('domain_knowledge_path', '')

        self._load_validation_rules()

    def validate_skill(self, skill_path: str, skill_content: Optional[str] = None) -> SkillValidationReport:
        """
        验证单个 Skill

        Args:
            skill_path: Skill 文件路径
            skill_content: Skill 文件内容（可选，未提供则读取）

        Returns:
            SkillValidationReport 验证报告
        """
        skill_name = Path(skill_path).stem
        print(f"[检查器] 开始验证 Skill: {skill_name}")

        # 读取内容
        if skill_content is None:
            with open(skill_path, 'r', encoding='utf-8') as f:
                skill_content = f.read()

        results = []
        start_time = datetime.now()

        # 执行所有验证规则
        for rule in self.rules:
            try:
                if rule.category == 'structure':
                    results.extend(self._validate_structure(rule, skill_content, skill_path))
                elif rule.category == 'best-practices':
                    results.extend(self._validate_best_practices(rule, skill_content, skill_path))
                elif rule.category == 'patterns':
                    results.extend(self._validate_patterns(rule, skill_content, skill_path))
                elif rule.category == 'documentation':
                    results.extend(self._validate_documentation(rule, skill_content, skill_path))
                elif rule.category == 'consistency':
                    results.extend(self._validate_consistency(rule, skill_content, skill_path))
            except Exception as e:
                results.append(ValidationResult(
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    passed=False,
                    severity='major',
                    message=f"验证失败: {e}",
                    location=skill_path,
                    suggested_fix="检查 Skill 实现是否完整"
                ))

        duration = (datetime.now() - start_time).total_seconds()

        # 统计结果
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed

        critical = sum(1 for r in results if r.severity == 'critical')
        major_issues = sum(1 for r in results if r.severity == 'major')
        minor_issues = sum(1 for r in results if r.severity == 'minor')
        warnings = sum(1 for r in results if r.severity == 'warning')

        # 计算合规性分数
        best_practices_compliance = self._calculate_best_practices_score(results)
        pattern_usage_score = self._calculate_pattern_score(results)
        overall_score = (best_practices_compliance * 0.4 +
                       pattern_usage_score * 0.3 +
                       (passed / total) * 0.3)

        # 生成推荐
        recommendations = self._generate_recommendations(results, skill_name)

        report = SkillValidationReport(
            skill_name=skill_name,
            skill_path=skill_path,
            validation_time=datetime.now().isoformat(),
            total_rules=total,
            passed_rules=passed,
            failed_rules=failed,
            critical_issues=critical,
            major_issues=major_issues,
            minor_issues=minor_issues,
            warnings=warnings,
            results=results,
            best_practices_compliance=best_practices_compliance,
            pattern_usage_score=pattern_usage_score,
            overall_score=overall_score,
            recommendations=recommendations
        )

        print(f"[检查器] 验证完成: {skill_name}")
        print(f"  - 通过: {passed}/{total}")
        print(f"  - 整体评分: {overall_score:.2f}")
        print(f"  - 最佳实践合规: {best_practices_compliance:.2f}")
        print(f"  - 模式使用: {pattern_usage_score:.2f}")

        return report

    def validate_multiple_skills(self, skills_dir: str) -> List[SkillValidationReport]:
        """验证多个 Skills"""
        reports = []

        # 查找所有 SKILL.md 文件
        skill_files = list(Path(skills_dir).rglob('**/SKILL.md'))

        print(f"[检查器] 找到 {len(skill_files)} 个 Skills 待验证")

        for skill_file in skill_files:
            try:
                report = self.validate_skill(str(skill_file))
                reports.append(report)
            except Exception as e:
                print(f"[检查器] 验证失败 {skill_file}: {e}")

        return reports

    def _load_validation_rules(self) -> None:
        """加载验证规则"""
        self.rules = [
            # 结构性规则
            ValidationRule(
                rule_id="struct_001",
                name="SKILL.md 文件格式",
                category="structure",
                description="SKILL.md 文件必须包含必需的章节",
                severity="critical",
                check_function="check_skill_md_structure",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="struct_002",
                name="目录结构存在",
                category="structure",
                description="Skill 必须有对应的目录结构",
                severity="critical",
                check_function="check_directory_structure",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="struct_003",
                name="必需文件存在",
                category="structure",
                description="README.md 和 description.md 必须存在",
                severity="major",
                check_function="check_required_files",
                auto_fixable=True
            ),

            # 最佳实践规则
            ValidationRule(
                rule_id="bp_001",
                name="Clean Architecture",
                category="best-practices",
                description="是否遵循 Clean Architecture 分层",
                severity="major",
                check_function="check_clean_architecture",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="bp_002",
                name="单一职责原则",
                category="best-practices",
                description="每个模块职责单一明确",
                severity="major",
                check_function="check_single_responsibility",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="bp_003",
                name="依赖注入",
                category="best-practices",
                description="使用依赖注入而非硬编码依赖",
                severity="minor",
                check_function="check_dependency_injection",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="bp_004",
                name="错误处理",
                category="best-practices",
                description="有适当的错误处理机制",
                severity="major",
                check_function="check_error_handling",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="bp_005",
                name="测试覆盖",
                category="best-practices",
                description="有测试文件和测试方法",
                severity="major",
                check_function="check_test_coverage",
                auto_fixable=False
            ),

            # 模式规则
            ValidationRule(
                rule_id="pat_001",
                name="MVVM 模式应用",
                category="patterns",
                description="是否使用 MVVM 架构模式",
                severity="minor",
                check_function="check_mvvm_pattern",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="pat_002",
                name="Repository 模式应用",
                category="patterns",
                description="是否使用 Repository 数据访问模式",
                severity="minor",
                check_function="check_repository_pattern",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="pat_003",
                name="Observer 模式应用",
                category="patterns",
                description="是否使用 Observer 状态监听模式",
                severity="minor",
                check_function="check_observer_pattern",
                auto_fixable=False
            ),

            # 文档规则
            ValidationRule(
                rule_id="doc_001",
                name="README 完整性",
                category="documentation",
                description="README 必须包含使用说明",
                severity="major",
                check_function="check_readme_completeness",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="doc_002",
                name="描述文档存在",
                category="documentation",
                description="description.md 必须存在且完整",
                severity="major",
                check_function="check_description_doc",
                auto_fixable=False
            ),

            # 一致性规则
            ValidationRule(
                rule_id="cons_001",
                name="命名约定一致性",
                category="consistency",
                description="文件命名遵循约定（kebab-case）",
                severity="warning",
                check_function="check_naming_convention",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="cons_002",
                name="导入顺序一致性",
                category="consistency",
                description="import 语句遵循 Dart 规范",
                severity="minor",
                check_function="check_import_order",
                auto_fixable=False
            ),
            ValidationRule(
                rule_id="cons_003",
                name="代码风格一致性",
                category="consistency",
                description="代码风格遵循约定（const、final）",
                severity="minor",
                check_function="check_code_style_consistency",
                auto_fixable=False
            )
        ]

        print(f"[检查器] 已加载 {len(self.rules)} 个验证规则")

    def _validate_structure(self, rule: ValidationRule, content: str, path: str) -> List[ValidationResult]:
        """验证结构"""
        results = []

        # 规则 1: SKILL.md 格式
        if not re.search(r'---\s*name:', content):
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="SKILL.md 文件缺少必需的 name 头部",
                location=path,
                suggested_fix="添加：\n---\nname: [Skill名称]"
            ))

        # 规则 2: 必需章节
        required_sections = ['## Capabilities', '## Input Specification', '## Output Specification']
        for section in required_sections:
            if section not in content:
                results.append(ValidationResult(
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    passed=False,
                    severity=rule.severity,
                    message=f"缺少必需章节: {section}",
                    location=path,
                    suggested_fix=f"添加 {section} 章节"
                ))

        return results

    def _validate_best_practices(self, rule: ValidationRule, content: str, path: str) -> List[ValidationResult]:
        """验证最佳实践"""
        results = []

        # 检查 Clean Architecture
        clean_arch_patterns = ['domain/entities', 'data/models', 'data/repositories', 'presentation/pages']
        has_clean_arch = any(pattern in content.lower() for pattern in clean_arch_patterns)

        if not has_clean_arch:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未检测到 Clean Architecture 分层结构",
                location=path,
                suggested_fix="创建 domain/data/presentation 目录结构"
            ))

        # 检查单一职责
        large_file_indicator = re.search(r'class.*\{.*\{.*\{.*\{', content)
        if large_file_indicator:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="检测到可能违反单一职责的复杂类（嵌套过深）",
                location=path,
                suggested_fix="考虑拆分复杂类"
            ))

        # 检查错误处理
        has_error_handling = any(keyword in content.lower() for keyword in
                               ['try', 'catch', 'except', 'error:', 'onerror:', 'errorbound', 'fallback'])

        if not has_error_handling:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未检测到错误处理机制",
                location=path,
                suggested_fix="添加 try-catch 或 ErrorBoundary"
            ))

        # 检查测试
        has_test = 'test' in content.lower() or 'mock' in content.lower()

        if not has_test:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未检测到测试代码或 mock",
                location=path,
                suggested_fix="添加测试文件或 mock"
            ))

        return results

    def _validate_patterns(self, rule: ValidationRule, content: str, path: str) -> List[ValidationResult]:
        """验证模式应用"""
        results = []

        # 检查 MVVM 模式
        mvvm_indicators = ['ViewModel', 'Model', 'Repository']
        has_mvvm = any(indicator in content for indicator in mvvm_indicators)

        if not has_mvvm:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未使用 MVVM 模式",
                location=path,
                suggested_fix="考虑使用 Model-View-ViewModel 分层"
            ))

        # 检查 Repository 模式
        has_repository = 'Repository' in content or 'repository' in content.lower()

        if not has_repository:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未使用 Repository 模式",
                location=path,
                suggested_fix="创建 Repository 类统一数据访问"
            ))

        # 检查 Observer 模式
        has_observer = 'Observer' in content or 'observable' in content or 'notify' in content

        if not has_observer:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="未使用状态监听模式",
                location=path,
                suggested_fix="考虑使用 Observer 或 Provider 监听"
            ))

        return results

    def _validate_documentation(self, rule: ValidationRule, content: str, path: str) -> List[ValidationResult]:
        """验证文档"""
        results = []

        # 检查 README（这是在验证之前单独检查）
        skill_dir = os.path.dirname(path)
        readme_path = os.path.join(skill_dir, 'README.md')

        if not os.path.exists(readme_path):
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="缺少 README.md 文件",
                location=skill_dir,
                suggested_fix="创建 README.md"
            ))

        # 检查描述文档
        description_path = os.path.join(skill_dir, 'description.md')
        if not os.path.exists(description_path):
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="缺少 description.md 文件",
                location=skill_dir,
                suggested_fix="创建 description.md"
            ))

        return results

    def _validate_consistency(self, rule: ValidationRule, content: str, path: str) -> List[ValidationResult]:
        """验证一致性"""
        results = []

        # 检查命名约定
        camel_case_files = re.findall(r'([A-Z][a-z0-9]+)\.dart', content)
        if len(camel_case_files) > 0:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message=f"发现 {len(camel_case_files)} 个文件使用 PascalCase 命名",
                location=path,
                suggested_fix="使用 kebab-case: filename.dart"
            ))

        # 检查导入顺序
        imports = re.findall(r'^import [\'"]([^\'"]+)[\'"]', content, re.MULTILINE)
        dart_imports = [imp for imp in imports if not imp.startswith('package:')]
        package_imports = [imp for imp in imports if imp.startswith('package:')]

        # Dart 内置应该在前
        has_wrong_order = False
        last_was_package = False
        for imp in imports:
            is_package = imp.startswith('package:')
            if is_package and not last_was_package:
                # Package import 之后还有 Dart 内置，顺序错误
                if any(not p.startswith('package:') for p in package_imports):
                    has_wrong_order = True
                    break
            last_was_package = is_package

        if has_wrong_order:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="import 顺序不符合 Dart 规范",
                location=path,
                suggested_fix="重新排序 import：Dart 内置 → package 导入"
            ))

        # 检查代码风格
        has_final_widgets = 'final Widget' in content or 'const Widget' in content
        if not has_final_widgets:
            results.append(ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                passed=False,
                severity=rule.severity,
                message="Widget 组件应使用 final 或 const 构造函数",
                location=path,
                suggested_fix="使用 final Widget myWidget = ..."
            ))

        return results

    def _check_directory_structure(self, path: str) -> bool:
        """检查目录结构"""
        skill_dir = os.path.dirname(path)

        # 检查是否有 lib/ 目录
        lib_path = os.path.join(skill_dir, 'lib')
        return os.path.exists(lib_path)

    def _check_required_files(self, path: str) -> bool:
        """检查必需文件"""
        skill_dir = os.path.dirname(path)

        readme = os.path.exists(os.path.join(skill_dir, 'README.md'))
        description = os.path.exists(os.path.join(skill_dir, 'description.md'))

        return readme and description

    def _calculate_best_practices_score(self, results: List[ValidationResult]) -> float:
        """计算最佳实践合规分数"""
        if not results:
            return 1.0

        # 统计最佳实践规则的结果
        bp_rules = [r for r in results if r.rule_id.startswith('bp_')]
        if not bp_rules:
            return 1.0

        passed = sum(1 for r in bp_rules if r.passed)
        total = len(bp_rules)

        # 根据严重程度加权
        weight_sum = 0
        score_sum = 0

        for r in bp_rules:
            if r.severity == 'critical':
                weight = 3
            elif r.severity == 'major':
                weight = 2
            elif r.severity == 'minor':
                weight = 1
            else:
                weight = 0.5

            weight_sum += weight
            if r.passed:
                score_sum += weight

        return score_sum / weight_sum if weight_sum > 0 else 1.0

    def _calculate_pattern_score(self, results: List[ValidationResult]) -> float:
        """计算模式使用分数"""
        if not results:
            return 1.0

        # 统计模式规则的结果
        pattern_rules = [r for r in results if r.rule_id.startswith('pat_')]
        if not pattern_rules:
            return 1.0

        passed = sum(1 for r in pattern_rules if r.passed)
        total = len(pattern_rules)

        return passed / total if total > 0 else 1.0

    def _generate_recommendations(self, results: List[ValidationResult], skill_name: str) -> List[str]:
        """生成推荐"""
        recommendations = []

        # 根据失败规则生成推荐
        failed_results = [r for r in results if not r.passed]

        # 去重推荐
        seen_recs = set()

        for result in failed_results:
            if result.suggested_fix and result.suggested_fix not in seen_recs:
                seen_recs.add(result.suggested_fix)
                recommendations.append(result.suggested_fix)

        # 添加通用推荐
        if not recommendations:
            recommendations.append("Skill 验证通过，继续保持")
        else:
            recommendations.insert(0, "修复上述问题以提高 Skill 质量")

        return recommendations

    def generate_validation_summary(self, reports: List[SkillValidationReport]) -> str:
        """生成验证摘要"""
        lines = [
            "# 元 Skill 验证摘要",
            "",
            f"验证时间: {datetime.now().isoformat()}",
            f"验证 Skill 数: {len(reports)}",
            "",
            "## 总体统计",
            ""
        ]

        total_critical = sum(r.critical_issues for r in reports)
        total_major = sum(r.major_issues for r in reports)
        total_minor = sum(r.minor_issues for r in reports)
        total_warnings = sum(r.warnings for r in reports)

        avg_score = sum(r.overall_score for r in reports) / len(reports) if reports else 0

        lines.extend([
            f"- 总验证规则执行: {sum(r.total_rules for r in reports)}",
            f"- 通过规则: {sum(r.passed_rules for r in reports)}",
            f"- 失败规则: {sum(r.failed_rules for r in reports)}",
            f"",
            f"- 严重问题: {total_critical}",
            f"- 主要问题: {total_major}",
            f"- 次要问题: {total_minor}",
            f"- 警告: {total_warnings}",
            f"- 平均合规分数: {avg_score:.2f}",
            ""
            "## 需要修复的 Skills（按分数排序）",
            ""
        ])

        # 按分数排序（最低分在前）
        sorted_reports = sorted(reports, key=lambda r: r.overall_score)

        for report in sorted_reports[:10]:  # 显示前 10 个
            lines.extend([
                f"### {report.skill_name} (分数: {report.overall_score:.2f})",
                f"",
                f"- 路径: {report.skill_path}",
                f"- 最佳实践合规: {report.best_practices_compliance:.2f}",
                f"- 模式使用: {report.pattern_usage_score:.2f}",
                f"",
                "**问题**: {len([r for r in report.results if not r.passed])}",
                ""
            ])

            if report.recommendations:
                lines.append("**推荐**:")
                for rec in report.recommendations[:5]:
                    lines.append(f"- {rec}")

        return "\n".join(lines)
