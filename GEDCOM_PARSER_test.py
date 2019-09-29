import unittest
import GEDCOM_Parser_Sprint1_v1
from prettytable import PrettyTable
import inspect
from GEDCOM_Parser_Sprint1_v1 import Parser, check_before_today, birth_before_death,birth_inlast_30days,death_inlast_30days,reject_illegitimate_dates

class TestUserStories(unittest.TestCase):

    rint = Parser()
    indi, fam, log = rint.main()
    rint.print_dicts(indi,fam)
    log_func={
     ("US21","HUSB"): lambda x: f"FAMILY: {x[0]}: US21: Husband ({x[1]}) has incorrect gender",
     ("US21","WIFE"): lambda x: f"FAMILY: {x[0]}: US21: Wife ({x[1]}) has incorrect gender",
     ("US22","FAM"): lambda x: f"FAMILY: {x}: US22: Family already exists",
     ("US22","INDI"): lambda x: f"INDIVIDUAL: {x}: US22: Individual already exists"
     }
    for x in log:
        print("ERROR: %s" %(log_func[x[0],x[1]](x[2])))

    def test_US01(self):
        """Tests if the date from the dictionary is before today's date"""

        for id, records in self.indi.items():
            with self.subTest(id=id): 
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')

                if birth_date1 is not None:
                    self.assertTrue(check_before_today(birth_date1))
                if death_date1 is not None:
                    self.assertTrue(check_before_today(death_date1))

        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is not None:
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
        self.assertEqual(len([i for i in self.log if i[0]=='US21']),1,"Should have exactly 1 errors for US21.")
        #self.assertIn(['US21', 'HUSB', ['@F4@', '@I3@']], self.log, "Husband Test failed.")
        self.assertIn(['US21', 'WIFE', ['@F4@', '@I4@']], self.log, "Wife Test failed.")
        self.assertEqual(self.log_func['US21','HUSB'](['F1','I5']), \
            "FAMILY: F1: US21: Husband (I5) has incorrect gender", "log printing test.")

    def test_US22(self):
        self.assertEqual(len([i for i in self.log if i[0]=='US22']),1,"Should have exactly 1 errors for US22.")
        self.assertIn(['US22', 'INDI', '@I1@'], self.log, "Individual Test failed.")
        #self.assertIn(['US22', 'FAM', '@F3@'], self.log, "Family Test failed.")
        self.assertEqual(self.log_func['US22', 'INDI']('x'), "INDIVIDUAL: x: US22: Individual already exists")
        ik=self.indi.keys()
        fk=self.fam.keys()
        self.assertEqual(len(ik),len(set(ik)))
        self.assertEqual(len(fk),len(set(fk)))

    def test_US35(self):
        """List birthdays in last 30 days"""
        x = PrettyTable(["ID","Name","Birthday"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                birth = record.get('BIRT')
                name = record.get('NAME')
                if birth is not None:
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
        
    def test_US42(self):
        "Tests if the illegitimate dates are rejected"

        for id, records in self.indi.items():
            with self.subTest(id=id):
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')
                name = records.get('NAME')
                if birth_date1 is not None:
                    self.assertTrue(reject_illegitimate_dates(birth_date1))
                if death_date1 is not None:
                    self.assertTrue(reject_illegitimate_dates(death_date1))


        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is not None:
                    self.assertTrue(reject_illegitimate_dates(marr_date1))
                if div_date1 is not None:
                    self.assertTrue(reject_illegitimate_dates(div_date1))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
