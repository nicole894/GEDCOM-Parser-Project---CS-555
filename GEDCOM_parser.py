from prettytable import PrettyTable
import time
today = time.strftime("%Y %m %d").split(' ')
month=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def validate_file(path):
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


    return  fp.seek(0)


def create_data(counter,content_list):
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


def build_data_dict(path, indi, fam):
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
                data = create_data(counter,content_list)
                indi.update({i[1]:data})
            elif int(i[0]) == 0 and len(i) == 3 and i[2] == 'FAM':
                data = create_data(counter, content_list)
                fam.update({i[1]: data})
            counter = counter + 1
        return indi, fam



def date_format(date_list):
    yyyy=date_list[2]
    mm=('%02d' % (month.index(date_list[1])+1))
    dd= '%02d' % int(date_list[0])
    return (yyyy, mm, dd)

def age_carry(new,old):
    if(new[1]<old[1]):
        return 1
    elif(new[1]==old[1] and new[2]<old[2]):
        return 1
    else:
        return 0

def print_indi(indi_dict):
    x = PrettyTable(["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"])
    for k,v in indi_dict.items():
        uid=k
        name=v.get('NAME')
        sex=v.get('SEX')
        DOB= date_format(v.get('BIRT').split(' '))
        DOD=v.get('DEAT','NA')
        alive=(DOD=='NA')
        if not alive:
            DOD = date_format(DOD.split(' '))
        if alive:
            age = int(today[0]) - int(DOB[0]) - age_carry(today,DOB)
        else:
            age = int(DOD[0]) - int(DOB[0]) - age_carry(DOD,DOB)
        child=v.get('FAMC','NA')
        spouse=v.get('FAMS', 'NA')
        x.add_row([uid,name,sex,'-'.join(DOB),age,alive,alive and 'NA' or '-'.join(DOD),child,spouse])
    print(x)

def print_fam(fam_dict, indi_dict):
    def get_name(indi_dict,nid):
        return indi_dict[nid].get('NAME')
    
    x=PrettyTable(["ID","Married","Divorced","Husband ID","Husband Name","Wife ID","Wife Name","Children"])
    for k,v in fam_dict.items():
        uid=k
        mar=date_format(v.get('MARR').split(' '))
        div=v.get('DIV', 'NA')
        if div!='NA':
            div=date_format(div.split(' '))
        hid=v.get('HUSB')
        hname=get_name(indi_dict,hid)
        wid=v.get('WIFE')
        wname=get_name(indi_dict,wid)
        children= v.get('CHIL','NA')
        x.add_row([uid,'-'.join(mar),(div=='NA') and 'NA' or '-'.join(div),hid,hname,wid,wname,children])       
    print(x)

def main():
    path = "GEDCOM_File.ged"                                    
    fam = {}
    indi = {}
    validate_file(path)
    indi, fam = build_data_dict(path,indi,fam)
    print("Individuals")
    print_indi(indi)
    print("Families")
    print_fam(fam, indi)

if __name__ == '__main__':
    main()