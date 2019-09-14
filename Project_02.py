def file_reader(path):
    """Read the contains of file"""
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("File not found : ",path )
    else:
        with fp:
            for line in fp:
                print("-->",line.strip("\n"))
                tokens = line.split() 
                if (len(tokens) == 3 and tokens[0] == '0' and (tokens[2] == 'INDI' or tokens[2] == "FAM")):
                    print(f"<--{tokens[0]}|{tokens[2]}|Y|{tokens[1]}")
                
                else:
                    tags = {'0' : ["HEAD", "TRLR", "NOTE"],
                    '1' : ["NAME","SEX","BIRT","DEAT", "FAMC","FAMS","MARR", "HUSB", "WIFE","CHIL", "DIV"],
                    '2' : ["DATE"]}
                    level = tokens[0]
                    tag = tokens[1]
                    argument = " ".join(tokens[2:])

                    if level in tags and tag in tags[level]:
                        print(f"<--{level}|{tag}|Y|{argument}")
                    else:
                        print(f"<--{level}|{tag}|N|{argument}")







                        

                
                    
        
            
            


                    
                    