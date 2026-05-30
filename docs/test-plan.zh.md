# 测试计划

[English](test-plan.md)

本项目主要产物是 skill、Markdown 文档、JSON 默认参数、shell 脚本和插件 manifest，因此采用轻量结构测试。

## 测试层级

### 单元测试

运行：

```bash
python3 -m unittest discover -s tests -v
```

覆盖范围：

- 插件 manifest 可以解析为 JSON，
- 共享默认参数包含必需配置段和核心值，
- 每个 `SKILL.md` 都有有效 frontmatter，
- 每个 Markdown 文件都有对应语言版本和语言链接，
- README 链接指向存在的本地文件，
- eval 文档包含指标、成功标准和失败标准，
- shell 脚本通过 `bash -n` 语法检查。

### 项目验证

运行：

```bash
./scripts/validate.sh
```

覆盖范围：

- manifest 和共享默认参数的 JSON 语法，
- 本地存在 Codex skill validator 时使用官方校验，
- 没有官方 validator 时使用 fallback frontmatter 校验。

### CI

GitHub Actions 会在 pull request 和 push 到 `main` 时运行。

CI 步骤：

1. checkout 仓库。
2. 设置 Python。
3. 运行 `python3 -m unittest discover -s tests -v`。
4. 运行 `./scripts/validate.sh`。

## 通过标准

所有单元测试和验证脚本都必须通过。

## 失败信号

- JSON 损坏，
- skill frontmatter 缺失，
- README 或 doc 链接损坏，
- 缺少中文或英文对应文件，
- eval 文档没有可衡量标准，
- shell 脚本语法错误。

## 人工检查

发布前人工检查：

- skill description 是否能触发预期任务，
- JSON 默认值是否仍然合理，
- eval 任务是否仍匹配 skill 行为，
- 安装脚本是否只复制本项目拥有的文件。
