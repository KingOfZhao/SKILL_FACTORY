# 领域知识库

此模块定义了各个领域的最佳实践知识库结构，支持自动收集、整合和检索领域相关的最佳实践。

## 核心概念

### 领域 (Domain)
领域代表一个技术领域或应用场景，例如：Flutter、Android、iOS、React Native、Web、AI、ML 等。

每个领域包含：
- 最佳实践列表
- 常见模式
- 推荐工具/库
- 已知问题和解决方案
- 社区资源链接

### 最佳实践 (Best Practice)
最佳实践是经过验证的、被广泛接受的做法，能提高开发效率和代码质量。

结构：
```typescript
interface BestPractice {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
  codeExample?: string;
  sources: SourceReference[];
  relatedPatterns?: Pattern[];
  pros: string[];
  cons?: string[];
  applicableScenarios: string[];
}
```

### 来源引用 (Source Reference)
记录最佳实践来自何处，便于追溯和验证。

```typescript
interface SourceReference {
  type: 'github' | 'pub.dev' | 'stackoverflow' | 'reddit' |
         'medium' | 'youtube' | 'official-docs' | 'devto' |
         'hackernews' | 'conference' | 'blog' | 'custom';
  url: string;
  title?: string;
  author?: string;
  publishedAt?: string;
  credibilityScore?: number; // 可信度评分 (0-100)
  verified?: boolean; // 是否经过社区验证
}
```

### 模式 (Pattern)
可复用的解决方案模式，可以组合使用。

```typescript
interface Pattern {
  id: string;
  name: string;
  category: 'architectural' | 'ui' | 'state-management' | 'data' |
           'error-handling' | 'testing' | 'performance' | 'security';
  description: string;
  implementation: string;
  example?: string;
  relatedPractices: string[];
}
```

## 领域分类

### Flutter 领域
- **架构模式**: Clean Architecture、MVVM、BLoC、Provider
- **状态管理**: Riverpod、Bloc、Provider、GetX
- **UI 组件**: Material Design 3、Adaptive Layout、Animations
- **数据可视化**: fl_chart、syncfusion_charts
- **网络请求**: dio、http、rest_client
- **本地存储**: sqflite、hive、shared_preferences
- **蓝牙相关**: flutter_blue_plus、flutter_bluetooth_serial
- **测试**: widget_test、integration_test、golden_test

### Android 领域
- **架构模式**: MVVM、MVP、Clean Architecture
- **UI 组件**: Jetpack Compose、Views、Material Components
- **网络请求**: Retrofit、OkHttp、Volley
- **本地存储**: Room、DataStore、SharedPreferences
- **后台服务**: WorkManager、Foreground Service
- **测试**: JUnit、Espresso、UI Automator

### iOS 领域
- **架构模式**: MVC、MVVM、VIPER、Coordinator
- **UI 组件**: SwiftUI、UIKit、Material Design
- **网络请求**: URLSession、Alamofire
- **本地存储**: Core Data、UserDefaults、Realm
- **后台服务**: Background Tasks、BGTaskScheduler
- **测试**: XCTest、XCUITest

### React Native 领域
- **架构模式**: Redux、MobX、Recoil、Zustand
- **UI 组件**: React Native Paper、Native Base、Tamagui
- **导航**: React Navigation、React Native Navigation
- **状态管理**: Context API、Redux、MobX
- **网络请求**: Axios、fetch、RTK Query
- **测试**: Jest、Detox、React Native Testing Library

### Web 领域
- **前端框架**: React、Vue、Angular、Svelte、Solid
- **状态管理**: Redux、Zustand、Jotai、Pinia
- **UI 组件**: Material-UI、Ant Design、Chakra UI、Tailwind
- **构建工具**: Vite、Webpack、esbuild、Next.js
- **测试**: Vitest、Jest、Playwright、Cypress

### AI/ML 领域
- **框架**: TensorFlow、PyTorch、scikit-learn、Transformers
- **数据处理**: Pandas、NumPy、Apache Spark
- **模型服务**: TensorFlow Serving、TorchServe、ONNX Runtime
- **MLOps**: MLflow、Weights & Biases、DVC
- **测试**: MLflow、Weights & Biases、DVC

## 知识存储格式

### JSON 结构
```json
{
  "version": "1.0",
  "lastUpdated": "2026-02-27T00:00:00Z",
  "domains": {
    "flutter": {
      "bestPractices": [...],
      "patterns": [...],
      "tools": [...],
      "commonIssues": [...]
    },
    "android": {
      "bestPractices": [...],
      "patterns": [...],
      "tools": [...],
      "commonIssues": [...]
    }
  }
},
"sources": {
  "github": {
    "baseSearchUrl": "https://github.com/search?q=",
    "repos": ["flutter/flutter", "flutterblue/flutter_blue_plus", "fl_chart/fl_chart"]
  },
  "pub.dev": {
    "baseSearchUrl": "https://pub.dev/search?q=",
    "popularPackages": ["provider", "riverpod", "flutter_blue_plus", "fl_chart"]
  },
  "stackoverflow": {
    "baseSearchUrl": "https://stackoverflow.com/search?q=",
    "tags": ["flutter", "dart", "android", "ios"]
  },
  "reddit": {
    "communities": ["r/FlutterDev", "r/androiddev", "r/iOSProgramming"],
    "baseSearchUrl": "https://www.reddit.com/r/{community}/search?q="
  },
  "medium": {
    "baseSearchUrl": "https://medium.com/search?q=",
    "publications": ["Flutter", "Flutter Medium Blog"]
  },
  "youtube": {
    "baseSearchUrl": "https://www.youtube.com/results?search_query=",
    "channels": ["Flutter", "Android Developers", "Google Developers"]
  },
  "officialDocs": {
    "flutter": "https://docs.flutter.dev",
    "android": "https://developer.android.com",
    "ios": "https://developer.apple.com"
  },
  "conferences": {
    "fluttercon": "https://fluttercon.dev",
    "devfest": "https://devfest.dev",
    "googleio": "https://developers.google.com/events"
  }
}
```

## 最佳实践来源优先级

收集来源按优先级排序：

### 第一优先级：官方文档
- docs.flutter.dev (Flutter 官方文档)
- developer.android.com (Android 官方文档)
- developer.apple.com (iOS 官方文档)

### 第二优先级：权威仓库
- Flutter 官方 GitHub (flutter/flutter)
- 流行包的 GitHub 仓库
- Awesome 列表 (awesome-flutter 等)

### 第三优先级：社区资源
- Stack Overflow (已验证答案)
- Reddit (r/FlutterDev 等社区)
- Discord (Flutter 社区服务器)
- Medium (技术博客文章)

### 第四优先级：教程和视频
- YouTube (Flutter 官方频道等)
- Dev.to (技术教程)
- Bilibili (中文教程)

### 第五优先级：会议和事件
- Fluttercon 演讲
- DevFest 议题
- Google I/O Keynote

## 知识更新策略

### 自动收集触发条件
1. **领域识别**: 当识别出创建 Skill 的领域时
2. **关键词提取**: 从问题描述中提取技术关键词
3. **现有知识不足**: 领域知识库中相关内容少于阈值
4. **用户明确请求**: 用户要求收集某个领域的最佳实践

### 收集流程
1. **构建搜索查询**: 根据领域 + 上下文关键词
2. **多来源查询**: 并行查询多个来源
3. **结果去重**: 根据 URL 或标题去重
4. **可信度评分**: 根据来源类型、投票数等评分
5. ** relevance 排序**: 根据与问题的相关性排序
6. **知识入库**: 存储到领域知识库

### 知识更新策略
1. **增量更新**: 只更新变动的部分，不全量重写
2. **版本控制**: 保留历史版本，支持回退
3. **定期验证**: 检查链接有效性，更新可信度评分
4. **用户反馈**: 允许用户标记实践的有效性

## 使用示例

### Flutter 蓝牙开发场景
```
问题: "实现 Flutter 蓝牙扫描和 RSSI 实时图表"

领域识别: Flutter + 蓝牙 + 图表

自动收集:
1. 搜索 flutter bluetooth best practices
2. 搜索 flutter_blue_plus github issues
3. 搜索 fl_chart flutter examples
4. 搜索 flutter rssi real-time graph

提取最佳实践:
- 使用 flutter_blue_plus (权威 BLE 库)
- 使用 fl_chart (权威图表库)
- 使用 Stream/StreamController 实时更新
- RSSI 监控间隔 500ms-1000ms
- 使用 Riverpod/Bloc 管理状态
- Clean Architecture 分层

集成到生成:
在 flutter_factory 生成时，自动应用这些实践。
```

## 知识持久化

### 文件位置
- 领域知识库: `domain_knowledge.json`
- 最佳实践索引: `best_practices_index.json`
- 模式注册表: `pattern_registry.json`
- 来源配置: `sources_config.json`

### 备份策略
- 每次更新前自动备份
- 保留最近 5 个版本
- 超过 30 天的旧版本自动清理
