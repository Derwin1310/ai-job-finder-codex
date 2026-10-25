# Codex usage and runtime map

Start with README.md. Open the folder in Codex Desktop or launch `codex` from the
repository root. Nothing needs to be copied into your global Codex directory.
No Claude Code, Gemini CLI, Anthropic account, or custom model pin is required.
The optional original Claude workflow remains in .claude/ as shared source.

## Install requirements

- Codex configured with your own account.
- Python 3.10+; install requirements.txt in a virtual environment.
- Bun for the Computrabajo and LinkedIn CLIs.
- For stock PDF output: LuaLaTeX for CVs, XeLaTeX for letters, and the packages
  listed under minimal TeX installation in SETUP.md. pypdf extracts/checks text;
  Poppler pdftoppm (or another available renderer) supports visual page inspection.
- Web tools/network for current jobs and company research.

`python3 tools/lint_skills.py` and `python3 tools/security_guards.py` validate the
repo guidance and manifests; they do not prove live job access or PDF quality.

## Private workspace before onboarding

The public repo is for sharing reusable instructions. A personal profile can
modify tracked files even though documents, generated CVs and trackers are ignored.
Keep changes local, or create an empty private GitHub repository, then point your
working checkout there before pushing anything personal. For example, after
creating YOUR_ACCOUNT/my-private-job-search as an empty **private** repository:

```sh
git remote rename origin template
git remote add origin https://github.com/YOUR_ACCOUNT/my-private-job-search.git
git remote -v
# Verify the destination is private before your first personal push.
```

Keep the public template remote only for reviewing framework updates. No script
here pushes your profile. If you fork publicly to contribute, publish generic
framework changes only. The public-template check deliberately rejects a
personalized candidate profile.

## Workflow

1. Import career sources with `$job-search-setup`. Choose target roles, levels,
   geography, languages, CV language and work arrangements. No city, degree,
   work permit, seniority, salary or tool experience is inferred from defaults.
2. Search with `$job-scraper`. Default sources: Computrabajo Colombia, LinkedIn
   and Get on Board. Select other portals explicitly if needed.
3. Check `$job-history` before presenting or registering a new job. Discovery
   and application sources are separate; the readable history joins them.
4. Rank with `$job-search-rank` or evaluate a URL with `$job-search-apply`.
5. Prepare only the requested documents. Compile, extract and inspect PDFs;
   never claim unverified drafts are ready. Review factual claims against the
   actual profile, not other tailored CVs.
6. A CV-only request creates a drafted row with no letter. No application is
   sent automatically. Record applied only when the user confirms submission.
7. Use `$job-search-outcome` and `$job-search-interview` as the process advances.

## How adapters work

Codex entry points are small SKILL.md files in .agents/skills/. They point to
canonical .claude/commands or .claude/skills specifications. AGENTS.md translates
runtime-specific tools, paths and invocation semantics without copying a user's
profile into the skill itself. Treat .claude/settings.json permissions and model
names as source-runtime metadata, not Codex permission settings.

When a canonical workflow requests a reviewer, use Codex's available subagent
capability. If unavailable, disclose that and perform a separate self-review;
never claim it was independent. Optional Gmail and Notion skills need connectors
configured by the user. Reset retains the source workflow's explicit RESET gate.

## Search behavior and limitations

Computrabajo is Colombia-only and page-1-only. LinkedIn needs an explicit location.
Read exact flags from each portal skill rather than guessing. Get on Board uses
web tools and public category/detail pages. A CLI error does not prove no jobs
exist; label search-index fallback results and check publication dates. Inspect
remote residence rules. Keep request volumes small and avoid login/access bypass.

## Development

Run the commands in README.md. Changes to reusable tools need meaningful tests;
job_history.py tests cover URL variants, company/title matching, draft/submission
separation, read-only export and CSV text handling. The PDF examples are blank
upstream templates until personalized. Follow UPSTREAM.md to review upstream
methodology changes without overwriting your own data.
