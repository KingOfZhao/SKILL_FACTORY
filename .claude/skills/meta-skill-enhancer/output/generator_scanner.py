"""
生成器扫描工具

负责扫描第三方库/框架的 GitHub 仓库、文档和社区讨论，
提取最佳实践、常见问题和解决方案，为 Skill 生成提供参考。
"""

import json
import re
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class IssueAnalysis:
    """Issue 分析结果"""
    issue_number: int
    title: str
    url: str
    state: str
    created_at: str
    comments_count: int
    reactions: Dict[str, int]
    labels: List[str]
    body_preview: str
    practice_hint: Optional[str] = None
    solution_hint: Optional[str] = None
    difficulty_level: str = "intermediate"


@dataclass
class PracticeExtraction:
    """实践提取结果"""
    practice_name: str
    category: str
    description: str
    source_issue: int
    confidence: float
    code_example: Optional[str] = None
    related_issues: List[int] = field(default_factory=list)


@dataclass
class CommonProblem:
    """常见问题定义"""
    problem_id: str
    title: str
    frequency: int  # 出现次数
    solutions: List[Dict]  # 解决方案列表
    first_mentioned: str
    severity: str = "medium"


@dataclass
class ScanResult:
    """扫描结果总览"""
    repo_name: str
    repo_url: str
    total_issues_scanned: int
    practices_extracted: int
    common_problems: List[CommonProblem]
    best_practices: List[Dict]
    scan_duration_seconds: float
    scanned_at: str
    recommendations: List[str]


class GeneratorScanner:
    """生成器扫描器"""

    def __init__(self, config: Dict):
        self.config = config
        self.repo_urls: List[str] = []
        self._load_repo_urls()

    def scan_repository(self, repo_url: str, limit: int = 100) -> ScanResult:
        """
        扫描单个仓库

        Args:
            repo_url: GitHub 仓库 URL
            limit: 最多扫描的 issue 数

        Returns:
            ScanResult 扫描结果
        """
        start_time = datetime.now()

        # 提取仓库名称
        repo_name = self._extract_repo_name(repo_url)
        print(f"[生成器扫描器] 开始扫描仓库: {repo_name}")

        # 构建搜索 URL
        # 实际使用中应该调用 GitHub API 或 MCP github_scanner
        # 这里使用占位符实现

        issues_analyzed = self._simulate_issue_scan(repo_url, limit)

        # 提取最佳实践
        practices = self._extract_practices_from_issues(issues_analyzed)

        # 识别常见问题
        common_problems = self._identify_common_problems(issues_analyzed)

        # 生成最佳实践总结
        best_practices = self._summarize_best_practices(issues_analyzed, practices)

        # 生成推荐
        recommendations = self._generate_recommendations(issues_analyzed, practices, common_problems)

        duration = (datetime.now() - start_time).total_seconds()

        result = ScanResult(
            repo_name=repo_name,
            repo_url=repo_url,
            total_issues_scanned=len(issues_analyzed),
            practices_extracted=len(practices),
            common_problems=common_problems,
            best_practices=best_practices,
            scan_duration_seconds=duration,
            scanned_at=datetime.now().isoformat(),
            recommendations=recommendations
        )

        print(f"[生成器扫描器] 扫描完成: {repo_name}")
        print(f"  - 扫描 issue: {len(issues_analyzed)}")
        print(f"  - 提取实践: {len(practices)}")
        print(f"  - 识别常见问题: {len(common_problems)}")
        print(f"  - 耗时: {duration:.1f} 秒")

        return result

    def scan_multiple_repos(self, repo_urls: List[str]) -> List[ScanResult]:
        """扫描多个仓库"""
        results = []

        for repo_url in repo_urls:
            try:
                result = self.scan_repository(repo_url)
                results.append(result)
            except Exception as e:
                print(f"[生成器扫描器] 扫描失败 {repo_url}: {e}")

        return results

    def _extract_repo_name(self, repo_url: str) -> str:
        """从 URL 提取仓库名称"""
        # https://github.com/flutterblue/flutter_blue_plus/issues/123
        # -> flutter_blue_plus
        parts = repo_url.rstrip('/').split('/')
        return parts[-1] if parts else 'unknown'

    def _simulate_issue_scan(self, repo_url: str, limit: int = 100) -> List[IssueAnalysis]:
        """模拟 Issue 扫描（实际需要使用 GitHub API）"""
        # 这是一个占位符实现
        # 实际使用中应该使用 GitHub API 或 MCP github_scanner

        issues = []
        repo_name = self._extract_repo_name(repo_url)

        # 模拟不同类型的 issues
        mock_issue_types = [
            ("connection issue", "Cannot connect to device", "connection", "high"),
            ("rssi issue", "RSSI not updating", "rssi", "medium"),
            ("performance issue", "App freezes when scanning", "performance", "high"),
            ("best practice", "How to implement retry logic", "general", "low"),
            ("documentation", "Missing parameter documentation", "docs", "low"),
            ("example", "Code example for background scanning", "example", "low")
        ]

        for i, (issue_type, title_template, category, severity) in enumerate(mock_issue_types[:limit]):
            issues.append(IssueAnalysis(
                issue_number=1000 + i,
                title=f"{repo_name}: {title_template}",
                url=f"{repo_url}/issues/{1000 + i}",
                state="open" if i % 5 == 0 else "closed",
                created_at=datetime.now().isoformat(),
                comments_count=(limit - i) * 3,
                reactions={"+1": (limit - i) * 5, "rocket": (limit - i) * 2},
                labels=[category, f"severity:{severity}"],
                body_preview=f"This is a mock issue about {category}...",
                difficulty_level="intermediate"
            ))

        return issues

    def _extract_practices_from_issues(self, issues: List[IssueAnalysis]) -> List[PracticeExtraction]:
        """从 issues 提取实践"""
        practices = []

        # 常见实践关键词
        practice_keywords = {
            'connection': ['connect', 'disconnect', 'retry', 'timeout', 'reconnect'],
            'rssi': ['rssi', 'signal', 'scan', 'subscribe', 'notification'],
            'performance': ['optimize', 'performance', 'lazy', 'cache', 'debounce'],
            'architecture': ['mvvm', 'repository', 'provider', 'service', 'clean'],
            'testing': ['test', 'mock', 'unit', 'integration', 'widget']
        }

        for issue in issues:
            title_lower = issue.title.lower()
            body_lower = issue.body_preview.lower()

            # 分析 issue 标题和内容
            for practice_name, keywords in practice_keywords.items():
                if any(kw in title_lower for kw in keywords):
                    # 确定置信度
                    confidence = 0.5

                    if issue.state == 'closed':
                        confidence += 0.3

                    if issue.reactions.get('+1', 0) > 10:
                        confidence += 0.2

                    if issue.comments_count > 5:
                        confidence += 0.1

                    practice = PracticeExtraction(
                        practice_name=practice_name,
                        category=self._categorize_issue(issue.labels),
                        description=f"从 issue #{issue.issue_number} 提取的实践",
                        source_issue=issue.issue_number,
                        confidence=min(confidence, 1.0),
                        related_issues=[issue.issue_number]
                    )

                    practices.append(practice)
                    break

        return practices

    def _categorize_issue(self, labels: List[str]) -> str:
        """对 issue 进行分类"""
        for label in labels:
            if 'connection' in label:
                return 'connection'
            elif 'rssi' in label:
                return 'rssi'
            elif 'performance' in label:
                return 'performance'
            elif 'architecture' in label:
                return 'architecture'
            elif 'test' in label:
                return 'testing'
        return 'general'

    def _identify_common_problems(self, issues: List[IssueAnalysis]) -> List[CommonProblem]:
        """识别常见问题"""
        problem_freq = {}

        # 统计问题频率
        for issue in issues:
            # 标准化问题标题（去除仓库名等）
            problem_key = self._normalize_problem_title(issue.title)

            if problem_key not in problem_freq:
                problem_freq[problem_key] = {
                    'title': problem_key,
                    'count': 0,
                    'first_mentioned': issue.created_at,
                    'solutions': [],
                    'severity': 'medium'
                }

            problem_freq[problem_key]['count'] += 1

            # 收集解决方案（从 issue 内容或评论中）
            # 这里简化处理
            if issue.state == 'closed':
                problem_freq[problem_key]['solutions'].append({
                    'issue_number': issue.issue_number,
                    'description': 'Solution in discussion',
                    'votes': issue.reactions.get('+1', 0)
                })

        # 转换为 CommonProblem 列表
        common_problems = []

        for problem_key, problem_data in problem_freq.items():
            if problem_data['count'] >= 3:  # 至少出现 3 次
                # 确定严重程度
                if problem_data['count'] >= 10:
                    severity = 'high'
                elif problem_data['count'] >= 5:
                    severity = 'medium'
                else:
                    severity = 'low'

                common_problem = CommonProblem(
                    problem_id=f"prob_{problem_key.replace(' ', '_')}",
                    title=problem_data['title'],
                    frequency=problem_data['count'],
                    solutions=problem_data['solutions'][:5],  # 最多 5 个解决方案
                    first_mentioned=problem_data['first_mentioned'],
                    severity=severity
                )

                common_problems.append(common_problem)

        # 按频率排序
        common_problems.sort(key=lambda p: p.frequency, reverse=True)

        return common_problems[:20]  # 最多返回 20 个常见问题

    def _normalize_problem_title(self, title: str) -> str:
        """标准化问题标题"""
        # 移除仓库名称
        normalized = title.lower()

        # 移除常见前缀
        prefixes = ['how to', 'problem with', 'issue:', 'bug:', 'error:']
        for prefix in prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):].strip()

        # 移除特殊字符
        normalized = re.sub(r'[^a-z0-9\s]', '', normalized).strip()

        return normalized

    def _summarize_best_practices(self, issues: List[IssueAnalysis],
                                  practices: List[PracticeExtraction]) -> List[Dict]:
        """总结最佳实践"""
        best_practices = []

        # 按 practice 分组
        practices_by_name = {}
        for practice in practices:
            if practice.practice_name not in practices_by_name:
                practices_by_name[practice.practice_name] = {
                    'count': 0,
                    'issues': [],
                    'total_confidence': 0.0,
                    'closed_count': 0
                }

            p_data = practices_by_name[practice.practice_name]
            p_data['count'] += 1
            p_data['issues'].append(practice.source_issue)
            p_data['total_confidence'] += practice.confidence
            if practice.source_issue in [i.issue_number for i in issues if i.state == 'closed']:
                p_data['closed_count'] += 1

        # 转换为最佳实践列表
        for practice_name, data in practices_by_name.items():
            if data['count'] >= 3:  # 至少出现 3 次
                avg_confidence = data['total_confidence'] / data['count']
                success_rate = data['closed_count'] / data['count']

                best_practices.append({
                    'name': practice_name,
                    'frequency': data['count'],
                    'avg_confidence': avg_confidence,
                    'success_rate': success_rate,
                    'related_issues': data['issues'][:5],
                    'category': self._infer_category(practice_name)
                })

        # 按综合评分排序
        best_practices.sort(
            key=lambda x: x['avg_confidence'] * x['success_rate'] * x['frequency'],
            reverse=True
        )

        return best_practices[:10]

    def _infer_category(self, practice_name: str) -> str:
        """推断实践类别"""
        category_mapping = {
            'connection': 'networking',
            'rssi': 'data',
            'performance': 'performance',
            'mvvm': 'architecture',
            'repository': 'architecture',
            'provider': 'state-management',
            'service': 'architecture',
            'test': 'testing'
        }
        return category_mapping.get(practice_name, 'general')

    def _generate_recommendations(self, issues: List[IssueAnalysis],
                                practices: List[PracticeExtraction],
                                problems: List[CommonProblem]) -> List[str]:
        """生成推荐"""
        recommendations = []

        # 分析 issues 状态
        open_issues = [i for i in issues if i.state == 'open']
        if len(open_issues) > 10:
            recommendations.append(
                f"仓库有 {len(open_issues)} 个未解决 issue，建议优先处理已知问题"
            )

        # 分析问题严重程度
        high_severity_problems = [p for p in problems if p.severity == 'high']
        if high_severity_problems:
            recommendations.append(
                f"发现 {len(high_severity_problems)} 个高频严重问题，建议在文档中添加故障排除指南"
            )

        # 分析最佳实践应用
        if practices:
            avg_confidence = sum(p.confidence for p in practices) / len(practices)
            if avg_confidence < 0.6:
                recommendations.append(
                    "提取的实践置信度较低，建议验证后应用"
                )

        # 分析代码示例需求
        code_example_issues = [i for i in issues if 'example' in i.title.lower()]
        if len(code_example_issues) > 0:
            recommendations.append(
                f"建议添加更多代码示例以提高易用性"
            )

        return recommendations

    def _load_repo_urls(self) -> None:
        """从配置加载仓库 URL"""
        self.repo_urls = []

        # 从各个域名的配置中提取仓库
        for domain, config in self.config.get('domains', {}).items():
            if 'repos' in config:
                for repo in config['repos']:
                    url = self._extract_github_url(repo)
                    if url:
                        self.repo_urls.append(url)

    def _extract_github_url(self, repo_config: Dict) -> str:
        """从仓库配置提取 GitHub URL"""
        repo_name = repo_config.get('name', '')
        if 'url' in repo_config:
            return repo_config['url']

        # 构建默认 URL
        return f"https://github.com/{repo_name}"

    def save_scan_results(self, results: List[ScanResult], output_file: str) -> None:
        """保存扫描结果"""
        output = {
            'version': '1.0',
            'scanned_at': datetime.now().isoformat(),
            'total_repos': len(results),
            'results': [r.__dict__ for r in results],
            'summary': {
                'total_issues': sum(r.total_issues_scanned for r in results),
                'total_practices': sum(r.practices_extracted for r in results),
                'total_problems': sum(len(r.common_problems) for r in results)
            }
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"[生成器扫描器] 已保存扫描结果到 {output_file}")

    def generate_scan_report(self, results: List[ScanResult]) -> str:
        """生成扫描报告"""
        lines = [
            "# 生成器扫描报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            f"扫描仓库数: {len(results)}",
            "",
            "## 扫描摘要",
            ""
        ]

        total_issues = sum(r.total_issues_scanned for r in results)
        total_practices = sum(r.practices_extracted for r in results)
        total_problems = sum(len(r.common_problems) for r in results)

        lines.extend([
            f"- 总扫描 Issue: {total_issues}",
            f"- 提取最佳实践: {total_practices}",
            f"- 识别常见问题: {total_problems}",
            "",
            "## 仓库详情",
            ""
        ])

        for result in results:
            lines.extend([
                f"### {result.repo_name}",
                f"",
                f"**扫描耗时**: {result.scan_duration_seconds:.1f} 秒",
                f"**扫描 Issue**: {result.total_issues_scanned}",
                f"**提取实践**: {result.practices_extracted}",
                f"**识别问题**: {len(result.common_problems)}",
                "",
                "**最佳实践（前 5）**:",
                ""
            ])

            for i, practice in enumerate(result.best_practices[:5]):
                lines.append(f"{i+1}. {practice['name']} (置信度: {practice['avg_confidence']:.2f}, 成功率: {practice['success_rate']:.2f})")

            if result.common_problems:
                lines.extend([
                    "",
                    "**高频问题（前 3）**:",
                    ""
                ])

                for problem in result.common_problems[:3]:
                    lines.append(f"- {problem['title']} (频率: {problem['frequency']}, 严重程度: {problem['severity']})")

            if result.recommendations:
                lines.extend([
                    "",
                    "**推荐**:",
                    ""
                ])

                for rec in result.recommendations:
                    lines.append(f"- {rec}")

            lines.append("")

        return "\n".join(lines)
