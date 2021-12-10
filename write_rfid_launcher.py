from FakeDevices import *
import logging

# AttributeError: module 'logging' has no attribute 'getlogger
log = logging.getLogger (__name__)

try:
    gui = Gui()
    gui.add(MifareRfid('testcards.json'))
    from write_rfid import *

except:
    log.exception('------------log-----------')
    
gui.quit()
print('Program terminated')