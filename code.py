import  MySQLdb
import sys
import csv

print("Enter password for the database:")
password = sys.stdin.readline()
print(password[:-1])
connectdata = {"user":"root","passwd":password[:-1], "host":"localhost", "db":"employees"}
try:
    conn=MySQLdb.connect(**connectdata)
    cur = conn.cursor()
    command = cur.execute("SHOW TABLES") 
    result =cur.fetchall()
except MySQLdb.Error:
    print("Connection failed")

else:
    print("success")
    dataTables = {}
    number = 1
    for entry in result:
        dataTables[number]= entry[0]
        number+=1
    

print("Enter the number of the table to access:")
for key in dataTables:
    print("%d -> %s" %(key,dataTables[key]))

choice = input()
tableReq = ""
try:
    tableReq = dataTables[choice]
    
except:
    print("Enter a valid number")
    
else:
    queryStatement = """DESCRIBE %s""" %tableReq
    command = cur.execute(queryStatement)
    results = cur.fetchall();
    entriesInTblSel = {};
    count =1;
    entriesInTbl =[]
    for result in results:
        entriesInTbl.append(result[0])
        entriesInTblSel[count] = result[0]
        print "%s-> %s" %(count,entriesInTblSel[count])
        
        count+=1
    choice = input("Enter the column number you want to sort the table by:")
    try:
        queryStatement = "SELECT * FROM %s ORDER BY %s" %(tableReq,entriesInTblSel[choice])
        command = cur.execute(queryStatement)
        results = cur.fetchall();
    except:
        print("Enter a valid number")
        
    else:
        resultFile = open("output.csv",'wb')
        # Create Writer Object
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(entriesInTbl)
        for result in results:
            wr.writerow(result)          
            #print(result)
        resultFile.close()
