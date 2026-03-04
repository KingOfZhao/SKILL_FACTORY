"""
最佳实践收集模块

负责从多个来源自动收集和整合某个技术领域的最佳实践。
"""

import json
from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class SourceType(Enum):
    """来源类型枚举"""
    OFFICIAL_DOCS = "official-docs"
    REPOS = "repos"
    PACKAGES = "packages"
    QA_COMMUNITIES = "qa-communities"
    FORUMS = "forums"
    BLOGS = "blogs"
    VIDEOS = "videos"
    CONFERENCES = "conferences"


class Difficulty(Enum):
    """难度等级枚举"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class SourceReference:
    """来源引用"""
    source_type: SourceType
    url: str
    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    credibility_score: int = 50
    verified: bool = False
    votes: int = 0


@dataclass
class Pattern:
    """模式定义"""
    id: str
    name: str
    category: str
    description: str
    implementation: str
    example: Optional[str] = None
    related_practices: List[str] = field(default_factory=list)


@dataclass
class BestPractice:
    """最佳实践定义"""
    id: str
    title: str
    description: str
    category: str
    difficulty: Difficulty
    tags: List[str]
    sources: List[SourceReference]
    related_patterns: List[Pattern]
    pros: List[str]
    cons: List[str]
    applicable_scenarios: List[str]
    code_example: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class BestPracticeCollector:
    """最佳实践收集器"""

    def __init__(self, domain: str, config: Dict):
        self.domain = domain
        self.config = config
        self.collected_practices: List[BestPractice] = []
        self.sources_config = config.get('domains', {}).get(domain, {})

    def collect(self, query: str, context_keywords: List[str]) -> List[BestPractice]:
        """
        收集最佳实践

        Args:
            query: 搜索查询
            context_keywords: 上下文关键词列表

        Returns:
            收集到的最佳实践列表
        """
        print(f"[最佳实践收集器] 开始收集 {self.domain} 领域的最佳实践: {query}")

        all_results = []

        # 从各个来源收集
        if 'official_docs' in self.sources_config:
            all_results.extend(self._collect_official_docs(query, context_keywords))

        if 'repos' in self.sources_config:
            all_results.extend(self._collect_from_repos(query, context_keywords))

        if 'packages' in self.sources_config:
            all_results.extend(self._collect_from_packages(query, context_keywords))

        if 'qa' in self.sources_config:
            all_results.extend(self._collect_from_qa(query, context_keywords))

        if 'forums' in self.sources_config:
            all_results.extend(self._collect_from_forums(query, context_keywords))

        if 'blogs' in self.sources_config:
            all_results.extend(self._collect_from_blogs(query, context_keywords))

        if 'videos' in self.sources_config:
            all_results.extend(self._collect_from_videos(query, context_keywords))

        # 去重
        unique_results = self._deduplicate_results(all_results)

        # 评分和排序
        ranked_results = self._rank_results(unique_results)

        # 转换为 BestPractice 对象
        practices = self._convert_to_practices(ranked_results, query, context_keywords)

        self.collected_practices.extend(practices)
        print(f"[最佳实践收集器] 收集完成，共 {len(practices)} 个实践")

        return practices

    def _collect_official_docs(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从官方文档收集"""
        results = []

        for doc_source in self.sources_config.get('official_docs', []):
            url = doc_source.get('url', '')
            sections = doc_source.get('sections', [])

            # 构建搜索 URL
            search_url = f"{url}/search?q={query}"

            # 模拟搜索结果（实际需要 MCP web_search 工具）
            results = self._simulate_search_results(search_url, count=3)

            for result in results:
                results.append({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'type': SourceType.OFFICIAL_DOCS,
                    'source_name': doc_source.get('name', 'Official Docs'),
                    'credibility_score': 100,
                    'verified': True
                })

        print(f"[官方文档] 从 {len(self.sources_config.get('official_docs', []))} 个来源收集到 {len(results)} 个结果")
        return results

    def _collect_from_repos(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从代码仓库收集"""
        results = []

        for repo in self.sources_config.get('repos', []):
            repo_name = repo.get('name', '')
            priority = repo.get('priority', 10)
            repo_type = repo.get('type', 'community')

            # GitHub issue 搜索
            search_query = f"{query} best practices"
            search_url = f"https://github.com/search?q={search_query}&type=issues"

            # 模拟搜索结果
            issues = self._simulate_search_results(search_url, count=min(5, 15 - priority))

            for issue in issues:
                results.append({
                    'url': issue.get('url', ''),
                    'title': issue.get('title', ''),
                    'type': SourceType.REPOS,
                    'source_name': repo_name,
                    'credibility_score': 90 if repo_type == 'official' else 75,
                    'verified': repo_type == 'official',
                    'votes': issue.get('votes', 0)
                })

        print(f"[代码仓库] 从 {len(self.sources_config.get('repos', []))} 个仓库收集到 {len(results)} 个结果")
        return results

    def _collect_from_packages(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从包仓库收集"""
        results = []

        for pkg in self.sources_config.get('packages', []):
            pkg_name = pkg.get('name', '')
            url = pkg.get('url', '')
            likes_threshold = pkg.get('likes_threshold', 1000)

            # 包搜索
            search_url = f"{url}/search?q={query}"

            # 模拟搜索结果
            packages = self._simulate_search_results(search_url, count=3)

            for pkg_info in packages:
                likes = pkg_info.get('likes', 0)
                if likes >= likes_threshold:
                    results.append({
                        'url': url,
                        'title': pkg_info.get('title', pkg_name),
                        'type': SourceType.PACKAGES,
                        'source_name': pkg_name,
                        'credibility_score': min(85 + likes // 1000, 95),
                        'verified': likes >= 5000,
                        'votes': likes
                    })

        print(f"[包仓库] 从 {len(self.sources_config.get('packages', []))} 个包收集到 {len(results)} 个结果")
        return results

    def _collect_from_qa(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从问答社区收集"""
        results = []

        for qa_source in self.sources_config.get('qa', []):
            platform = qa_source.get('platform', 'stackoverflow')
            tags = qa_source.get('tags', [])
            min_score = qa_source.get('min_score', 10)

            for tag in tags:
                search_query = f"{query} {tag}" if tag else query
                search_url = f"{platform}/questions?q={search_query}&sort=votes"

                # 模拟搜索结果
                answers = self._simulate_search_results(search_url, count=5)

                for answer in answers:
                    score = answer.get('score', 0)
                    if score >= min_score:
                        results.append({
                            'url': answer.get('url', ''),
                            'title': answer.get('title', ''),
                            'type': SourceType.QA_COMMUNITIES,
                            'source_name': platform,
                            'credibility_score': min(75 + score // 5, 90),
                            'verified': score >= 50,
                            'votes': score
                        })

        print(f"[问答社区] 从 {len(self.sources_config.get('qa', []))} 个 QA 来源收集到 {len(results)} 个结果")
        return results

    def _collect_from_forums(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从论坛收集"""
        results = []

        for forum_source in self.sources_config.get('forums', []):
            platform = forum_source.get('platform', 'reddit')
            communities = forum_source.get('communities', [])
            min_upvotes = forum_source.get('min_upvotes', 5)

            for community in communities:
                community_name = community.get('name', '')
                search_url = f"https://www.reddit.com/r/{community_name}/search?q={query}&sort=top&t=all"

                # 模拟搜索结果
                posts = self._simulate_search_results(search_url, count=5)

                for post in posts:
                    upvotes = post.get('upvotes', 0)
                    if upvotes >= min_upvotes:
                        results.append({
                            'url': post.get('url', ''),
                            'title': post.get('title', ''),
                            'type': SourceType.FORUMS,
                            'source_name': community_name,
                            'credibility_score': min(65 + upvotes // 2, 80),
                            'verified': upvotes >= 20,
                            'votes': upvotes
                        })

        print(f"[论坛] 从 {len(self.sources_config.get('forums', []))} 个论坛收集到 {len(results)} 个结果")
        return results

    def _collect_from_blogs(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从博客平台收集"""
        results = []

        for blog_source in self.sources_config.get('blogs', []):
            platform = blog_source.get('platform', 'medium')
            publications = blog_source.get('publications', [])

            for pub in publications:
                pub_name = pub.get('name', '')
                search_url = f"{platform}/search?q={query} {pub_name}"

                # 模拟搜索结果
                articles = self._simulate_search_results(search_url, count=5)

                for article in articles:
                    results.append({
                        'url': article.get('url', ''),
                        'title': article.get('title', ''),
                        'type': SourceType.BLOGS,
                        'source_name': pub_name,
                        'credibility_score': 65,
                        'verified': pub.get('type', 'curated') == 'official',
                        'votes': article.get('claps', 0)
                    })

        print(f"[博客] 从 {len(self.sources_config.get('blogs', []))} 个博客来源收集到 {len(results)} 个结果")
        return results

    def _collect_from_videos(self, query: str, context_keywords: List[str]) -> List[Dict]:
        """从视频平台收集"""
        results = []

        for video_source in self.sources_config.get('videos', []):
            platform = video_source.get('platform', 'youtube')
            channels = video_source.get('channels', [])

            for channel in channels:
                channel_name = channel.get('name', '')
                channel_url = channel.get('url', '')
                search_url = f"{platform}/results?search_query={query}+{channel_name}"

                # 模拟搜索结果
                videos = self._simulate_search_results(search_url, count=3)

                for video in videos:
                    results.append({
                        'url': video.get('url', ''),
                        'title': video.get('title', ''),
                        'type': SourceType.VIDEOS,
                        'source_name': channel_name,
                        'credibility_score': 60 if channel.get('type') == 'educational' else 50,
                        'verified': channel.get('type') == 'official',
                        'votes': video.get('views', 0)
                    })

        print(f"[视频] 从 {len(self.sources_config.get('videos', []))} 个视频频道收集到 {len(results)} 个结果")
        return results

    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """去重结果"""
        seen_urls = set()
        unique_results = []

        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results

    def _rank_results(self, results: List[Dict]) -> List[Dict]:
        """对结果进行评分和排序"""
        for result in results:
            base_score = result.get('credibility_score', 50)

            # 额外加分
            score = base_score

            # 有标题 (+5)
            if result.get('title'):
                score += 5

            # 有作者 (+3)
            if result.get('author'):
                score += 3

            # 有投票/赞数 (+10)
            votes = result.get('votes', 0)
            if votes > 0:
                score += min(10, votes // 10)

            # 已验证 (+15)
            if result.get('verified'):
                score += 15

            result['final_score'] = score

        # 按分数排序
        sorted_results = sorted(results, key=lambda x: x.get('final_score', 0), reverse=True)

        return sorted_results[:50]  # 最多返回 50 个结果

    def _convert_to_practices(self, results: List[Dict], query: str,
                              context_keywords: List[str]) -> List[BestPractice]:
        """将搜索结果转换为 BestPractice 对象"""
        practices = []

        for i, result in enumerate(results):
            practice_id = f"practice_{self.domain}_{i}"

            # 分析难度
            difficulty = self._infer_difficulty(result)

            # 提取标签
            tags = self._extract_tags(result, context_keywords)

            # 提取优缺点
            pros, cons = self._extract_pros_cons(result)

            # 构建来源引用
            source_ref = SourceReference(
                source_type=result.get('type', SourceType.BLOGS),
                url=result.get('url', ''),
                title=result.get('title', ''),
                credibility_score=result.get('final_score', 50),
                verified=result.get('verified', False),
                votes=result.get('votes', 0)
            )

            practice = BestPractice(
                id=practice_id,
                title=result.get('title', ''),
                description=result.get('description', result.get('title', '')),
                category=self._categorize_practice(result, context_keywords),
                difficulty=difficulty,
                tags=tags,
                sources=[source_ref],
                pros=pros,
                cons=cons,
                applicable_scenarios=self._extract_scenarios(result, context_keywords)
            )

            practices.append(practice)

        return practices

    def _infer_difficulty(self, result: Dict) -> Difficulty:
        """推断难度"""
        title = result.get('title', '').lower()
        description = result.get('description', '').lower()

        # 根据关键词推断
        if any(kw in title or kw in description for kw in ['beginner', 'basic', 'getting started']):
            return Difficulty.BEGINNER
        elif any(kw in title or kw in description for kw in ['advanced', 'complex', 'optimization', 'architecture']):
            return Difficulty.ADVANCED
        else:
            return Difficulty.INTERMEDIATE

    def _extract_tags(self, result: Dict, context_keywords: List[str]) -> List[str]:
        """提取标签"""
        title = result.get('title', '').lower()
        tags = context_keywords.copy()

        # 从标题中提取额外标签
        if 'state' in title or 'riverpod' in title or 'bloc' in title:
            tags.append('state-management')
        if 'architecture' in title or 'clean' in title or 'mvvm' in title:
            tags.append('architecture')
        if 'ui' in title or 'widget' in title or 'component' in title:
            tags.append('ui')
        if 'test' in title:
            tags.append('testing')
        if 'performance' in title:
            tags.append('performance')

        return list(set(tags))

    def _extract_pros_cons(self, result: Dict) -> tuple:
        """提取优缺点（模拟）"""
        # 实际实现中需要从内容中解析
        # 这里只是模拟
        return (["经过社区验证"], ["可能需要根据项目调整"])

    def _extract_scenarios(self, result: Dict, context_keywords: List[str]) -> List[str]:
        """提取适用场景"""
        scenarios = ["通用场景"]

        # 根据关键词推断场景
        if 'mobile' in context_keywords:
            scenarios.append("移动应用")
        if 'web' in context_keywords:
            scenarios.append("Web 应用")
        if 'bluetooth' in context_keywords:
            scenarios.append("蓝牙应用")
        if 'database' in context_keywords:
            scenarios.append("数据密集应用")

        return scenarios

    def _categorize_practice(self, result: Dict, context_keywords: List[str]) -> str:
        """对实践进行分类"""
        title = result.get('title', '').lower()

        if 'architecture' in title or 'clean' in title:
            return "architecture"
        elif 'state' in title or 'riverpod' in title or 'bloc' in title:
            return "state-management"
        elif 'ui' in title or 'widget' in title:
            return "ui-components"
        elif 'api' in title or 'network' in title:
            return "networking"
        elif 'test' in title:
            return "testing"
        elif 'performance' in title:
            return "performance"
        else:
            return "general"

    def _simulate_search_results(self, url: str, count: int = 5) -> List[Dict]:
        """模拟搜索结果（实际需要使用 MCP web_search）"""
        # 这是一个占位符实现
        # 实际使用中应该调用 web_search MCP 工具

        results = []
        for i in range(count):
            results.append({
                'url': f"{url}&page={i}",
                'title': f"搜索结果 #{i+1}",
                'description': f"模拟的搜索结果描述",
                'votes': (count - i) * 10,
                'upvotes': (count - i) * 5,
                'views': (count - i) * 100,
                'claps': (count - i) * 8,
                'likes': (count - i) * 50
            })

        return results

    def save_to_file(self, filepath: str) -> None:
        """保存收集到的最佳实践到文件"""
        practices_data = [p.__dict__ for p in self.collected_practices]

        output = {
            'version': '1.0',
            'domain': self.domain,
            'collected_at': datetime.now().isoformat(),
            'total_practices': len(self.collected_practices),
            'practices': practices_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"[最佳实践收集器] 已保存 {len(self.collected_practices)} 个实践到 {filepath}")

    def load_from_file(self, filepath: str) -> List[BestPractice]:
        """从文件加载最佳实践"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                practices_data = data.get('practices', [])

                practices = [
                    BestPractice(**p) for p in practices_data
                ]

                self.collected_practices = practices
                print(f"[最佳实践收集器] 已从 {filepath} 加载 {len(practices)} 个实践")
                return practices
        except FileNotFoundError:
            print(f"[最佳实践收集器] 文件不存在: {filepath}")
            return []
        except Exception as e:
            print(f"[最佳实践收集器] 加载失败: {e}")
            return []
