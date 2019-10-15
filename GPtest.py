import unittest
from prettytable import PrettyTable
import GDriver as D
from GDriver import us38_list_upcoming_birthdays, us39_list_upcoming_anniversary, us35_birth_inlast_30days, us36_death_inlast_30days
import GParser as P
D.today = '15 OCT 2019'

class TestUS(unittest.TestCase):
    __ALL__=["US01","US02","US03","US21","US22","US35","US36","US42",
             "US04","US05","US07","US08","US09","US10","US38","US39"]
    __INFO__=["US35", "US36", "US38", "US39"]
    _path='GEDCOM_File_withErrors.ged'
    p = D.main(_path)

    def run_test(self,_test):
        x = None
        logs = [i for i in self.p.log if i[0]==_test]
        count=len(logs)
        if _test in self.__INFO__:
            # if count==1:
            #     print(f"{_test} Output: \n{logs[0][2][0]}")
            self.assertEqual(count, 1,f"{_test}: This test should always generate an INFO.")
        else:
            if count:
                x = PrettyTable(["Test","Case","Spec"])
                for i in self.p.log:
                    if i[0]==_test:
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
        expected_id = ['@F1@', '@F2@', '@F3@', '@F6@'];
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
            self.run_test('US09')
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

    def test_US38(self):
        
        expected_id = ['@I5@', '@I21@']
        q = P.Parser()
       
        fix_date = D.today 
        generated_id = us38_list_upcoming_birthdays(q, fix_date)
        self.assertEqual(expected_id, generated_id)
       
    def test_US39(self):
        expected_id = ['@F5@','@F9@']
        q = P.Parser()
        
        fix_date = D.today 
        generated_id = us39_list_upcoming_anniversary(q, fix_date)
        self.assertEqual(expected_id, generated_id)

if __name__ == '__main__':
    unittest.main()

        

        
   





        

        
   






