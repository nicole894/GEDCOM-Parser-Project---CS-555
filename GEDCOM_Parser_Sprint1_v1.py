from prettytable import PrettyTable
import time
import unittest
from datetime import datetime, timedelta
from datetime import date
import inspect
from dateutil.parser import parse

today = time.strftime("%Y %m %d").split(' ')
month=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
class Parser():

    test_v ='This works'
    fam = {}
    indi = {}
    log = []

    def validate_file(self, path):
        path = "GEDCOM_File.ged"
        print(path)
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
                    if (len(tokens) == 3 and tokens[0] == '0' and (tokens[2] == 'INDI' or tokens[2] == "FAM")):
                            valid_lines = valid_lines + 1

                    else:
                        tags = {'0' : ["HEAD", "TRLR", "NOTE"],
                                '1' : ["NAME","SEX","BIRT","DEAT", "FAMC","FAMS","MARR", "HUSB", "WIFE","CHIL", "DIV"],
                                '2' : ["DATE"]}
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
        #return  fp.seek(0)


    def create_data(self, counter,content_list):
        spec_list = ['BIRT','DEAT','DIV','MARR']
        data_dict={}
        fams_list = []
        child_list=[]
        for i in range(counter+1,len(content_list)):
            each_data = content_list[i]
            if int(each_data[0])==0:
                return data_dict
            elif int(each_data[0]) == 1 and each_data[1] == 'FAMS':
                fams_list.append(each_data[2])
                data_dict.update({each_data[1]: fams_list })
            elif int(each_data[0]) == 1 and each_data[1] == 'CHIL':
                child_list.append(each_data[2])
                data_dict.update({each_data[1]: child_list})
            elif int(each_data[0])==1 and each_data[1] not in spec_list :
                data_dict.update({each_data[1]:each_data[2]})
            elif int(each_data[0]) == 1 and each_data[1] in spec_list :
                 date_list = content_list[i+1]
                 date = date_list[2]
                 test_date = reject_illegitimate_dates(date)
                 #print(test_date)
                 if test_date == "False":
                    data_dict.update({each_data[1]: date})

        return data_dict


    def build_data_dict(self, path, indi, fam, log):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("File not found : ",path )
        else:

            content_list = []
            file_content = fp.readlines()
            for line in file_content:

                line = list(line.rstrip("\n").split(" ", 2))
                content_list.append(line)

            counter =0

            for i in content_list:
                if int(i[0]) == 0 and len(i) == 3 and i[2] == 'INDI':
                    data = self.create_data(counter,content_list)
                    if i[1] in indi.keys(): #Tag US22
                        log.append(["US22","INDI",i[1]])
                    else:
                        indi.update({i[1]:data})
                elif int(i[0]) == 0 and len(i) == 3 and i[2] == 'FAM':
                    data = self.create_data(counter, content_list)
                    if i[1] in fam.keys(): #Tag US22
                        log.append(["US22","FAM",i[1]])
                    else:
                        fam.update({i[1]: data})
                counter = counter + 1
                fp.close()
            return indi, fam, log



    def date_format(self,date_list):
        yyyy=date_list[2]
        mm=('%02d' % (month.index(date_list[1])+1))
        dd= '%02d' % int(date_list[0])
        return (yyyy, mm, dd)

    def age_carry(self,new,old):
        if(new[1]<old[1]):
            return 1
        elif(new[1]==old[1] and new[2]<old[2]):
            return 1
        else:
            return 0

    def print_indi(self,indi_dict):
        x = PrettyTable(["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"])
        for k,v in indi_dict.items():
            uid=k
            name=v.get('NAME')
            sex=v.get('SEX')
            DOB= v.get('BIRT', 'NA')
            born = (DOB!='NA')
            if born:
                DOB = self.date_format(DOB.split(' '))
            DOD=v.get('DEAT','NA')
            alive=(DOD=='NA')
            if not alive:
                DOD = self.date_format(DOD.split(' '))
            if not born:
                age='NA'
            elif alive:
                age = int(today[0]) - int(DOB[0]) - self.age_carry(today,DOB)
            else:
                age = int(DOD[0]) - int(DOB[0]) - self.age_carry(DOD,DOB)
            child=v.get('FAMC','NA')
            spouse=v.get('FAMS', 'NA')
            x.add_row([uid,name,sex,'-'.join(DOB),age,alive,alive and 'NA' or '-'.join(DOD),child,spouse])
        print(x)

    def print_fam(self, fam_dict, indi_dict):
        def get_name(indi_dict,nid):
            return indi_dict[nid].get('NAME')

        x=PrettyTable(["ID","Married","Divorced","Husband ID","Husband Name","Wife ID","Wife Name","Children"])
        for k,v in fam_dict.items():
            uid=k
            mar= v.get('MARR', 'NA')
            married = (mar!='NA')
            if married:
                mar = self.date_format(mar.split(' '))
            div=v.get('DIV', 'NA')
            if div!='NA':
                div=self.date_format(div.split(' '))
            hid=v.get('HUSB')
            hname= get_name(indi_dict,hid)
            wid=v.get('WIFE')
            wname=get_name(indi_dict,wid)
            children= v.get('CHIL','NA')
            x.add_row([uid,'-'.join(mar),(div=='NA') and 'NA' or '-'.join(div),hid,hname,wid,wname,children])
        print(x)
    def US21_right_gender_for_role(self, indi, fam, log):
        fam_ids=self.fam.keys()
        for k in self.fam:
            hid = self.fam[k]['HUSB'] #Tag US21
            wid = self.fam[k]['WIFE']
            if self.indi[hid]['SEX']!='M':
                self.log.append(["US21","HUSB",[k,hid]])
            if self.indi[wid]['SEX']!='F':
                self.log.append(["US21","WIFE",[k,wid]]) #End US21

    def main(self):
        path = "GEDCOM_File.ged"
        self.validate_file(path)
        self.indi,self.fam, self.log = self.build_data_dict(path,self.indi,self.fam, self.log)
        self.US21_right_gender_for_role(self.indi,self.fam, self.log)
        return  self.indi,self.fam, self.log

    def print_dicts(self,indi, fam):
        print("Individual Dictionary: {}" .format(indi))
        print("Families Dictionary: {}" .format(fam))
        print("Individuals")
        self.print_indi(indi)
        print("Families")
        self.print_fam(fam, indi)

#End of the Parser Class


def log_fault(story, id, message, indi, fam):
    dict_type = ''
    if id in indi:
        dict_type = 'INDIVIDUAL'
    else:
        dict_type = 'FAMILY'
    print("ERROR: {}: {}: {}: {}.".format(story,dict_type,id,message))


def convert_str_date(date):
    datetime_object = datetime.strptime(date, '%d %b %Y')
    return datetime_object

def reject_illegitimate_dates(dates):
    "Rejects illegitimate dates"
    #print("In REJECT FUN")
    return_flag = 'False'
    try:
        parse(dates)
    except ValueError:
        return_flag = 'True'
    return return_flag

def check_before_today(date):

    """Checks if the date is before today"""

    date1= convert_str_date(date)
    date2 = date1.date()

    today = datetime.today()
  
    if date2 > today.date():
        return False
    else:
        return True


def birth_before_death(birth, death):

        if death is None:
            return True
        else:
            birth = convert_str_date(birth)
            death = convert_str_date(death)
            #print(birth.date())
            #print(death.date())

            if birth < death:
                return True
            else:
                return False

def birth_inlast_30days(birth):
    """Calculate birthdays in last 30 days"""
    birthday = convert_str_date(birth).date()
    todays_date = datetime.today().date()
    
    last30 = (todays_date - timedelta(days=30))

    if last30 <= birthday and birthday <= todays_date:
        return True
    else:
        return False

def death_inlast_30days(death):
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



