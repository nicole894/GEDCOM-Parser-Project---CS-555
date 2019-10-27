
from prettytable import PrettyTable
import time

api_version=204

today = time.strftime("%Y %m %d").split(' ')
month=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
log_level=["US35", "US36", "US38", "US39"]
log_func={
    ("US01","B_NA"): lambda x: f"US01: INDI: {x[0]}: Birth Date is not known",
    ("US01","BIRT"): lambda x: f"US01: INDI: {x[0]}: Birth Date {x[1]} is after today's date",
    ("US01","DEAT"): lambda x: f"US01: INDI: {x[0]}: Death Date {x[1]} is after today's date",
    ("US01","M_NA"): lambda x: f"US01: FAM: {x[0]}: Marriage Date is not known",
    ("US01","MARR"): lambda x: f"US01: FAM: {x[0]}: Marriage Date {x[1]} is after today's date",
    ("US01","DIV" ): lambda x: f"US01: FAM: {x[0]}: Divorce Date {x[1]} is after today's date.",

    ("US02","M_NA"): lambda x: f"US02: FAM: {x[0]}: Marriage Date is not known",
    ("US02","H_NA"): lambda x: f"US02: FAM: {x[0]}: Husband's Birth Date is not known",
    ("US02","HUSB"): lambda x: f"US02: FAM: {x[0]}: Husband's ({x[1]}) Birth Date {x[2]} is after Marriage Date {x[3]}",
    ("US02","W_NA"): lambda x: f"US02: FAM: {x[0]}: Wife's Birth Date is not known",
    ("US02","WIFE"): lambda x: f"US02: FAM: {x[0]}: Wife's ({x[1]}) Birth Date {x[2]} is after Marriage Date {x[3]}",

    ("US03","B_NA"): lambda x: f"US03: INDI: {x[0]}: Birth Date is not known",
    ("US03","BB4D"): lambda x: f"US03: INDI: {x[0]}: Birth Date {x[1]} is after Death Date {x[2]}",

    ("US04","MB4D"): lambda x: f"US04: FAM: {x[0]}: Marriage Date {x[1]} is after Divorce Date {x[2]}",

    ("US05","HUSB"): lambda x: f"US05: FAM: {x[0]}: Marriage Date {x[1]} is after Husband's ({x[2]}) Death Date {x[3]}",
    ("US05","WIFE"): lambda x: f"US05: FAM: {x[0]}: Marriage Date {x[1]} is after Wife's ({x[2]}) Death Date {x[3]}",

    ("US07","BIRT"): lambda x: f"US07: INDI: {x[0]}: This Person's Birth Date is {x[1]} and is over 150 years old.",
    ("US07","DEAT"): lambda x: f"US07: INDI: {x[0]}: This Person's Birth Date is {x[1]} died on {x[2]} and is over 150 years old.",

    ("US08","BBPM"): lambda x: f"US08: FAM: {x[0]}: This child ({x[2]}) was born on {x[3]} before Parent's Marriage {x[1]}.",
    ("US08","BAPD"): lambda x: f"US08: FAM: {x[0]}: This child ({x[2]}) was born on {x[3]} over 9 months after Parent's Divorce {x[1]}.",

    ("US09","WIFE"): lambda x: f"US09: FAM: {x[0]}: This child ({x[3]}) was born on {x[4]} before Wife's ({x[1]}) Death {x[2]}.",
    ("US09","HUSB"): lambda x: f"US09: FAM: {x[0]}: This child ({x[3]}) was born on {x[4]} over 9 months after Husband's({x[1]}) Death {x[2]}.",    

    ("US10","HUSB"): lambda x: f"US10: FAM: {x[0]}: Marriage Date {x[1]} is before Husband's ({x[2]}) 14's Birthday.",
    ("US10","WIFE"): lambda x: f"US10: FAM: {x[0]}: Marriage Date {x[1]} is before WIFE's ({x[2]}) 14's Birthday.",
    
    ("US12","HUSB"): lambda x: f"US12: FAM: {x[0]}: Husband ({x[1]}):{x[2]} is too old when ({x[3]}):{x[4]} is born.",
    ("US12","WIFE"): lambda x: f"US12: FAM: {x[0]}: Wife ({x[1]}):{x[2]} is too old when ({x[3]}):{x[4]} is born.",

    ("US13","SPAC"): lambda x: f"US13: FAM: {x[0]}: Kid#1 {x[1]} born on {x[2]} has not proper spacing with kid#2 {x[3]} born on {x[4]}.",

    ("US21","HUSB"): lambda x: f"US21: FAM: {x[0]}: Husband ({x[1]}) has incorrect gender",
    ("US21","WIFE"): lambda x: f"US21: FAM: {x[0]}: Wife ({x[1]}) has incorrect gender",
 
    ("US22","FAM" ): lambda x: f"US22: FAM: {x[0]}: Family already exists",
    ("US22","INDI"): lambda x: f"US22: INDI: {x[0]}: Individual already exists",

    ("US35","BIRT"): lambda x: f"INFO: US35: INDI: List all birthdays in the last 30 days \n {x[0]}",
    ("US36","DEAT"): lambda x: f"INFO: US36: INDI: List all deaths in the last 30 days \n {x[0]}",

    ("US38","BIRT"): lambda x: f"INFO: US38: INDI: List all upcoming birthdays\n {x[0]}",
    ("US39","ANNI"): lambda x: f"INFO: US39: INDI: List all upcoming anniversaries\n {x[0]}",

    ("US42","BIRT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Birth Date {x[1]}",
    ("US42","DEAT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Death Date {x[1]}",
    ("US42","MARR"): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Marraige Date {x[1]}",
    ("US42","DIV" ): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Divorce Date {x[1]}",
    ("US06","WIFE" ): lambda x: f"US06: FAM: {x[0]}: Wife's ({x[1]}) Death date {x[2]} is before Divorce Date {x[3]}",
    ("US06","HUSB" ): lambda x: f"US06: FAM: {x[0]}: Husband's ({x[1]}) Death date {x[2]}  is before Divorce Date {x[3]}",
    ("US15","FAM" ): lambda x: f"US15: FAM: {x[0]}: Family ({x[0]}) has more than 14 siblings {x[1]}"
    }

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
        sex=v.get('SEX', 'NA')
        DOB=v.get('BIRT', 'NA')
        born = (DOB!='NA')
        if born:
            DOB=date_format(DOB.split(' '))
        DOD=v.get('DEAT','NA')
        alive=(DOD=='NA')
        if not alive:
            DOD = date_format(DOD.split(' '))
        if not born:
            age = 'NA'
        elif alive:
            age = int(today[0]) - int(DOB[0]) - age_carry(today,DOB)
        else:
            age = int(DOD[0]) - int(DOB[0]) - age_carry(DOD,DOB)
        child=v.get('FAMC','NA')
        spouse=v.get('FAMS', 'NA')
        x.add_row([uid,name,sex,born and '-'.join(DOB) or 'NA', age, born and alive, alive and 'NA' or '-'.join(DOD), child, spouse])
    print(x)

def print_fam(fam_dict, indi_dict):
    def get_name(indi_dict,nid):
        return indi_dict[nid].get('NAME')
    
    x=PrettyTable(["ID","Married","Divorced","Husband ID","Husband Name","Wife ID","Wife Name","Children"])
    for k,v in fam_dict.items():
        uid=k
        mar= v.get('MARR', 'NA')
        if (mar!='NA'):
            mar = date_format(mar.split(' '))
        div=v.get('DIV', 'NA')
        if div!='NA':
            div=date_format(div.split(' '))
        hid=v.get('HUSB')
        hname=get_name(indi_dict,hid)
        wid=v.get('WIFE')
        wname=get_name(indi_dict,wid)
        children= v.get('CHIL','NA')
        x.add_row([uid, (mar=='NA') and 'NA' or '-'.join(mar), (div=='NA') and 'NA' or '-'.join(div),hid,hname,wid,wname,children])       
    print(x)
    
def print_log(log_dict):
    for i in log_dict:
        if i[0] in log_level:
            print(log_func[i[0],i[1]](i[2]))
        else:
            print("ERROR: "+ log_func[i[0],i[1]](i[2]))
