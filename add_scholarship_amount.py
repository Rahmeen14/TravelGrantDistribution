import csv
import random
with open('data/conf.csv','r') as csvinput:
    with open('data/conf_scholarships.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('scholarship_amount')
        all.append(row)
        for row in reader:
            print row[4]
            if row[4] == '1' :
                row.append(2000+random.randint(500, 1000))
            if row[4] == '3' :
                row.append(1000+random.randint(100, 500))
            if row[4] == '5' :
                row.append(500+random.randint(50, 100))
            if row[4] == '7' :
                row.append(300+random.randint(0, 50))
            
            all.append(row)
        writer.writerows(all)