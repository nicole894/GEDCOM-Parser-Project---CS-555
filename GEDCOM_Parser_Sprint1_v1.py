from prettytable import PrettyTable
import time
import unittest
from datetime import datetime, timedelta
from datetime import date
import inspect
from dateutil.parser import parse
import logging

today = time.strftime("%Y %m %d").split(' ')
month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


class Parser():
    fam = {}
    indi = {}
    log = []

    def validate_file(self, path):
        path = "GEDCOM_File_withErrors.ged"
        """Read the contains of file"""
        valid_lines = 0
        total_lines = 0
        line_count = 0
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        else:
            total_lines = fp.readlines()
            total_lines = len(total_lines)
            fp.seek(0)
            for line in fp:
                tokens = line.split()
                line_count += 1
                if len(tokens) == 3 and tokens[0] == '0' and (tokens[2] == 'INDI' or tokens[2] == "FAM"):
                    valid_lines = valid_lines + 1

                else:
                    tags = {'0': ["HEAD", "TRLR", "NOTE"],
                            '1': ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                            '2': ["DATE"]}
                    level = tokens[0]
                    tag = tokens[1]
                    argument = " ".join(tokens[2:])

                    if level in tags and tag in tags[level]:
                        valid_lines = valid_lines + 1
                    else:
                        print("File not valid at: Line {}".format(line_count))

            try:
                if valid_lines != total_lines:
                    raise ArithmeticError
            except ArithmeticError:
                print("File is invalid: Please check the contents of the file")
                exit(0)

        fp.close()
        # return  fp.seek(0)

    def create_data(self, counter, content_list, dict_type, id, log):
        spec_list = ['BIRT', 'DEAT', 'DIV', 'MARR']
        data_dict = {}
        fams_list = []
        child_list = []
        for i in range(counter + 1, len(content_list)):
            each_data = content_list[i]
            if int(each_data[0]) == 0:
                return data_dict
            elif int(each_data[0]) == 1 and each_data[1] == 'FAMS':
                fams_list.append(each_data[2])
                data_dict.update({each_data[1]: fams_list})
            elif int(each_data[0]) == 1 and each_data[1] == 'CHIL':
                child_list.append(each_data[2])
                data_dict.update({each_data[1]: child_list})
            elif int(each_data[0]) == 1 and each_data[1] not in spec_list:
                data_dict.update({each_data[1]: each_data[2]})
            elif int(each_data[0]) == 1 and each_data[1] in spec_list:
                date_list = content_list[i + 1]
                date = date_list[2]
                test_date = us42_reject_illegitimate_dates(date)
                # print(test_date)
                if test_date == "False":
                    data_dict.update({each_data[1]: date})
                else:
                    log.append(["US42", each_data[1], [id, date]])

        return data_dict

    def build_data_dict(self, path, indi, fam, log):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("File not found : ", path)
        else:

            content_list = []
            file_content = fp.readlines()
            for line in file_content:
                line = list(line.rstrip("\n").split(" ", 2))
                content_list.append(line)

            counter = 0

            for i in content_list:
                if int(i[0]) == 0 and len(i) == 3 and i[2] == 'INDI':
                    data = self.create_data(counter, content_list, i[2], i[1], log)
                    if i[1] in indi.keys():  # Tag US22
                        log.append(["US22", "INDI", i[1]])
                    else:
                        indi.update({i[1]: data})
                elif int(i[0]) == 0 and len(i) == 3 and i[2] == 'FAM':
                    data = self.create_data(counter, content_list, i[2], i[1], log)
                    if i[1] in fam.keys():  # Tag US22
                        log.append(["US22", "FAM", i[1]])
                    else:
                        fam.update({i[1]: data})
                counter = counter + 1
                fp.close()
            return indi, fam, log

    @staticmethod
    def date_format(date_list):
        yyyy = date_list[2]
        mm = ('%02d' % (month.index(date_list[1]) + 1))
        dd = '%02d' % int(date_list[0])
        return (yyyy, mm, dd)

    @staticmethod
    def age_carry(new, old):
        if new[1] < old[1]:
            return 1
        elif new[1] == old[1] and new[2] < old[2]:
            return 1
        else:
            return 0

    def print_indi(self, indi_dict):
        x = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        for k, v in indi_dict.items():
            uid = k
            name = v.get('NAME')
            sex = v.get('SEX')
            dob = v.get('BIRT', 'NA')
            born = (dob != 'NA')
            if born:
                dob = self.date_format(dob.split(' '))
            dod = v.get('DEAT', 'NA')
            alive = (dod == 'NA')
            if not alive:
                dod = self.date_format(dod.split(' '))
            if not born:
                age = 'NA'
            elif alive:
                age = int(today[0]) - int(dob[0]) - self.age_carry(today, dob)
            else:
                age = int(dod[0]) - int(dob[0]) - self.age_carry(dod, dob)
            child = v.get('FAMC', 'NA')
            spouse = v.get('FAMS', 'NA')
            x.add_row([uid, name, sex, '-'.join(dob), age, alive, alive and 'NA' or '-'.join(dod), child, spouse])
        # print(x)
        logging.info(f"Individual Table \n {x}")

    def print_fam(self, fam_dict, indi_dict):
        def get_name(indi_dict, nid):
            return indi_dict[nid].get('NAME')

        x = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
        for k, v in fam_dict.items():
            uid = k
            mar = v.get('MARR', 'NA')
            married = (mar != 'NA')
            if married:
                mar = self.date_format(mar.split(' '))
            div = v.get('DIV', 'NA')
            if div != 'NA':
                div = self.date_format(div.split(' '))
            hid = v.get('HUSB')
            hname = get_name(indi_dict, hid)
            wid = v.get('WIFE')
            wname = get_name(indi_dict, wid)
            children = v.get('CHIL', 'NA')
            x.add_row([uid, '-'.join(mar), (div == 'NA') and 'NA' or '-'.join(div), hid, hname, wid, wname, children])
        logging.info(f"Family Table \n {x}")
        # print(x)

    def us21_right_gender_for_role(self, indi, fam, log):
        fam_ids = self.fam.keys()
        for k in self.fam:
            hid = self.fam[k]['HUSB']  # Tag US21
            wid = self.fam[k]['WIFE']
            if self.indi[hid]['SEX'] != 'M':
                self.log.append(["US21", "HUSB", [k, hid]])
            if self.indi[wid]['SEX'] != 'F':
                self.log.append(["US21", "WIFE", [k, wid]])  # End US21

    def main(self):
        path = "GEDCOM_File_withErrors.ged"
        self.validate_file(path)
        self.indi, self.fam, self.log = self.build_data_dict(path, self.indi, self.fam, self.log)
        self.us21_right_gender_for_role(self.indi, self.fam, self.log)
        return self.indi, self.fam, self.log

    def print_dicts(self, indi, fam):
        # print("Individual Dictionary: {}" .format(indi))
        # print("Families Dictionary: {}" .format(fam))
        # print("Individuals")
        self.print_indi(indi)
        # print("Families")
        self.print_fam(fam, indi)


# End of the Parser Class
def convert_str_date(date):
    datetime_object = datetime.strptime(date, '%d %b %Y')
    return datetime_object


def us42_reject_illegitimate_dates(dates):
    "Rejects illegitimate dates"
    # print("In REJECT FUN")
    return_flag = 'False'
    try:
        parse(dates)
    except ValueError:
        return_flag = 'True'
    return return_flag


def us01_check_before_today(check_date):
    """Checks if the date is before today"""

    date1 = convert_str_date(check_date)
    date2 = date1.date()

    today1 = datetime.today()

    if date2 > today1.date():
        return False
    else:
        return True



def check_date1_before_date2(date1, date2):
    date1 = convert_str_date(date1)
    date2 = convert_str_date(date2)
    if date1 < date2:
        return True
    else:
        return False


def us03_birth_before_death():
    g = Parser()
    checked_list = []
    # print(f"This is a list of indi: {g.indi}")
    for id, v in g.indi.items():
        birth = v.get('BIRT')
        death = v.get('DEAT')
        if birth and death:
            result = check_date1_before_date2(birth, death)
            if result is True:
                checked_list.append("Yes")
            else:
                checked_list.append("No")
                logging.error(
                    f"US03 : INDI : {id} : Death Date {convert_str_date(death).date()} is before Birth Date "
                    f"{convert_str_date(birth).date()} ")
    return checked_list


def us04_marriage_before_divorce():
    g = Parser()
    checked_list = []
    for id, v in g.fam.items():
        marriage = v.get('MARR')
        divorce = v.get('DIV')
        if marriage and divorce:
            result = check_date1_before_date2(marriage, divorce)
            if result is True:
                checked_list.append("Yes")
            else:
                checked_list.append("No")
                logging.error(
                    f'US04 : FAM : {id} : Divorce Date {convert_str_date(divorce).date()} is '
                    f'before Marriage Date {convert_str_date(marriage).date()}')
    return checked_list


def us02_birth_before_marriage():
    g = Parser()
    checked_list = []
    for id, v in g.fam.items():
        marriage = v.get('MARR')
        husb = v.get('HUSB')
        wife = v.get('WIFE')
        husb_birth = g.indi[husb].get('BIRT')
        wife_birth = g.indi[wife].get('BIRT')
        if marriage and husb_birth and wife_birth:
            husb_result = check_date1_before_date2(husb_birth, marriage)
            if husb_result is False:
                logging.error(f'US02 : FAM : {id} : Marriage Date {convert_str_date(marriage).date()}'
                              f' is before Husband\'s ({husb}) birthdate {convert_str_date(husb_birth).date()}')
            wife_result = check_date1_before_date2(wife_birth, marriage)
            if wife_result is False:
                logging.error(f'US02 : FAM : {id} : Marriage Date {convert_str_date(marriage).date()}'
                              f' is before Wife\'s ({wife}) birthdate {convert_str_date(wife_birth).date()}')
            if wife_result and husb_result:
                checked_list.append('Yes')
            else:
                checked_list.append('No')
    return checked_list

def us05_marriage_before_death():
    g = Parser()
    checked_list = []
    for id, v in g.fam.items():
        marriage = v.get('MARR')
        husb = v.get('HUSB')
        wife = v.get('WIFE')
        husb_result = True
        wife_result = True
        husb_death = g.indi[husb].get('DEAT')
        wife_death = g.indi[wife].get('DEAT')
        if marriage and husb_death:
            husb_result = check_date1_before_date2(marriage, husb_death)
            if husb_result is False:
                logging.error(f'US05 : FAM : {id} : Marriage Date {convert_str_date(marriage).date()}'
                              f' is after Husband\'s ({husb}) Death date {convert_str_date(husb_death).date()}')
        if marriage and wife_death:
            wife_result = check_date1_before_date2(marriage, wife_death)
            if wife_result is False:
                logging.error(f'US05 : FAM : {id} : In Family ({id}), Marriage Date {convert_str_date(marriage).date()}'
                              f' is after Wife\'s ({wife}) Death {convert_str_date(wife_death).date()}')
            if wife_result and husb_result:
                checked_list.append('Yes')
            else:
                checked_list.append('No')
    return checked_list




def us35_birth_inlast_30days(birth):
    """Calculate birthdays in last 30 days"""
    birthday = convert_str_date(birth).date()
    todays_date = datetime.today().date()

    last30 = (todays_date - timedelta(days=30))

    if last30 <= birthday and birthday <= todays_date:
        return True
    else:
        return False


def us36_death_inlast_30days(death):
    """Calculate death in last 30 days"""
    if death is None:
        return False
    else:
        deathday = convert_str_date(death).date()
        todays_date = datetime.today().date()

        last30 = (todays_date - timedelta(days=30))

        if last30 <= deathday and deathday <= todays_date:
            return True
        else:
            return False
