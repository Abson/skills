# Claude Code Skills

A collection of custom [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills that extend Claude's capabilities for everyday tasks.

## What are Skills?

Skills are reusable prompt-and-script bundles that teach Claude Code new abilities. Each skill lives in its own folder with a `SKILL.md` (the instruction set) and supporting scripts/references. Once installed, skills activate automatically when Claude detects a matching user intent — no slash command needed.

## Available Skills

| Skill | Description | Trigger Examples |
|-------|-------------|-----------------|
| [stock-diglett](./stock-diglett/) | Fetch real market data and generate structured stock analysis reports with price charts, fundamentals, event timelines, and buy/sell insights. | `analyze AAPL`, `TSLA fundamentals`, `should I buy GOOGL?`, `NFLX最近走势` |

## Installation

### Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/Abson/skills.git

# 2. Copy the skill(s) you want into your Claude Code skills directory
cp -r skills/stock-diglett ~/.claude/skills/stock-diglett

# 3. Install any skill-specific dependencies (see each skill's README)
```

### Directory Structure

```
~/.claude/skills/
└── stock-diglett/
    ├── SKILL.md                  # Skill definition (auto-loaded by Claude Code)
    ├── scripts/                  # Python scripts for data fetching & rendering
    └── references/               # Benchmark guides and reference materials
```

## Updating Skills

```bash
# Pull the latest changes
cd /path/to/skills
git pull

# Re-copy to your Claude Code skills directory
cp -r stock-diglett ~/.claude/skills/stock-diglett
```

## Contributing

Want to add a new skill? Each skill folder should contain:

1. **`SKILL.md`** — YAML frontmatter (`name`, `description`) + detailed instructions for Claude
2. **`README.md`** — Human-readable docs: what it does, how to install, example output
3. **`scripts/`** — Any helper scripts the skill relies on
4. **`references/`** — Optional reference materials (benchmarks, guides, templates)

## License

MIT
