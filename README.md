# Scientific Workflow Figure PPT

**简体中文** · [English](README.en.md)

一个用于 **Codex** 的 skill：根据文字描述、手绘草图或参考图，创建或修改**单页、可编辑的 PowerPoint 科研流程图**。适用于研究流程、分析管线、概念框架和模型架构图。

## 特点

- 使用 PowerPoint 原生图形、文字和连接符，便于后续逐项编辑。
- 先梳理实体、层级和关系；对旋转草图按用户指定方向解读。
- 核对数学符号、上下标以及向量和矩阵的维度与方向。
- 用配色和贴近标签的示意图标表达科学含义，避免为填满画布而添加无意义元素。
- 检查文字、排版和连线；指向性连接符通常与物块保留微小可见间距。
- 提供 PPTX 审核脚本，辅助检查结构和可指定的语义约束。

本仓库提供工作流程说明和审核脚本，**不附带 PowerPoint 或独立的 PPT 生成引擎**。创建 PPTX 时，Codex 仍需有可用的演示文稿制作与渲染工具。

## 安装

### 方法一：在 Codex 中安装

在 Codex 中输入：

```text
$skill-installer 请从 GitHub 仓库 Quzhongk/workflow-figure-ppt 的根目录（path: .）安装，并将技能命名为 workflow-figure-ppt。
```

### 方法二：手动克隆

需要先安装 Git。将仓库克隆到个人 skills 目录，使 `SKILL.md` 位于 `workflow-figure-ppt` 文件夹内。

**macOS / Linux**

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Quzhongk/workflow-figure-ppt.git "$HOME/.agents/skills/workflow-figure-ppt"
```

**Windows PowerShell**

```powershell
$skillRoot = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/Quzhongk/workflow-figure-ppt.git (Join-Path $skillRoot 'workflow-figure-ppt')
```

如果你的 Codex 环境使用 `$CODEX_HOME/skills`（通常是 `~/.codex/skills`），也可以将仓库克隆到该目录下。Codex 通常会自动发现新安装的 skill；如果没有显示，重启 Codex。安装位置和发现方式可参阅 [OpenAI 的 skill 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

在请求中明确调用 skill，例如：

```text
$workflow-figure-ppt 请把这张横向阅读的手绘生信流程图做成单页可编辑 PPTX。
保留正常细胞与癌细胞的区别，并核对向量、矩阵和时间点的记号。
```

也可以直接描述科研流程和期望的图形结构。skill 的完整规则见 [SKILL.md](SKILL.md)；视觉与版式细节见 [references](references)。

## 可选：审核已有 PPTX

审核脚本使用 Python 3 标准库：

```bash
python scripts/audit_pptx.py path/to/figure.pptx
```

如需检查重复元素的尺寸、对齐或连接关系，可按 [验证说明](references/validation.md) 提供任务专用的 `figure-spec.json`。自动审核不能代替 PowerPoint 中的视觉检查和科学含义核对。
