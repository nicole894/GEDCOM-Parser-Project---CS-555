
from dateutil.parser import parse

api_version = 200

class Parser():
    _fam = {}
    _ind = {}
    _log = []

    @property
    def fam(self):
        return self._fam

    @property
    def indi(self):
        return self._ind

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, xlog):
        self._log = xlog

    def export_props(self):
        return self.indi, self.fam, self.log

    #=======================================#

    def validate_file(self, path):
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
    
    def create_data(self, counter, content_list, id):
        def us42_reject_illegitimate_dates(dates):
            "Rejects illegitimate dates"
            _flag = False
            try:
                parse(dates)
            except ValueError:
                _flag = True
            return _flag
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
                 if us42_reject_illegitimate_dates(date):
                    self.log.append(["US42",each_data[1],[id, date]])
                 else:
                    data_dict.update({each_data[1]: date})
        return data_dict
    
    def build_data_dict(self, path):
        def US22_unique_ids(i):
            data_dict =self.indi if i[2]=='INDI' else self.fam
            if i[1] in data_dict.keys(): #Tag US22
                self.log.append(["US22",i[2],[i[1]]])
            else:
                data_dict.update({i[1]:data})
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
                    data = self.create_data(counter, content_list, i[1])
                    US22_unique_ids(i)
                elif int(i[0]) == 0 and len(i) == 3 and i[2] == 'FAM':
                    data = self.create_data(counter, content_list, i[1])
                    US22_unique_ids(i)
                counter = counter + 1
                fp.close()

    def main(self, path = "GEDCOM_File_withErrors.ged"):        
        self.validate_file(path)
        self.build_data_dict(path)
