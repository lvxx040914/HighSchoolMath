"""Coverage, reference and deliberate-failure tests for the V1.1 catalogs."""
import tempfile
import unittest
from pathlib import Path
from shutil import copytree
import yaml
from tools.validate_catalog import ROOT, validate_catalog


class CatalogTest(unittest.TestCase):
    def test_catalog_and_legacy_links(self):
        errors, counts = validate_catalog()
        self.assertEqual(errors, [])
        self.assertEqual(counts['domains'], 11)
        self.assertGreaterEqual(counts['topics'], 90)
        self.assertGreaterEqual(counts['methods'], 40)
        self.assertGreaterEqual(counts['archetypes'], 50)
        self.assertEqual(counts['mapped_questions'], 34)

    def _snapshot(self, folder):
        root = Path(folder)
        for name in ('catalog', 'knowledge', 'methods', 'questions'):
            copytree(ROOT/name, root/name)
        return root

    def test_unknown_topic_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self._snapshot(folder)
            path=root/'catalog/methods.yml'
            data=yaml.safe_load(path.read_text(encoding='utf-8'))
            data['methods'][0]['related_topics'].append('T-XYZ-99')
            path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
            errors,_ = validate_catalog(root)
            self.assertTrue(any('unknown topic T-XYZ-99' in x for x in errors))

    def test_prerequisite_cycle_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self._snapshot(folder)
            path=root/'catalog/knowledge_map.yml'
            data=yaml.safe_load(path.read_text(encoding='utf-8'))
            data['domains'][0]['topics'][0]['prerequisites'].append('T-PRE-02')
            path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
            errors,_=validate_catalog(root)
            self.assertTrue(any('prerequisite cycle' in x for x in errors))

    def test_archetype_unmapped_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self._snapshot(folder)
            path=root/'questions/HSM-FUN-0001/metadata.yml'
            data=yaml.safe_load(path.read_text(encoding='utf-8'))
            data['archetypes']=['A-NOT-99']
            path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
            errors,_=validate_catalog(root)
            self.assertTrue(any('unknown archetype A-NOT-99' in x for x in errors))


if __name__=='__main__':
    unittest.main()
