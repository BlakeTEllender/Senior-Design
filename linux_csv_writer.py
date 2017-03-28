#test csvwriter_linux
import csv
import time

class woohoo(object):
    def __init__(self):
        self.csv_name = 'holder1.csv'
        
    def update_console(self,csv_name):
        print ('gets to update_console')
        """
        Greenlet that outputs sensor, gyro and battery values once per second to the console.
        """ 
        count = 0 #initializing values
        T = time.time()
        t_curr = 0
        cycles = 1
        last_tme = 1
        epoc_time = 3 #desired length of epoc[sec]
        #csv_name = 'holder1.csv'

        epoc = []

        if self.display_output:
            while self.running:
                count += 1
                counter = [count]
                t = time.time() - T
                t_curr = int(t)
                #current_line = [int(self.sensors[k[1]]['value']) for k in enumerate(self.sensors)]
                #line_wrt = counter + [t] + current_line
                line_wrt = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                print(line_wrt)
                if t_curr >= epoc_time:
                    self.csv_name = 'holder2.csv'
                    return self.csv_name
                else:
                    with open(csv_name, 'ab') as fp:
                        wr = csv.writer(fp,delimiter=',')
                        wr.writerow(linel_wrt)
                        fp.close()
                    
        gevent.sleep(0)

    def setup(self):
        runner = update_console(csv_name)
        print csv_name
        
        
