from prettytable import PrettyTable
import time
import unittest
from datetime import datetime
import inspect

today = time.strftime("%Y %m %d").split(' ')
month=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

class Parser():

    test_v ='This works'
    fam = {}
    indi = {}

    def validate_file(self, path):

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
                 data_dict.update({each_data[1]: date})

        return data_dict


    def build_data_dict(self, path, indi, fam):
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
                    indi.update({i[1]:data})
                elif int(i[0]) == 0 and len(i) == 3 and i[2] == 'FAM':
                    data = self.create_data(counter, content_list)
                    fam.update({i[1]: data})
                counter = counter + 1
                fp.close()
            return indi, fam



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
            DOB= self.date_format(v.get('BIRT').split(' '))
            DOD=v.get('DEAT','NA')
            alive=(DOD=='NA')
            if not alive:
                DOD = self.date_format(DOD.split(' '))
            if alive:
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
            mar=self.date_format(v.get('MARR').split(' '))
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

    def main(self):
        path = "GEDCOM_File.ged"
        self.validate_file(path)
        indi, fam = self.build_data_dict(path,self.indi,self.fam)

        return  indi,fam

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






class TestUserStories(unittest.TestCase):

    print = Parser()
    indi, fam = print.main()
    print.print_dicts(indi,fam)

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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
