# skill_factory 工程化任务入口。
# 统一用 `python3 -m <tool>` 调用，避免依赖 PATH 中的可执行脚本位置。

PY ?= python3

.DEFAULT_GOAL := help

.PHONY: help install lint format format-check typecheck test cov scan-check ci clean

help: ## 显示可用目标
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## 安装包及开发依赖（可编辑模式）
	$(PY) -m pip install -e ".[dev]"

lint: ## ruff 静态检查
	$(PY) -m ruff check skill_factory tests

format: ## ruff 自动格式化
	$(PY) -m ruff format skill_factory tests

format-check: ## 校验格式（不修改）
	$(PY) -m ruff format --check skill_factory tests

typecheck: ## mypy 类型检查
	$(PY) -m mypy

test: ## 运行测试
	$(PY) -m pytest

cov: ## 运行测试并输出覆盖率
	$(PY) -m pytest --cov=skill_factory --cov-report=term-missing

scan-check: ## 校验技能能力清单是否最新（目录漂移门禁）
	$(PY) -m skill_factory.cli scan --check

ci: lint format-check typecheck cov scan-check ## 本地复跑 CI 全部门禁

clean: ## 清理构建/缓存产物
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov \
		skill_factory.egg-info build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
