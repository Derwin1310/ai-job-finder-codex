import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('history', Path(__file__).resolve().parents[1] / 'tools/job_history.py')
history = importlib.util.module_from_spec(spec)
spec.loader.exec_module(history)

class HistoryTest(unittest.TestCase):
    def test_linkedin_same_job_across_hosts_slugs_and_tracking(self):
        a = 'https://co.linkedin.com/jobs/view/developer-123456?trackingId=x'
        b = 'https://www.linkedin.com/jobs/view/123456/'
        self.assertEqual(history.identity(a), history.identity(b))
        self.assertNotEqual(history.identity(a), history.identity('https://www.linkedin.com/jobs/view/999999'))

    def test_getonboard_language_variants_and_company_normalization(self):
        a = 'https://www.getonbrd.com/jobs/programming/full-stack-company-remote'
        b = 'https://getonbrd.com/empleos/programacion/full-stack-company-remote?ref=x'
        self.assertEqual(history.identity(a), history.identity(b))
        rows = [{'company':'Tecnología S.A.S.', 'title':'Front-end Developer', 'url':a}]
        self.assertEqual(len(history.find_matches(rows, company='TECNOLOGIA SAS', role='Frontend Developer')), 1)
        self.assertFalse(history.find_matches(rows, company='Different company', role='Frontend Developer'))

    def test_csv_export_neutralizes_formula_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            history.export_history([{'company':'Example', 'title':'=HYPERLINK("https://example.com")'}],root)
            with (root/'history.csv').open(encoding='utf-8-sig') as stream:
                row=next(csv.DictReader(stream))
            self.assertTrue(row['title'].startswith("'="))

    def test_merge_drafts_does_not_claim_submission_and_render_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);state = root/'state.json';tracker=root/'tracker.csv'
            state.write_text(json.dumps({'seen':{'u':{'url':'https://www.linkedin.com/jobs/view/test-123', 'title':'Developer', 'company':'Example', 'status':'new', 'first_seen':'2026-10-24'}}}))
            with tracker.open('w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=['date','company','role','status','source','cv_file']);writer.writeheader()
                writer.writerow({'date':'2026-10-24','company':'Example','role':'Developer','status':'drafted','source':'https://co.linkedin.com/jobs/view/123','cv_file':'cv/test.pdf'})
            before=(state.read_bytes(),tracker.read_bytes())
            records=history.load_records(state,tracker)
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]['application_status'],'drafted')
            self.assertEqual(len(history.find_matches(records,url='https://linkedin.com/jobs/view/123')),1)
            history.export_history(records,root/'out')
            self.assertEqual(before,(state.read_bytes(),tracker.read_bytes()))
            with (root/'out/history.csv').open(encoding='utf-8-sig') as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(rows[0]['application_status'],'drafted')

if __name__=='__main__':unittest.main()
