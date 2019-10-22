from datetime import datetime, timedelta
from datetime import date
from prettytable import PrettyTable
import PTutil as U
import GParser as P
# assert U.api_version >= P.api_version, "Parser is incompatible with api version of PTutil."
md=30.4;yd=365.25
today = 'today'


def convert_str_date(date):
    datetime_object = datetime.strptime(date, '%d %b %Y')
    return datetime_object

def check_date1_before_date2(date1, date2= today):
    if None in [date1, date2]:
        return None
    date1 = (date1 == 'today') and datetime.today() or convert_str_date(date1)
    date2 = (date2 == 'today') and datetime.today() or convert_str_date(date2)
    return date1 < date2

def date_in_n_days_from_today(date,n, td= today, both=True):
    if None in [date, td]:
        return None
    else:
        date = convert_str_date(date).date()
        td = datetime.today() if td=='today' else convert_str_date(td)
        td = td.date()       
        nd = (td + timedelta(days=n))
        if n<0:
            if not both:
                return nd <= date
            return nd <= date and date <= td
        else:
            if not both:
                return date <= nd
            return td <= date and date <= nd

K=convert_str_date
Kf=lambda date:K(date).strftime("%Y-%m-%d")
C=check_date1_before_date2
N=date_in_n_days_from_today
#=============================================================================#
def us21_correct_gender(p):
    for id, v in p.fam.items():
        hid = p.fam[id]['HUSB']
        wid = p.fam[id]['WIFE']
        if p.indi[hid]['SEX']!='M':
            p.log.append(["US21","HUSB",[id,hid]])
        if p.indi[wid]['SEX']!='F':
            p.log.append(["US21","WIFE",[id,wid]])

def us03_birth_before_death(p):
    for id, v in p.indi.items():
        birth = v.get('BIRT')
        death = v.get('DEAT')
        if birth is None:
            p.log.append(['US03','B_NA',[id]])
        elif C(birth, death) is False:
            p.log.append(['US03','BB4D',[id,Kf(birth),Kf(death)]])

def us01_check_before_today(p):
    for id, v in p.indi.items():
        birth = v.get('BIRT')
        death = v.get('DEAT')
        if birth is None:
            p.log.append(['US01','B_NA',[id]])
        elif C(birth, 'today') is False:
            p.log.append(['US01','BIRT',[id,Kf(birth)]])
        if death is not None and C(death, 'today') is False:
            p.log.append(['US01','DEAT',[id,Kf(death)]])
    for id, v in p.fam.items():
        mar = v.get('MARR')
        div = v.get('DIV')
        if mar is None:
            p.log.append(['US01','M_NA',[id]])
        elif C(mar, 'today') is False:
            p.log.append(['US01','MARR',[id,Kf(mar)]])
        if div is not None and C(div, 'today') is False:
            p.log.append(['US01','DIV',[id,Kf(div)]])

def us02_birth_before_marriage(p):
    for id, v in p.fam.items():
        mar = v.get('MARR')
        if mar is None:
            p.log.append(['US02','M_NA',[id]])
        else:
            K_mar=Kf(mar)
            hid=v.get('HUSB')
            hbir=p.indi[hid].get('BIRT')
            wid=v.get('WIFE')
            wbir=p.indi[wid].get('BIRT')
            if hbir is None:
                p.log.append(['US02','H_NA',[id]])
            elif C(hbir, mar) is False:
                p.log.append(['US02','HUSB',[id,hid,Kf(hbir),K_mar]])
            if wbir is None:
                p.log.append(['US02','W_NA',[id]])
            elif C(wbir, mar) is False:
                p.log.append(['US02','WIFE',[id,wid,Kf(wbir),K_mar]])

def us35_birth_inlast_30days(p, todays_date):
    x = PrettyTable(["ID","Name","Birthday"])
    id3 = []
    todays_date = (todays_date == 'today') and datetime.today() or convert_str_date(todays_date)
    todays_date = todays_date.date()

    for id, v in p.indi.items():
        birth = v.get('BIRT')
        name = v.get('NAME')
        if birth is not None:
            check_birth = N(birth, -30)
            if check_birth is True:
                x.add_row([id,name,birth])
                id3.append(id)
    p.log.append(['US35','BIRT',[x]])
    return id3

def us36_death_inlast_30days(p, todays_date):
    x = PrettyTable(["ID","Name","Death"])
    id4 = []
    for id, v in p.indi.items():
        death = v.get('DEAT')
        name = v.get('NAME')
        if death is not None:
            check_death = N(death, -30)
            if check_death is True:
                x.add_row([id,name,death])
                id4.append(id)
    p.log.append(['US36','DEAT',[x]])
    return id4

def us04_marriage_before_divorce(p):
    for id, v in p.fam.items():
        mar = v.get('MARR')
        if mar is not None:
            K_mar=Kf(mar)
            div = v.get('DIV')
            if div is not None and C(mar, div) is False:
                p.log.append(['US04','MB4D', [id,K_mar,Kf(div)]])

def us05_marriage_before_death(p):
    for id, v in p.fam.items():
        mar = v.get('MARR')
        if mar is not None:
            K_mar=Kf(mar)
            hid=v.get('HUSB')
            hdea=p.indi[hid].get('DEAT')
            wid=v.get('WIFE')
            wdea=p.indi[wid].get('DEAT')
            if hdea is not None and C(mar, hdea) is False:
                p.log.append(['US05','HUSB',[id,K_mar,hid,Kf(hdea)]])
            if wdea is not None and C(mar, wdea) is False:
                p.log.append(['US05','WIFE',[id,K_mar,wid,Kf(wdea)]])

def us07_150_years_old(p):
    for id, v in p.indi.items():
        birth = v.get('BIRT')
        death = v.get('DEAT')
        if birth is not None:
            if death is None:
                if N(birth,-150*yd, 'today', False) is False:
                    p.log.append(['US07','BIRT', [id,Kf(birth)]])
            else:
                if N(birth,-150*yd, death, False) is False:
                    p.log.append(['US07','DEAT', [id,Kf(birth),Kf(death)]])

def us08_birth_when_parent_married(p):
    for id, v in p.fam.items():
        mar = v.get('MARR')
        if mar is not None:
            div = v.get('DIV')
            kids = v.get('CHIL',[])
            for kid in kids:
                kbr = p.indi[kid].get('BIRT')
                if kbr is not None:
                    if C(kbr,mar):
                        p.log.append(['US08','BBPM',[id,Kf(mar),kid,Kf(kbr)]])
                    if N(kbr, 9*md, div, False) is False:
                        p.log.append(['US08','BAPD',[id,Kf(div),kid,Kf(kbr)]])

def us09_birth_before_parent_death(p):
    for id, v in p.fam.items():
        hid = p.fam[id]['HUSB']
        hdea=p.indi[hid].get('DEAT')
        wid=v.get('WIFE')
        wdea=p.indi[wid].get('DEAT')
        kids = v.get('CHIL',[])
        for kid in kids:
            kbr = p.indi[kid].get('BIRT')
            if kbr is not None:
                if C(wdea, kbr):
                    p.log.append(['US09','WIFE',[id,wid,Kf(wdea),kid,kbr]])
                if N(kbr, 9*md, hdea, False) is False:
                    p.log.append(['US09','HUSB',[id,hid,Kf(hdea),kid,kbr]])

def us10_marriage_after_14(p):
    for id, v in p.fam.items():
        mar = v.get('MARR')
        if mar is not None:
            K_mar=Kf(mar)
            hid=v.get('HUSB')
            hbir=p.indi[hid].get('BIRT')
            wid=v.get('WIFE')
            wbir=p.indi[wid].get('BIRT')
            if N(mar, 14*yd, hbir):
                p.log.append(['US10','HUSB',[id,K_mar,hid,Kf(hbir)]])
            if N(mar, 14*yd, wbir):
                p.log.append(['US10','WIFE',[id,K_mar,wid,Kf(wbir)]])

def us12_parent_not_too_old(p):
    for id, v in p.fam.items():
        hid = p.fam[id]['HUSB']
        hbir=p.indi[hid].get('BIRT')
        wid=v.get('WIFE')
        wbir=p.indi[wid].get('BIRT')
        kids = v.get('CHIL',[])
        for kid in kids:
            kbr = p.indi[kid].get('BIRT')
            if kbr is not None:
                if N(kbr, 60*yd, wbir, False) is False:
                    p.log.append(['US12','WIFE',[id,wid,Kf(wbir),kid,Kf(kbr)]])
                if N(kbr, 80*yd, hbir, False) is False:
                    p.log.append(['US12','HUSB',[id,hid,Kf(hbir),kid,Kf(kbr)]])

def us13_sibling_spacing(p):
    def spacing(date1,date2):
        if None in [date1, date2]:
            return None
        if C(date1,date2):
            return spacing(date2,date1)
        return N(date1,8*md,date2) and not N(date1,1,date2)
    for id, v in p.fam.items():
        kids = v.get('CHIL',[])
        kbrs = [p.indi[i].get('BIRT') for i in kids]
        for i in range(len(kids)-1):
            for j in range(i+1, len(kids)):
                if spacing(kbrs[i],kbrs[j]):
                    p.log.append(['US13', 'SPAC',[id,kids[i],Kf(kbrs[i]),kids[j],Kf(kbrs[j])]])                
                
def us38_list_upcoming_birthdays(p, todays_date):
    x = PrettyTable(["ID","Name","Birthday"])
    id1 = []
    todays_date = (todays_date == 'today') and datetime.today() or convert_str_date(todays_date)
    todays_date = todays_date.date()
    for id, v in p.indi.items():
        birth = v.get('BIRT')
        name = v.get('NAME')
        if birth is not None:
            birthday = K(birth).date()
            
            check_birth=(birthday-todays_date).days%yd < md
            if check_birth is True:
                x.add_row([id,name,birth])
                id1.append(id)
    p.log.append(['US38','BIRT',[x]])
    return id1


def us39_list_upcoming_anniversary(p, todays_date):
    x = PrettyTable(["ID","Husband","Wife","Anniversary"])
    id2 = []
    todays_date = (todays_date == 'today') and datetime.today() or convert_str_date(todays_date)
    todays_date = todays_date.date()

    for id, v in p.fam.items():
        marriage = v.get('MARR')
        hid = v.get('HUSB')
        hname = p.indi[hid].get('NAME')
        wid = v.get('WIFE')
        wname = p.indi[wid].get('NAME')
        if marriage is not None:
            anniversary_date =K(marriage).date()
            # todays_date=datetime.today().date()
            check_anniversary=(anniversary_date-todays_date).days%yd < md
            if check_anniversary is True:
                x.add_row([id,hname, wname, marriage])
                id2.append(id)
    p.log.append(['US39','ANNI',[x]])
    return id2

def main(path = "GEDCOM_File_withErrors.ged"):
    p=P.Parser()
    p.main(path)
    us21_correct_gender(p)
    us01_check_before_today(p)
    us02_birth_before_marriage(p)
    us03_birth_before_death(p)
    us35_birth_inlast_30days(p, today)
    us36_death_inlast_30days(p, today)
    us04_marriage_before_divorce(p)
    us05_marriage_before_death(p)
    us07_150_years_old(p)
    us08_birth_when_parent_married(p)
    us09_birth_before_parent_death(p)
    us10_marriage_after_14(p)
    us12_parent_not_too_old(p)
    us13_sibling_spacing(p)
    us38_list_upcoming_birthdays(p, today)
    us39_list_upcoming_anniversary(p, today)
    return p

if __name__ == '__main__':
    p=main('GEDCOM_File_withErrors.ged')
    p.log.sort(key=lambda x:x[0])
    print("INFO: Individual Table:")
    U.print_indi(p.indi)
    print("INFO: Family Table:")
    U.print_fam(p.fam, p.indi)
    U.print_log(p.log)
