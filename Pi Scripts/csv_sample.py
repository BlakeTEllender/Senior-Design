import csv

csv_name = raw_input("Enter name for csv file '<name>.csv':  \n")
with open (csv_name, 'ab') as fp:
    wr = csv.writer(fp,delimiter= ',')
    lead_names = ('Sampling Freq:','Counter:','Time:', 'F3:', 'F4:', 'P7:', 'FC6:', 'F7:', 'F8:', 'T7:',
                          'P8:', 'FC5:', 'AF4:', 'T8:','O2:', 'O1:', 'AF3:')
    #test_line = [0,0,0,0,0,0,]
    wr.writerow(lead_names)
    fp.close()
    
