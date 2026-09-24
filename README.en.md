# Scientific Workflow Figure PPT

[简体中文](README.md) · **English**

A **Codex skill** for creating or revising **single-slide, editable PowerPoint scientific workflow figures** from prose, hand-drawn sketches, or reference images. It is intended for research workflows, analysis pipelines, conceptual frameworks, and model architecture diagrams.

## Highlights

- Uses native PowerPoint shapes, text, and connectors so individual elements remain editable.
- Identifies entities, hierarchy, and relationships before layout; reads rotated sketches in the direction specified by the user.
- Checks mathematical symbols, subscripts, superscripts, and vector/matrix dimensions and orientation.
- Uses color and meaningful, closely labeled schematic icons without adding filler elements.
- Reviews text, composition, and routes; directional connectors usually leave a small visible gap from objects.
- Includes a PPTX audit script for structural and optional task-specific semantic checks.

This repository contains workflow instructions and audit scripts. It **does not bundle PowerPoint or a standalone PPT generator**. Codex still needs an available presentation authoring and rendering toolchain to create PPTX files.

## Installation

### Option 1: Install from Codex

Enter this in Codex:

```text
$skill-installer Install the skill from the root of Quzhongk/workflow-figure-ppt on GitHub (path: .), using the name workflow-figure-ppt.
```

### Option 2: Clone manually

Install Git first. Clone the repository into your personal skills directory so that `SKILL.md` sits inside the `workflow-figure-ppt` folder.

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

If your Codex setup uses `$CODEX_HOME/skills` (typically `~/.codex/skills`), you can clone the repository there instead. Codex normally discovers newly installed skills automatically; restart Codex if the skill does not appear. See the [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) for skill locations and discovery.

## Usage

Invoke the skill explicitly in your request, for example:

```text
$workflow-figure-ppt Turn this hand-drawn bioinformatics workflow, read horizontally,
into a single-slide editable PPTX. Distinguish normal and cancer cells, and check
the vector, matrix, and time-point notation.
```

You can also describe the research process and desired figure structure directly. See [SKILL.md](SKILL.md) for the full workflow and [references](references) for visual and layout guidance.

## Optional: Audit an existing PPTX

The audit script uses the Python 3 standard library:

```bash
python scripts/audit_pptx.py path/to/figure.pptx
```

For repeated dimensions, alignment, or connection checks, provide a task-specific `figure-spec.json` as described in the [validation guide](references/validation.md). Automated checks do not replace visual inspection in PowerPoint or review of the scientific meaning.
