#!/usr/bin/env python3
"""Read-only dedup checks and human-readable views over existing job-search state."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

def normalized(value):
    value = unicodedata.normalize('NFKD', str(value or '')).casefold()
    return ''.join(c for c in value if c.isalnum() and not unicodedata.combining(c))

def identity(url):
    parts = urlsplit(str(url or ''))
    host = (parts.hostname or '').lower()
    path = unquote(parts.path).rstrip('/')
    if host == 'linkedin.com' or host.endswith('.linkedin.com'):
        match = re.search(r'/jobs/view/(?:.*-)?(\d+)$', path)
        if match:
            return 'linkedin:' + match.group(1)
    if host == 'computrabajo.com' or host.endswith('.computrabajo.com'):
        match = re.search(r'([a-fA-F0-9]{32})$', path)
        if match:
            return 'computrabajo:' + match.group(1).lower()
    if host == 'getonbrd.com' or host.endswith('.getonbrd.com'):
        if re.match(r'^/(jobs|empleos)/[^/]+/[^/]+$', path):
            return 'getonboard:' + path.rsplit('/', 1)[-1].casefold()
    return (host + path).casefold() if host else str(url or '').strip()

def load_records(state_path, tracker_path):
    records = {}
    if state_path.exists():
        data = json.loads(state_path.read_text(encoding='utf-8'))
        seen = data.get('seen', data)
        if not isinstance(seen, dict):
            raise ValueError('Job state must contain an object of entries')
        for key, entry in seen.items():
            url = entry.get('url') or key
            record = dict(entry)
            record.update(url=url, application_status='', cv_file='', cover_letter_file='')
            records[identity(url)] = record
    if tracker_path.exists():
        with tracker_path.open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                url = row.get('source') or ''
                pair = (normalized(row.get('company')), normalized(row.get('role')))
                key = identity(url) if url else ''
                if key not in records:
                    key = next((k for k, r in records.items() if pair[0] and pair == (normalized(r.get('company')), normalized(r.get('title')))), key)
                if not key:
                    key = 'company-role:' + ':'.join(pair)
                record = records.setdefault(key, {'company': row.get('company'), 'title': row.get('role'), 'url': url})
                # Keep one output row per application when a later reapplication exists.
                if record.get('application_status'):
                    key += ':' + str(row.get('date') or '') + ':' + str(len(records))
                    record = records.setdefault(key, dict(record))
                record.update(application_status=row.get('status', ''), tracker_date=row.get('date', ''),
                              cv_file=row.get('cv_file', ''), cover_letter_file=row.get('cover_letter_file', ''),
                              application_notes=row.get('notes', ''))
    return list(records.values())

def find_matches(records, url='', company='', role=''):
    key = identity(url) if url else None
    pair = (normalized(company), normalized(role))
    return [r for r in records if (key and key == identity(r.get('url'))) or
            (all(pair) and pair == (normalized(r.get('company')), normalized(r.get('title'))))]

def export_history(records, directory):
    directory.mkdir(parents=True, exist_ok=True)
    columns = ['company', 'title', 'url', 'first_seen', 'posted_date', 'status', 'application_status', 'tracker_date', 'portal', 'cv_file', 'fit_note', 'application_notes']
    with (directory / 'history.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        # Posting text must remain data when this CSV is opened in a spreadsheet.
        writer.writerows({k: ("'" + str(v) if str(v or '').lstrip().startswith(('=', '+', '-', '@')) else v)
                          for k, v in record.items()} for record in records)
    def cell(value):
        return str(value or '').replace('|', '\\|').replace('\n', ' ')
    lines = ['# Historial de ofertas', '', 'Fuentes de verdad: seen_jobs.json (descubrimiento) y job_search_tracker.csv (candidaturas).',
             'drafted = CV preparado, no enviado. applied = envío confirmado por el usuario. Esta vista se puede regenerar.', '',
             '| Empresa | Cargo | Estado búsqueda | Candidatura | CV | Oferta |', '| --- | --- | --- | --- | --- | --- |']
    for r in records:
        lines.append('| ' + ' | '.join(cell(r.get(k)) for k in ['company', 'title', 'status', 'application_status', 'cv_file', 'url']) + ' |')
    (directory / 'history.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, default=ROOT / 'job_scraper/seen_jobs.json')
    parser.add_argument('--tracker', type=Path, default=ROOT / 'job_search_tracker.csv')
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check')
    check.add_argument('--url', default='')
    check.add_argument('--company', default='')
    check.add_argument('--role', default='')
    render = commands.add_parser('render')
    render.add_argument('--output', type=Path, default=ROOT / 'job_scraper')
    args = parser.parse_args()
    try:
        records = load_records(args.state, args.tracker)
        if args.command == 'check':
            if not args.url and not (args.company and args.role):
                parser.error('check needs --url or both --company and --role')
            matches = find_matches(records, args.url, args.company, args.role)
            print(json.dumps({'known': bool(matches), 'matches': matches}, ensure_ascii=False, indent=2))
        else:
            export_history(records, args.output)
            print(json.dumps({'records': len(records), 'directory': str(args.output)}, ensure_ascii=False))
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__':
    main()
