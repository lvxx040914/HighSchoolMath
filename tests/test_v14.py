import copy
import unittest
from pathlib import Path
import yaml
from tools.validate_review import validate_review
from tools.compose import select_questions

ROOT=Path(__file__).resolve().parents[1]

class V14ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=yaml.safe_load((ROOT/'review/v1_4_audit.yml').read_text(encoding='utf8'))

    def test_40_prechecks_with_no_promotion(self):
        errors,n=validate_review()
        self.assertEqual(errors,[])
        self.assertEqual(n,40)
        self.assertTrue(all(e['human_review_required'] for e in self.audit['entries']))
        for e in self.audit['entries']:
            data=yaml.safe_load((ROOT/'questions'/e['id']/'metadata.yml').read_text(encoding='utf8'))
            self.assertEqual(data['review_status'],'draft')

    def test_precheck_invalidated_after_edit(self):
        bad=copy.deepcopy(self.audit)
        bad['entries'][0]['content_sha256']['stem.tex']='0'*64
        errors,_=validate_review(data=bad)
        self.assertTrue(any('stale audit' in e for e in errors))

    def test_unknown_equivalence_target_rejected(self):
        bad=copy.deepcopy(self.audit)
        bad['canonical_equivalence_groups'][0]['members'].append('HSM-FUN-9999')
        errors,_=validate_review(data=bad)
        self.assertTrue(any('unknown equivalence' in e for e in errors))

    def test_no_duplicated_equivalent_in_selected_sheet(self):
        selected=select_questions(count=27,seed=37,avoid_equivalent=True)
        self.assertEqual(len(selected),27)
        self.assertEqual(len(set(selected)),27)
        self.assertIn('HSM-FUN-0006',selected)
        self.assertIn('HSM-FUN-0007',selected)
        for blocked in ('HSM-FUN-0014','HSM-FUN-0028','HSM-FUN-0029'):
            self.assertNotIn(blocked,selected)

    def test_equivalent_filter_rejects_impossible_count(self):
        with self.assertRaises(ValueError):
            select_questions(count=29,avoid_equivalent=True)

    def test_solution_independent_of_lecture_numbering(self):
        solution=(ROOT/'questions/HSM-FUN-0040/solution.tex').read_text(encoding='utf8')
        self.assertNotIn('由例题',solution)
        self.assertIn('F\'(x)=3(x+1)(x-1)',solution)

if __name__=='__main__':unittest.main()
