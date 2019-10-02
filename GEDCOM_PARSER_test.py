import unittest
import GEDCOM_Parser_Sprint1_v1
from prettytable import PrettyTable
import inspect
import GEDCOM_Parser_Sprint1_v1
from GEDCOM_Parser_Sprint1_v1 import Parser, us01_check_before_today, us03_birth_before_death,us02_birth_before_marriage,us35_birth_inlast_30days,us36_death_inlast_30days,us42_reject_illegitimate_dates
import logging

class TestUserStories(unittest.TestCase):


    logging.basicConfig(filename='gedcom.log',filemode='w', format='%(levelname)-2s : %(message)s')

    rint = Parser()
    indi, fam, log = rint.main()
    rint.print_dicts(indi,fam)
    log_func={
     ("US21","HUSB"): lambda x: f"US21: FAM: {x[0]}: Husband ({x[1]}) has incorrect gender",
     ("US21","WIFE"): lambda x: f"US21: FAM: {x[0]}: Wife ({x[1]}) has incorrect gender",
     ("US22","FAM"): lambda x: f"US22: FAM: {x}: Family already exists",
     ("US22","INDI"): lambda x: f"US22: INDI: {x}: Individual already exists",
     ("US42","BIRT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Birth Date {x[1]}",
     ("US42","DEAT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Death Date {x[1]}",
     ("US42","MARR"): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Marraige Date {x[1]}",
     ("US42","DIV"): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Divorce Date {x[1]}"
     }
    for x in log:
        logging.error(log_func[x[0],x[1]](x[2]))
        #print("ERROR: %s" %(log_func[x[0],x[1]](x[2])))


    def test_US01(self):
        """Tests if the date from the dictionary is before today's date"""

        user_story = inspect.stack()[0][3].replace('test_', '')

        for id, records in self.indi.items():
            with self.subTest(id=id): 
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')

                
                if birth_date1 is None:
                    logging.error(
                        f"{user_story} : INDI : {id} : Birth Date is not known ")
                    out = False
                else:
                    check_birth = us01_check_before_today(birth_date1)
                    if check_birth is False:
                        logging.error(
                            f"{user_story} : INDI : {id} : Birth Date {birth_date1} is before today's date.")
                    self.assertTrue(check_birth)

                
                if death_date1 is not None:
                #     logging.error(
                #         f"{user_story} : INDI : {id} : Death Date is not known ")
                #     out = False
                # else:
                    check_death = us01_check_before_today(death_date1)
                    if check_death is False:
                        logging.error(
                            f"{user_story} : INDI : {id} : Death Date {death_date1} is before today's date.")
                    self.assertTrue(check_death)

        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is None:
                    logging.error(
                        f"{user_story} : FAM : {id} : Marriage Date is not known ")
                    out = False
                else:
                    check_marr = us01_check_before_today(marr_date1)
                    if check_marr is False:
                        logging.error(
                            f"{user_story} : FAM : {id} : Marriage Date {marr_date1} is before today's date.")
                    self.assertTrue(check_marr)
 
                if div_date1 is not None:
                #     logging.error(
                #         f"{user_story} : FAM : {id} : Divorce Date is not known ")
                #     out = False
                # else:
                    check_div = us01_check_before_today(div_date1)
                    if check_div is False:
                        logging.error(
                            f"{user_story} : FAM : {id} : Divorce Date {div_date1} is before today's date.")
                    self.assertTrue(check_div)


    def test_US02(self):
        '''Birth Date before marriage between spouses'''
        user_story = inspect.stack()[0][3].replace('test_', '')
        for id, record in self.fam.items():
            marriage = record.get('MARR')
            if marriage is None:
                logging.warning(f"{user_story} : FAM : {id} : Marriage date is not known")
            else:
                husband_birth = self.indi[record.get('HUSB')].get('BIRT')
                wife_birth = self.indi[record.get('WIFE')].get('BIRT') 
                with self.subTest(id=id):
                    if husband_birth is None:
                        logging.error(
                            f"{user_story} : FAM : {id} : Husband's Birth Date is not known ")
                        out = False
                    else:
                        check_husband = us02_birth_before_marriage(marriage,husband_birth)
                        if check_husband is False:
                            logging.error(
                                f"{user_story} : FAM : {id} : Husband's Birth Date {husband_birth} is after Marriage Date {marriage} ")
                        self.assertTrue(check_husband)
                with self.subTest(id=id):
                    if wife_birth is None:
                        logging.error(
                            f"{user_story} : FAM : {id} : Wife's Birth Date is not known ")
                        out = False
                    else:
                        check_wife = us02_birth_before_marriage(marriage,wife_birth)
                        if check_wife is False:
                            logging.error(
                                f"{user_story} : FAM : {id} : Wife's Birth Date {wife_birth} is after Marriage Date {marriage} ")
                        self.assertTrue(check_wife)


    def test_US03(self):
        '''Test for Birth Date before Death Date'''
        user_story = inspect.stack()[0][3].replace('test_','')
        for id, record in self.indi.items():
            with self.subTest(id=id):
                birth = record.get('BIRT')
                death = record.get('DEAT')
                if birth is None:
                    logging.warning(f"{user_story} : INDI : {id} : Individual does not seems to be born yet. ")
                    out=False
                else:
                    out = us03_birth_before_death(birth, death)
                    if out is False:
                        logging.error(f"{user_story} : INDI : {id} : Death Date {death} is before Birth Date {birth} ")
                    self.assertTrue(out)



    def test_US21(self):
        """Test the logging and printing of correct gender for roles"""
        print(f"\nThere is {len([i for i in self.log if i[0]=='US21'])} Error Found For User Story 21: ")
        x = PrettyTable(["Test","Case","Spec"])
        for i in self.log:
            if i[0]=='US21':
                x.add_row(i)
        print(x)
        #self.assertEqual(self.log_func['US21','HUSB'](['F1','I5']), \
        #    "FAMILY: F1: US21: Husband (I5) has incorrect gender", "log printing test.")
        #self.assertEqual(self.log_func['US21','WIFE'](['F2','I4']), \
        #    "FAMILY: F2: US21: Wife (I4) has incorrect gender", "log printing test.")

    def test_US22(self):
        """Test if the Family ID and the Individual ID are Unique"""
        print(f"\nThere is {len([i for i in self.log if i[0]=='US22'])} Error Found For User Story 22: ")
        x = PrettyTable(["Test","Case","Spec"])
        for i in self.log:
            if i[0]=='US22':
                x.add_row(i)
        print(x)
        #self.assertEqual(self.log_func['US22', 'INDI']('x'), "INDIVIDUAL: x: US22: Individual already exists")
        #self.assertEqual(self.log_func['US22', 'FAM']('x'), "FAMILY: x: US22: Family already exists")
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
                    check_birth = us35_birth_inlast_30days(birth)
                    if check_birth is True:
                        x.add_row([id,name,birth])
        print(f"\n{x}")
                    

    def test_US36(self):
        """List death date in last 30 days"""
        x = PrettyTable(["ID","Name","Death"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                death = record.get('DEAT')
                name = record.get('NAME')
                check_death = us36_death_inlast_30days(death)
                if check_death is True:
                    x.add_row([id,name,death])
        #logging.(f"List all deaths in the last 30 days \n {x}")            
        print(f"\n{x}")
        
    def test_US42(self):
        "Tests if the illegitimate dates are rejected"

        for id, records in self.indi.items():
            with self.subTest(id=id):
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')
                name = records.get('NAME')
                if birth_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(birth_date1))
                if death_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(death_date1))


        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(marr_date1))
                if div_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(div_date1))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
