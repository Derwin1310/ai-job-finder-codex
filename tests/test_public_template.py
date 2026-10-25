import importlib.util
import tempfile
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('public_template',Path(__file__).resolve().parents[1]/'tools/check_public_template.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class PublicTemplateTests(unittest.TestCase):
    def base(self,root):
        for rel,token in mod.REQUIRED.items():
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(token)
    def test_unpersonalized_sources_and_structure_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.base(root)
            self.assertEqual(mod.check(root,['README.md','documents/cv/.gitkeep','documents/cv/README.md']),[])
    def test_profile_and_runtime_data_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.base(root)
            (root/'CLAUDE.md').write_text('Personalized candidate')
            errors=mod.check(root,['documents/cv/resume.pdf','job_scraper/seen_jobs.json','job_search_tracker.csv','.env'])
            self.assertGreaterEqual(len(errors),5)

if __name__=='__main__':unittest.main()
