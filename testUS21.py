import unittest
from out import indi, fam

class TestCorrectGender(unittest.TestCase):
    def test_husb_M(self):
        ids = sorted(list(set([fam[i]['HUSB'] for i in fam.keys()])))
        for hid in ids:
            with self.subTest(hid=hid):
                self.assertEqual(indi[hid]['SEX'], 'M')
        ids = sorted(list(set([fam[i]['WIFE'] for i in fam.keys()])))
        for wid in ids:
            with self.subTest(wid=wid):
                self.assertEqual(indi[wid]['SEX'], 'F')


if __name__ == '__main__':
    unittest.main(exit=False)
