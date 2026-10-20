import unittest
from pathlib import Path
import yaml
from tools.compose import select_questions
from tools.validate import validate

ROOT=Path(__file__).resolve().parents[1]

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.config=yaml.safe_load((ROOT/'config/monotonicity.yml').read_text(encoding='utf8'))

    def test_40_separate_items_and_answers(self):
        ids=self.config['question_ids']+self.config['worked_ids']
        self.assertEqual(len(ids),40)
        self.assertEqual(len(set(ids)),40)
        for qid in ids:
            self.assertTrue((ROOT/'questions'/qid/'answer.tex').read_text(encoding='utf8').strip())

    def test_all_six_manual_examples_migrated(self):
        source=(ROOT/'lectures/functions/monotonicity.tex').read_text(encoding='utf8')
        self.assertNotIn('\\begin{examplebox}',source)
        for n in range(35,41):
            self.assertIn('HSM-FUN-%04d'%n,source)
            qid='HSM-FUN-%04d'%n
            meta=yaml.safe_load((ROOT/'questions'/qid/'metadata.yml').read_text(encoding='utf8'))
            self.assertEqual(meta['review_status'],'draft')
            self.assertTrue(meta['archetypes'])

    def test_selection_reproducible_and_tagged(self):
        kwargs=dict(topic='K-FUN-MONO',min_difficulty=2,max_difficulty=4,count=4,seed=17)
        picked=select_questions(**kwargs)
        self.assertEqual(picked,select_questions(**kwargs))
        self.assertEqual(len(set(picked)),4)
        for qid in picked:
            item=yaml.safe_load((ROOT/'questions'/qid/'metadata.yml').read_text(encoding='utf8'))
            self.assertIn('K-FUN-MONO',item['topics'])
            self.assertLessEqual(item['difficulty'],4)

    def test_selection_errors_instead_of_silent_underfill(self):
        with self.assertRaises(ValueError):
            select_questions(count=1000)
        with self.assertRaises(ValueError):
            select_questions(count=2,min_difficulty=5,max_difficulty=2)

    def test_generated_workbook_and_answer_order(self):
        files={'workbook_questions.tex':'showworkbookquestion','short_answers.tex':'showshortanswer'}
        for name, command in files.items():
            data=(ROOT/'tex/generated'/name).read_text(encoding='utf8')
            self.assertEqual(data.count('\\'+command+'{'),30)
            for qid in self.config['question_ids']:
                self.assertIn(qid,data)

    def test_question_bank_still_valid(self):
        self.assertEqual(validate()[0],[])

if __name__=='__main__':unittest.main()
