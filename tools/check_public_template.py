#!/usr/bin/env python3
"""Validate a public template snapshot, not a personalized working repository."""
from pathlib import Path
import subprocess
import os
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    'CLAUDE.md': '[YOUR_NAME]',
    '.claude/skills/job-application-assistant/01-candidate-profile.md': '[YOUR_EMAIL]',
    '.claude/skills/job-application-assistant/04-job-evaluation.md': '[YOUR_PRIMARY_SKILLS]',
    'cv/main_example.tex': '[First]',
    'cover_letters/cover_example.tex': '[YOUR NAME]',
}

def check(root, paths):
    errors = []
    for rel, token in REQUIRED.items():
        path = root / rel
        if not path.is_file() or token not in path.read_text(encoding='utf-8'):
            errors.append(f'{rel}: original placeholder missing; review for personal data')
    private_dirs = ('documents/cv/', 'documents/linkedin/', 'documents/diplomas/',
                    'documents/references/', 'documents/applications/', 'documents/postings/',
                    'company_research/', 'gmail_sync/', 'outputs/', 'work/', 'reports/')
    for rel in paths:
        path = Path(rel)
        if any(part in {'node_modules', '.venv', '__pycache__'} for part in path.parts):
            errors.append(f'{rel}: local dependency/cache included')
        if rel.startswith(private_dirs) and path.name not in {'README.md', '.gitkeep'}:
            errors.append(f'{rel}: private runtime/document path included')
        if rel.startswith('job_scraper/') and path.name not in {'README.md', '.gitkeep'}:
            errors.append(f'{rel}: search history included')
        if path.suffix.lower() in {'.pdf', '.zip'} or path.name in {'job_search_tracker.csv', 'salary_data.json', '.env'} or path.name.startswith('.env.'):
            errors.append(f'{rel}: generated or sensitive artifact included')
    return errors

def main():
    if (ROOT / '.git').exists():
        raw = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT)
        paths = raw.decode().split('\0')
    else:
        paths = []
        for base, directories, files in os.walk(ROOT):
            directories[:] = [d for d in directories if d not in {'.git', 'node_modules', '.venv', '__pycache__'}]
            paths.extend(str((Path(base) / name).relative_to(ROOT)) for name in files)
    errors = check(ROOT, [p for p in paths if p])
    if errors:
        print('\n'.join(errors))
        return 1
    print('Public template checks passed: placeholders intact; no tracked candidate/runtime artifacts.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
