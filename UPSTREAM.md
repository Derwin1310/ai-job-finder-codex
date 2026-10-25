# Origin and attribution

- Original project: https://github.com/MadsLorentzen/ai-job-search
- Source branch for this snapshot: https://github.com/oscarbol09/ai-job-search/tree/feature/computrabajo-search
- Source revision: `de016b5af7dc6bea45fcee5b205af03d5330857c`
- License: MIT, original copyright notice preserved in LICENSE.

This is an independent source snapshot plus Codex adapters, not a claim of
original authorship of the framework or the Colombian portal integrations.
The public repository starts with a clean snapshot so it contains no private
workspace history. README_UPSTREAM.md preserves the source README.

Codex additions: root runtime guidance, portable workflow adapters,
Get on Board web-source guidance, job-history checking/export, tests, and a
clean-public-template validation step. Original CLI implementations, fixtures,
methodology, fonts and templates are retained unless documented otherwise.

To review later updates, add an upstream remote and inspect changes before
merging or porting. Public framework updates and private candidate data must stay
separate. The inherited upstream-watch workflow is manual-only in this adaptation
so cloning/publishing does not silently enable scheduled issue creation.

Adaptation-specific test changes: CLI contracts discover actual CLI directories
so web-only sources are not mistaken for missing implementations; reset coverage
uses the template's .gitkeep markers so it can also run on an uncommitted source
export. The README retains the source mascot and adjacent fork/privacy warning.
