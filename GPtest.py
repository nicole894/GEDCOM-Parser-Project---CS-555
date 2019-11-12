import unittest
from prettytable import PrettyTable
import GDriver as D
from GDriver import us38_list_upcoming_birthdays, us39_list_upcoming_anniversary, us35_birth_inlast_30days, us36_death_inlast_30days, us29_list_of_deceased, us30_list_all_living_married_people, us31_living_single, us33_list_orphans, us17_no_marriages_to_children, us18_sibilings_should_not_marry,us32_list_multiple_births,us34_larger_age_difference
import GParser as P
D.today = '15 OCT 2019'

class TestUS(unittest.TestCase):
    __ALL__ = ["US01", "US02", "US03", "US21", "US22", "US35", "US36", "US42", "US04", "US05", "US07", "US08", "US09",
               "US10","US17","US18", "US38", "US39","US29","US30","US31","US23","US32","US34"]
    __INFO__ = ["US35", "US36", "US38", "US39","US29","US30","US31","US23","US32","US34"]
    _path = 'GEDCOM_File_withErrors.ged'
    p = D.main(_path)

    def run_test(self, _test):
        x = None
        logs = [i for i in self.p.log if i[0] == _test]
        count = len(logs)
        if _test in self.__INFO__:
            # if count==1:
            #     print(f"{_test} Output: \n{logs[0][2][0]}")
            self.assertEqual(count, 1, f"{_test}: This test should always generate an INFO.")
        else:
            if count:
                x = PrettyTable(["Test", "Case", "Spec"])
                for i in self.p.log:
                    if i[0] == _test:
                        x.add_row(i)
            self.assertEqual(count, 0, f"{_test}: There is {count} error found in GEDCOM file:\n{x}")

    def test_US01(self):
        expected_id = ['@I2@','@I6@', '@I9@','@F1@', '@F2@', '@F3@'];
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US01']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)
        
    def test_US02(self):
        expected_id = ['@F1@', '@F2@', '@F3@', '@F6@','@F6@', '@F8@', '@F9@'];
        generated_id =[]
        log = [i for i in self.p.log if i[0] == 'US02']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)
        
    def test_US03(self):
        expected_id = ['@I6@', '@I9@']
        generated_id =[]
        log = [i for i in self.p.log if i[0] == 'US03']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US21(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0] == 'US21']
            self.assertIn(['US21', 'WIFE', ['@F4@', '@I4@']], logs)
        else:
            self.run_test('US21')

    def test_US22(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0] == 'US22']
            self.assertIn(['US22', 'INDI', ['@I1@']], logs)
        else:
            self.run_test('US22')

    def test_US35(self):
        expected_id = ['@I23@']
        q = P.Parser()
        
        fix_date = D.today
        generated_id = us35_birth_inlast_30days(q, fix_date)
        self.assertEqual(expected_id, generated_id)
        
    def test_US36(self):
        expected_id = ['@I9@']
        q = P.Parser()
        
        fix_date = D.today 
        generated_id = us36_death_inlast_30days(q, fix_date)
        self.assertEqual(expected_id, generated_id)

    def test_US29(self):
        expected_id = ['@I9@','@I18@','@I24@', '@I25@', '@I26@', '@I45@', '@I46@']
        q = P.Parser()
        
        generated_id = us29_list_of_deceased(q)
        self.assertEqual(expected_id, generated_id)

    def test_US30(self):
        expected_id = ['@I1@','@I2@','@I3@', '@I4@', '@I5@','@I6@','@I8@','@I14@', '@I15@', '@I16@','@I17@','@I19@','@I20@', '@I21@', '@I22@','@I44@']
        q = P.Parser()
        
        generated_id = us30_list_all_living_married_people(q)
        self.assertEqual(expected_id, generated_id)

    def test_US42(self):
        expected_id = ['@I6@','@I19@','@F1@']
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US42']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)
        
    def test_US04(self):
        expected_id = ['@F3@']
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US04']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US05(self):
         expected_id = ['@F7@']
         generated_id = []
         log = [i for i in self.p.log if i[0] == 'US05']
         for record in log:
             a = record[2];
             generated_id.append(a[0])
         self.assertEqual(expected_id, generated_id)

    def test_US07(self):
        expected_id = ['@I1@']
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US07']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US08(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0] == 'US08']
            self.assertIn(['US08', 'BBPM', ['@F3@', '2020-02-14', '@I10@', '2002-04-04']], logs)
        else:
            self.run_test('US08')

    def test_US09(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0] == 'US09']
            self.assertIn(['US09', 'WIFE', ['@F7@', '@I18@', '1954-12-20', '@I8@', '10 MAY 1969']], logs)
        else:
            self.run_test('US09')
        
    def test_US10(self):
        expected_id = ['@F10@']
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US10']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US12(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0]=='US12']
            self.assertIn(['US12', 'HUSB', ['@F1@', '@I1@', '1703-01-02', '@I7@', '2013-01-16']], logs)
            self.assertIn(['US12', 'HUSB', ['@F2@', '@I1@', '1703-01-02', '@I3@', '1975-08-09']], logs)
            self.assertIn(['US12', 'HUSB', ['@F2@', '@I1@', '1703-01-02', '@I5@', '1969-11-11']], logs)
        else:
            self.run_test('US12')

    def test_US13(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0]=='US13']
            self.assertIn(['US13', 'SPAC', ['@F6@', '@I13@', '2002-11-28', '@I14@', '2002-12-10']], logs)
        else:
            self.run_test('US13')

    def test_US38(self):
        
        expected_id = ['@I5@', '@I21@', '@I36@']
        q = P.Parser()
       
        fix_date = D.today 
        generated_id = us38_list_upcoming_birthdays(q, fix_date)
        self.assertEqual(expected_id, generated_id)
       
    def test_US39(self):
        expected_id = ['@F9@']
        q = P.Parser()
        fix_date = D.today 
        generated_id = us39_list_upcoming_anniversary(q, fix_date)
        self.assertEqual(expected_id, generated_id)

    def test_US06(self):
        expected_id = ['@F2@', '@F11@'];
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US06']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US15(self):
        expected_id = ['@F11@'];
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US15']
        for record in log:
            a = record[2];
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)
    
    def test_US31(self):
        expected_id = ['@I27@','@I28@','@I29@','@I30@','@I31@','@I32@','@I33@','@I34@','@I35@','@I36@','@I37@','@I38@','@I39@','@I40@','@I41@']
        q = P.Parser()
        
        generated_id = us31_living_single(q)
        self.assertEqual(expected_id, generated_id)

    def test_US23(self):
        expected_id = ['@I42@','@I43@']
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US23']
        for record in log:
            a = record[2]
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US26(self):
            expected_id = ['@I44@','@I44@', '@F11@', '@F12@', '@F12@'];
            generated_id = []
            log = [i for i in self.p.log if i[0] == 'US26']
            for record in log:
                a = record[2];
                generated_id.append(a[0])
            self.assertEqual(expected_id, generated_id)

    def test_US33(self):
            expected_id = ['@I47@'];
            q = P.Parser()
            generated_id = us33_list_orphans(q)

            self.assertEqual(expected_id, generated_id)


    def test_US17(self):
        expected_id = ['@F6@','@F6@','@F8@','@F9@']
        p = P.Parser()
        
        generated_id = []
        log = [i for i in self.p.log if i[0] == 'US17']
        for record in log:
            a = record[2]
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US18(self):
        expected_id = ['@F6@']
        p = P.Parser()
        
        generated_id = []

        log = [i for i in self.p.log if i[0] == 'US18']
        for record in log:
            a = record[2]
            generated_id.append(a[0])
        self.assertEqual(expected_id, generated_id)

    def test_US16(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0]=='US16']
            self.assertIn(['US16', 'LAST', ['@F7@', '@I16@', '@I8@']], logs)
        
        else:
            self.run_test('US16')
    
    def test_US20(self):
        if self._path == 'GEDCOM_File_withErrors.ged':
            logs = [i for i in self.p.log if i[0]=='US20']
            self.assertIn(['US20', 'AUNT', ['@F6@', '@I12@', '@I13@']], logs)
            self.assertIn(['US20', 'UNCL', ['@F6@', '@I13@', '@I12@']], logs)
        
        else:
            self.run_test('US20')
    
    def test_US32(self):
        
        expected_id = ['@I42@','@I43@','@I44@','@I48@']
        q = P.Parser()
        generated_id = us32_list_multiple_births(q)

        self.assertEqual(expected_id, generated_id)
    
    def test_US34(self):
        
        expected_id = ['@F1@','@F2@','@F3@','@F8@']
        q = P.Parser()
        generated_id = us34_larger_age_difference(q)

        self.assertEqual(expected_id, generated_id)


if __name__ == '__main__':
    unittest.main()

        

        
   





        

        
   






