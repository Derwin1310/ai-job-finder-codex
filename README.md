<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the original AI Job Search mascot" width="160">
</p>

# AI Job Finder for Codex

A local job-search workspace for **Codex**: import your CV, find relevant jobs,
compare requirements, prepare tailored CVs and track applications without
repeated discoveries. No Claude Code or Anthropic API account is required for
the Codex workflow.

Adapted from **[MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search)**,
originally built for Claude Code. This adaptation reuses its methodology and
adds Codex entry points, runtime guidance, Get on Board search, and a persistent
job-history skill. It was based on the
[Computrabajo branch in oscarbol09/ai-job-search](https://github.com/oscarbol09/ai-job-search/tree/feature/computrabajo-search).
The original MIT license is retained. See [provenance](UPSTREAM.md).

## Start here

**Before onboarding:** setup writes personal data into some tracked template
files. Keep your personal workspace local or use a private repository; do not
push a filled-in candidate profile to this public template. See [privacy](#keep-personal-data-private).

You need Codex (desktop or CLI), Python 3.10+, and Bun for portal searches.
For CV PDF generation with the stock templates, also install LuaLaTeX and
XeLaTeX with the packages described in [the upstream setup guide](SETUP.md).
Browsing requires Codex web tools and network access. Searches can run before
installing TeX; generating verified PDFs cannot.

```sh
git clone https://github.com/Derwin1310/ai-job-finder-codex.git
cd ai-job-finder-codex
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.
Both default portal CLIs have no runtime dependencies. To run their development
checks, install packages inside each CLI:

```sh
cd .agents/skills/computrabajo-search/cli
bun install
cd ../../linkedin-search/cli
bun install
cd ../../../..
```

Open the repository folder as a project in the Codex desktop app, or run
`codex` from the root after installing/configuring Codex. The project guidance
is in [AGENTS.md](AGENTS.md), and skills live in `.agents/skills/`.
See the [official Codex customization documentation](https://learn.chatgpt.com/docs/customization/overview).

## Your first session

Put your source CV under `documents/cv/` and tell Codex:

> Use `$job-search-setup` to import my CV. Ask about my target roles, seniority,
> location, work arrangements, languages and CV language. Do not invent missing data.

Then use natural language or the explicit skills:

| Task | Skill / example |
| --- | --- |
| Find jobs | `$job-scraper` — search using my saved profile and preferences |
| Prioritize results | `$job-search-rank` |
| Prepare an application | `$job-search-apply` followed by a posting URL or full text |
| Prepare only a CV | Ask for a CV only; it is recorded as prepared, not submitted |
| Check previous jobs | `$job-history` |
| Record submission/results | `$job-search-outcome` — say which job and the actual date |
| Prepare an interview | `$job-search-interview` |
| View the pipeline | `$job-search-html-report` |

The original `/setup`, `/scrape`, `/apply` labels describe Claude workflows.
In Codex use the skills above or natural language. No global skill installation
or custom MCP server is required for the core local workflow. Gmail and Notion
are optional integrations requiring their own connections.

## Included sources

- **Computrabajo Colombia:** Bun CLI, public listings, page 1 only. Geographic
  and recency filters are applied to returned data where no CLI flag exists.
- **LinkedIn:** Bun CLI for public listings, explicit location and documented
  recency/work-arrangement filters.
- **Get on Board:** Codex web search and direct public posting pages, including
  salary and remote-residence checks. No Get on Board CLI is claimed.

Other supplied portals are kept as disabled examples. Enable only those needed
for your market. Public access may be blocked or rate-limited; keep requests
small and follow each portal's documented access/usage restrictions. A remote
label does not necessarily permit working from any country.

## History and no duplicate applications

- `job_scraper/seen_jobs.json` stores discoveries, including skipped/expired jobs.
- `job_search_tracker.csv` records prepared and submitted applications.
- `job_scraper/history.md` and `history.csv` are regenerable views of both.
- `$job-history` checks URLs/job IDs and company/role before presenting a new job.

```sh
python3 tools/job_history.py check --url 'https://www.linkedin.com/jobs/view/123456'
python3 tools/job_history.py render
```

`drafted` means documents are prepared. `applied` means submission was confirmed.
Generating a CV does not submit anything. Reapplications remain explicit choices,
and old records are preserved. Title variants may need human review.

## Keep personal data private

This public repository contains **empty templates only**. It contains no real
candidate CV, contact details, employment profile, applications or search history.
The generated folders and state are ignored, but setup also personalizes tracked
files such as `CLAUDE.md`, profile references and `cv/main_example.tex`.
**Ignoring a file does not protect an already tracked file.**

For a personal search, either keep all changes local without pushing, or create
a separate **private repository** and use that as `origin`. Public forks are for
contributing framework changes, not for uploading your personal profile.
The detailed private-workspace recipe is in [CODEX.md](CODEX.md). Never put career
records in public issues or PRs.

Before publishing template changes run `python3 tools/check_public_template.py`.
It checks placeholder integrity and excluded paths; it is a guard, not a secret
scanner or a guarantee that arbitrary text contains no private information.

## Development

```sh
python3 tools/lint_skills.py
python3 tools/security_guards.py
python3 -m unittest discover -s tests -t .
python3 tools/check_public_template.py
```

For a portal CLI, run `bun test` and `bun run typecheck` in its `cli/` directory.
CI runs fixture/mock tests, not live job searches. Requirements for each workflow
and the runtime mappings are in [CODEX.md](CODEX.md).

## Attribution

The core profile, evaluation, CV, interview and outcome workflows were created
by [Mads Lorentzen](https://github.com/MadsLorentzen/ai-job-search). Colombian portal
work was taken from [oscarbol09's branch](https://github.com/oscarbol09/ai-job-search/tree/feature/computrabajo-search).
This repository is an independent Codex adaptation, not an official OpenAI or
Anthropic project. Original documentation is preserved in
[README_UPSTREAM.md](README_UPSTREAM.md). License: [MIT](LICENSE).

## Contributing through a fork

### 1. Fork and clone

For generic framework contributions only:

```sh
gh repo fork Derwin1310/ai-job-finder-codex --clone
```

A fork of this public template is public. Setup writes personal data into tracked
files, so use a separate private repository for your own search. See the private
workspace recipe in [CODEX.md](CODEX.md) and [SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork).
