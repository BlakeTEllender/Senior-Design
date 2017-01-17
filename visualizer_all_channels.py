import os
import platform
import time
import numpy as np
import matplotlib.pyplot as plt
system_platform = platform.system()
import socket  # Needed to prevent gevent crashing on Windows. (surfly / gevent issue #459)
import pywinusb.hid as hid
import gevent
from Crypto.Cipher import AES
from Crypto import Random
from gevent.queue import Queue
from subprocess import check_output

# How long to gevent-sleep if there is no data on the EEG.
# To be precise, this is not the frequency to poll on the input device
# (which happens with a blocking read), but how often the gevent thread
# polls the real threading queue that reads the data in a separate thread
# to not block gevent with the file read().
# This is the main latency control.
# Setting it to 1ms takes about 10% CPU on a Core i5 mobile.
# You can set this lower to reduce idle CPU usage; it has no effect
# as long as data is being read from the queue, so it is rather a
# "resume" delay.
DEVICE_POLL_INTERVAL = 0.001  # in seconds

sensor_bits = {
    'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
    'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
    'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
    'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
    'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
    'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
    'O2': [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
    'P8': [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
    'T8': [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
    'F8': [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
    'AF4': [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
    'FC6': [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
    'F4': [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
}

g_battery = 0
tasks = Queue()


def get_level(data, bits):
    """
    Returns sensor level value from data using sensor bit mask in micro volts (uV).
    """
    level = 0
    for i in range(13, -1, -1):
        level <<= 1
        b, o = (bits[i] / 8) + 1, bits[i] % 8
        level |= (ord(data[b]) >> o) & 1
    return level


def get_linux_setup():
    """
    Returns hidraw device path and headset serial number.
    """
    raw_inputs = []
    for filename in os.listdir("/sys/class/hidraw"):
        real_path = check_output(["realpath", "/sys/class/hidraw/" + filename])
        split_path = real_path.split('/')
        s = len(split_path)
        s -= 4
        i = 0
        path = ""
        while s > i:
            path = path + split_path[i] + "/"
            i += 1
        raw_inputs.append([path, filename])
    for input in raw_inputs:
        try:
            with open(input[0] + "/manufacturer", 'r') as f:
                manufacturer = f.readline()
                f.close()
            if "Emotiv Systems" in manufacturer:
                with open(input[0] + "/serial", 'r') as f:
                    serial = f.readline().strip()
                    f.close()
                print "Serial: " + serial + " Device: " + input[1]
                # Great we found it. But we need to use the second one...
                hidraw = input[1]
                hidraw_id = int(hidraw[-1])
                # The dev headset might use the first device, or maybe if more than one are connected they might.
                hidraw_id += 1
                hidraw = "hidraw" + hidraw_id.__str__()
                print "Serial: " + serial + " Device: " + hidraw + " (Active)"
                return [serial, hidraw, ]
        except IOError as e:
            print "Couldn't open file: %s" % e



class EmotivPacket(object):
    """
    Basic semantics for input bytes.
    """

    def __init__(self, data, sensors, model):
        """
        Initializes packet data.
        Updates each sensor with current sensor value from the packet data.
        """
        self.raw_data = data
        self.counter = ord(data[0])
        if self.counter > 127:
            self.counter = 128
        self.sync = self.counter == 0xe9
        for name, bits in sensor_bits.items():
            # Get Level for sensors subtract 8192 to get signed value
            value = get_level(self.raw_data, bits) - 8192
            setattr(self, name, (value,))
            sensors[name]['value'] = value
        self.old_model = model
        #self.handle_quality(sensors)
        self.sensors = sensors


    def __repr__(self):
        """
        Returns custom string representation of the Emotiv Packet.
        """
        return 'EmotivPacket(counter=%i)' % (
            self.counter)



class Emotiv(object):
    """
    Receives, decrypts and stores packets received from Emotiv Headsets.
    """

    def __init__(self, display_output=True, serial_number="", is_research=False):
        """
        Sets up initial values.
        """
        self.running = True
        self.packets = Queue()
        self.packets_received = 0
        self.packets_processed = 0
        self.battery = 0
        self.display_output = display_output
        self.is_research = is_research
        self.sensors = {
            'F3': {'value': 0, 'quality': 0},
            'FC6': {'value': 0, 'quality': 0},
            'P7': {'value': 0, 'quality': 0},
            'T8': {'value': 0, 'quality': 0},
            'F7': {'value': 0, 'quality': 0},
            'F8': {'value': 0, 'quality': 0},
            'T7': {'value': 0, 'quality': 0},
            'P8': {'value': 0, 'quality': 0},
            'AF4': {'value': 0, 'quality': 0},
            'F4': {'value': 0, 'quality': 0},
            'AF3': {'value': 0, 'quality': 0},
            'O2': {'value': 0, 'quality': 0},
            'O1': {'value': 0, 'quality': 0},
            'FC5': {'value': 0, 'quality': 0},
        }

        self.serial_number = serial_number  # You will need to set this manually for OS X.
        self.old_model = False


    def setup(self):
        """
        Runs setup function depending on platform.
        """
        if system_platform == "Windows":
            self.setup_windows()


    def setup_windows(self):
        """
        Setup for headset on the Windows platform.
        """
        devices = []
        try:
            devicesUsed = 0
            for device in hid.find_all_hid_devices():
                print "Product name " + device.product_name
                print "device path " + device.device_path
                print "instance id " + device.instance_id
                print "\r\n"
                useDevice = ""


                if device.product_name == 'EEG Signals':

                    print "\n" + device.product_name + " Found!\n"
                    useDevice = raw_input("Use this device? [Y]es? ")

                    if useDevice.upper() == "Y":
                        devicesUsed += 1
                        devices.append(device)
                        device.open()
                        self.serial_number = device.serial_number
                        device.set_raw_data_handler(self.handler)
                elif device.product_name == 'Brain Computer Interface USB Receiver/Dongle':

                    print "\n" + device.product_name + " Found!\n"
                    useDevice = raw_input("Use this device? [Y]es? ")
                    if useDevice.upper() == "Y":
                        devicesUsed += 1
                        devices.append(device)
                        device.open()
                        self.serial_number = device.serial_number
                        device.set_raw_data_handler(self.handler)

                elif device.product_name == 'Emotiv RAW DATA':

                    print "\n" + device.product_name + " Found!\n"
                    useDevice = raw_input("Use this device? [Y]es? ")

                    if useDevice.upper() == "Y":
                        devicesUsed += 1
                        devices.append(device)
                        device.open()
                        self.serial_number = device.serial_number
                        device.set_raw_data_handler(self.handler)

            print "\n\n Devices Selected: " + str(devicesUsed)
            crypto = gevent.spawn(self.setup_crypto, self.serial_number)
            console_updater = gevent.spawn(self.update_console)
            raw_input("Press Enter to continue...")
            while self.running:
                try:
                    gevent.sleep(0)

                except KeyboardInterrupt:
                    self.running = False
        finally:
            for device in devices:
                device.close()

            gevent.kill(crypto, KeyboardInterrupt)
            gevent.kill(console_updater, KeyboardInterrupt)

    def handler(self, data):
        """
        Receives packets from headset for Windows. Sends them to a Queue to be processed
        by the crypto greenlet.
        """
        assert data[0] == 0
        tasks.put_nowait(''.join(map(chr, data[1:])))
        self.packets_received += 1
        return True


    def setup_crypto(self, sn):
        """
        Performs decryption of packets received. Stores decrypted packets in a Queue for use.
        """
        print self.old_model
        k = ['\0'] * 16
        k[0] = sn[-1]
        k[1] = '\0'
        k[2] = sn[-2]
        if self.is_research:
            k[3] = 'H'
            k[4] = sn[-1]
            k[5] = '\0'
            k[6] = sn[-2]
            k[7] = 'T'
            k[8] = sn[-3]
            k[9] = '\x10'
            k[10] = sn[-4]
            k[11] = 'B'
        else:
            k[3] = 'T'
            k[4] = sn[-3]
            k[5] = '\x10'
            k[6] = sn[-4]
            k[7] = 'B'
            k[8] = sn[-1]
            k[9] = '\0'
            k[10] = sn[-2]
            k[11] = 'H'
        k[12] = sn[-3]
        k[13] = '\0'
        k[14] = sn[-4]
        k[15] = 'P'
        key = ''.join(k)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_ECB, iv)
        for i in k:
            print "0x%.02x " % (ord(i))
        while self.running:
            while not tasks.empty():
                task = tasks.get()
                try:
                    data = cipher.decrypt(task[:16]) + cipher.decrypt(task[16:])
                    self.packets.put_nowait(EmotivPacket(data, self.sensors, self.old_model))
                    self.packets_processed += 1
                except:
                    pass
                gevent.sleep(0)
            gevent.sleep(0)

    def dequeue(self):
        """
        Returns an EmotivPacket popped off the Queue.
        """
        try:
            return self.packets.get()
        except Exception, e:
            print e

    def close(self):
        """
        Shuts down the running greenlets.
        """
        self.running = False

    def update_console(self):
        """
        Greenlet that outputs sensor values to the console and stores values in csv file.
        """
        count = 0 #initializing values
        t_curr = 0
        cycles = 1
        last_tme = 1

        x1 = 0
        x2 = 20

#electrode names: (F3, F4, P7, FC6, F7, F8, T7, P8, FC5, AF4, T8, O2, O1, AF3)

        f, (F3, F4, P7, FC6, F7, F8, T7,P8,FC5,AF4,T8,O2,O1,AF3) = plt.subplots(14, sharex=True, sharey=True)
        plt.axis([x1, x2, -10, 10])
        f.set_size_inches(18, 10, forward=True)
        f.subplots_adjust(hspace=0)
        F3.set_title('Time Domain')
        P7.set_xlabel('Time(s)')
        F3.set_ylabel('F3')
        F4.set_ylabel('F4')
        P7.set_ylabel('P7')
        FC6.set_ylabel('FC6')
        F7.set_ylabel('F7')
        F8.set_ylabel('F8')
        T7.set_ylabel('T7')
        P8.set_ylabel('P8')
        FC5.set_ylabel('FC5')
        AF4.set_ylabel('AF4')
        T8.set_ylabel('T8')
        O2.set_ylabel('O2')
        O1.set_ylabel('O1')
        AF3.set_ylabel('AF3')

        if self.display_output:
            while self.running:
                os.system('cls')
                count += 1
                counter = [count]
                t = time.clock()
                t_curr = int(t)
                if t_curr == last_tme:
                    samp_freq = [cycles]
                    cycles = 1
                    last_tme = t_curr + 1
                else:
                    samp_freq = ['']
                    cycles = cycles +1
                current_line = [int(self.sensors[k[1]]['value']) for k in enumerate(self.sensors)]
                line_wrt =  samp_freq + counter + [t] + current_line
                print(line_wrt)
                plt.ion()

                y1 = current_line[0]
                y2 = current_line[1]
                y3 = current_line[2]
                y4 = current_line[3]
                y5 = current_line[4]
                y6 = current_line[5]
                y7 = current_line[6]
                y8 = current_line[7]
                y9 = current_line[8]
                y10 = current_line[9]
                y11 = current_line[10]
                y12 = current_line[11]
                y13 = current_line[12]
                y14 = current_line[13]

                F3.scatter(t,y1)
                F4.scatter(t,y2)
                P7.scatter(t,y3)
                FC6.scatter(t,y4)
                F7.scatter(t,y5)
                F8.scatter(t,y6)
                T7.scatter(t,y7)
                P8.scatter(t,y8)
                FC5.scatter(t,y9)
                AF4.scatter(t,y10)
                T8.scatter(t,y11)
                O2.scatter(t,y12)
                O1.scatter(t,y13)
                AF3.scatter(t,y14)

                plt.pause(.001)

                if t > 18:
                    x1 = (t_curr)-17
                    x2 = (t_curr)+3

                plt.axis([x1, x2, -10, 10])
                plt.show()

                gevent.sleep(0)


if __name__ == "__main__":
    a = Emotiv()
    try:
        a.setup()
    except KeyboardInterrupt:
        a.close()
