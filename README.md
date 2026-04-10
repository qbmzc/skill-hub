# skill-hub

本仓库收集可在 Cursor / Codex 等 Agent 中复用的 **Skills**：每个 skill 为独立目录，内含 `SKILL.md`（YAML frontmatter + 正文说明）。

## 目录结构

```
skills/
├── code-review/       # PR / 代码审查清单与输出格式
├── git-commit/        # 基于 diff 的 Conventional Commits 文案
├── pr-description/    # PR 描述模板（摘要、测试计划、风险）
├── refactor-safely/   # 安全重构步骤与红线
├── debug-playbook/    # 系统化排错流程
└── doc-api-outline/   # API 文档大纲（OpenAPI / README 用）
```

## 如何使用

1. **整库克隆**后，将需要的子目录复制或软链到 Cursor 项目技能目录：
   - 项目内：`<你的项目>/.cursor/skills/<skill-name>/`
   - 或用户级：`~/.cursor/skills/<skill-name>/`
2. 确保每个 skill 目录下存在 `SKILL.md`，且含有效的 `name` 与 `description` 字段（供 Agent 发现与触发）。
3. 可按团队规范修改各 `SKILL.md` 中的清单、模板或术语。

## 新增 skill

建议遵循 [Cursor 官方 create-skill 指南](https://cursor.com/docs) 中的约定：`name` 小写与连字符、`description` 写清「做什么 + 何时用」、正文保持精简（复杂内容可拆 `reference.md`）。

## 许可

各 skill 内容为项目内文档；使用与分发方式由仓库维护者自行约定。
