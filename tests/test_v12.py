import unittest
from pathlib import Path
import yaml
from tools.validate import validate

ROOT = Path(__file__).resolve().parents[1]

class V12ContentTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load((ROOT / 'config/monotonicity.yml').read_text(encoding='utf-8'))

    def test_unique_problem_ids_after_example_migration(self):
        ids = self.data['worked_ids'] + self.data['question_ids']
        self.assertEqual(len(ids), 40)
        self.assertEqual(len(set(ids)), 40)
        self.assertEqual((len(self.data['worked_ids']), len(self.data['question_ids'])), (10, 30))

    def test_all_new_items_are_draft_and_tagged(self):
        for num in range(11, 35):
            qid = f'HSM-FUN-{num:04d}'
            folder = ROOT / 'questions' / qid
            meta = yaml.safe_load((folder / 'metadata.yml').read_text(encoding='utf-8'))
            self.assertEqual(meta['review_status'], 'draft')
            self.assertTrue(meta['archetypes'])
            self.assertTrue((folder / 'stem.tex').read_text(encoding='utf-8').strip())
            self.assertTrue((folder / 'solution.tex').read_text(encoding='utf-8').strip())

    def test_worked_are_externally_referenced(self):
        lecture = (ROOT/'lectures/functions/monotonicity.tex').read_text(encoding='utf-8')
        for qid in self.data['worked_ids']:
            self.assertIn('{' + qid + '}', lecture)

    def test_generated_indexes_match_training(self):
        qtex = (ROOT/'tex/generated/questions.tex').read_text(encoding='utf-8')
        stex = (ROOT/'tex/generated/solutions.tex').read_text(encoding='utf-8')
        for qid in self.data['question_ids']:
            self.assertIn('\\showquestion{' + qid + '}', qtex)
            self.assertIn('\\showanswer{' + qid + '}', stex)
        for qid in self.data['worked_ids']:
            self.assertNotIn('\\showquestion{' + qid + '}', qtex)
            self.assertNotIn('\\showanswer{' + qid + '}', stex)

    def test_main_schema_validation(self):
        errors, count = validate()
        self.assertEqual(errors, [])
        self.assertEqual(count, 40)
