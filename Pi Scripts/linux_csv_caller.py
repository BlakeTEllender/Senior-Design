import emotiv_linux_csv_working
from emotiv_linux_csv_working import Emotiv

t = Emotiv()
t.setup()
while True:
    t.update_console()
