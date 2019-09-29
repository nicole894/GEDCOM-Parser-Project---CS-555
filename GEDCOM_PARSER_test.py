import unittest
import GEDCOM_Parser_Sprint1_v1
from prettytable import PrettyTable
import inspect
from GEDCOM_Parser_Sprint1_v1 import Parser, check_before_today, birth_before_death,birth_inlast_30days,death_inlast_30days

class TestUserStories(unittest.TestCase):

    print = Parser()
    indi, fam = print.main()
    print.print_dicts(indi,fam)

    def test_US01(self):
        """Tests if the date from the dictionary is before today's date"""

        for id, records in self.indi.items():
            with self.subTest(id=id):
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')

                self.assertTrue(check_before_today(birth_date1))
                if death_date1 is not None:
                    self.assertTrue(check_before_today(death_date1))

        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                self.assertTrue(check_before_today(marr_date1))
                if div_date1 is not None:
                    self.assertTrue(check_before_today(div_date1))

    def test_US02(self):
        user_story = inspect.stack()[0][3].replace('test_','')
        #state = []
        for id, record in self.indi.items():
            with self.subTest(id=id):
                birth = record.get('BIRT')
                death = record.get('DEAT')
                out = birth_before_death(birth, death)
                self.assertTrue(out)


    def test_US21(self):
        ids = sorted(list(set([self.fam[i]['HUSB'] for i in self.fam.keys()])))
        for hid in ids:
            with self.subTest(hid=hid):
                self.assertEqual(self.indi[hid]['SEX'], 'M')
        ids = sorted(list(set([self.fam[i]['WIFE'] for i in self.fam.keys()])))
        for wid in ids:
            with self.subTest(wid=wid):
                self.assertEqual(self.indi[wid]['SEX'], 'F')

    def test_US35(self):
        """List birthdays in last 30 days"""
        x = PrettyTable(["ID","Name","Birthday"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                birth = record.get('BIRT')
                name = record.get('NAME')
                check_birth = birth_inlast_30days(birth)
                if check_birth is True:
                    x.add_row([id,name,birth])
        print(x)       
                    

    def test_US36(self):
        """List death date in last 30 days"""
        x = PrettyTable(["ID","Name","Death"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                death = record.get('DEAT')
                name = record.get('NAME')
                check_death = death_inlast_30days(death)
                if check_death is True:
                    x.add_row([id,name,death])
        print(x)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
