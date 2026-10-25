---
name: job-history
description: Consulta y mantiene el historial de ofertas encontradas y candidaturas para evitar repetir vacantes y distinguir CV preparado de postulación enviada.
---

Read root AGENTS.md. Before presenting a job, check the canonical discovery state
`job_scraper/seen_jobs.json` and application tracker `job_search_tracker.csv`:

```sh
python3 tools/job_history.py check --url '<posting URL>' --company '<company>' --role '<role>'
```

The JSON `known: true` means do not present it as a new discovery. The helper
normalizes LinkedIn IDs, Computrabajo IDs, Get on Board slugs, URL tracking and
company/title punctuation. Compare requisition IDs and posting text when title
variants need judgment; do not silently merge genuinely different vacancies.
Existing jobs can be discussed again at the user's request; disclose their state.

New discoveries belong in seen_jobs.json using the canonical scraper schema.
Never delete old skipped/expired/rejected/applied records to reset deduplication.
Reuse tools/rank_state.py's atomic save_state when updating discovery state.
Preserve first_seen, original source and any rank fields. Match tracker rows by
company/role case-insensitively before updates. Preserve final applications and
append a separate row for an explicitly requested reapplication.

When the user requests CV-only preparation, register verified CVs in the canonical
tracker with status=drafted and an empty cover_letter_file; this does not imply
a cover letter or application was sent. Set applied and the actual submission
date only after user confirmation or direct submission evidence. Do not regress
an applied/interview/offer/final status when revising a CV. Store uncertain
requirements in notes; never imply full eligibility from document generation.
Use the existing outcome workflow for later status updates and final results.

Regenerate the readable list after state/tracker changes:

```sh
python3 tools/job_history.py render
```

This writes `job_scraper/history.csv` and `job_scraper/history.md` as derived views,
not new databases. They include all found and discarded jobs and application
state when present. The helper does not send anything or mutate either source.
