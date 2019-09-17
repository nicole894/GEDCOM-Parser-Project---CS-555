#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 2019-09-17 17:28:23
# @Author   : Mingyu Yao (myao4@stevens.edu)
# @Version  : 0.1.0
# @Description  : Pretty Table Utility

from prettytable import PrettyTable
import time
today = time.strftime("%Y %m %d").split(' ')
month=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


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
        DOB=date_format(v.get('BIRT').split(' '))
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
    
