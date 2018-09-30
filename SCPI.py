# wykys 2017
# HMO1002 SCPI - Standard Commands for Programmable Instruments

from HMO1002 import HMO1002


class SCPI(HMO1002):
    """ Standard Commands for Programmable Instruments """

    def __init__(self):
        """ initialization """
        super().__init__()

    def autoscale(self):
        """ set autoscale """
        self.send_cmd('AUToscale')

    def screenshot(self, name='img', color='color'):
        """ download screenshot """
        self.send_cmd('STOP')
        self.send_cmd('HCOPy:FORMat PNG')

        if color == 'color':
            self.send_cmd('HCOPy:COLOR:SCHeme COLor')
        elif color == 'gray':
            self.send_cmd('HCOPy:COLOR:SCHeme GRAYscale')
        else:
            self.send_cmd('HCOPy:COLOR:SCHeme INVerted')

        self.send_cmd('HCOPy:DATA?')

        if chr(self.read_byte()) != '#':
            log.err('# not found')
            exit(1)

        size_len = self.read_byte()
        if size_len == None:
            log.err('no data')
            exit(1)
        size_len = int(size_len - ord('0'))

        bytes_len = []
        for i in range(size_len):
            tmp = self.read_byte()
            if tmp == None:
                log.err('no data')
                exit(1)
            bytes_len.append(tmp)
        bytes_len = int(bytes(bytes_len), 10)

        img = []
        for i in range(bytes_len):
            tmp = self.read_byte()
            if tmp == None:
                log.err('no data')
                exit(1)
            img.append(tmp)
        img = bytes(img)

        fw = open(name + '.png', 'wb')
        fw.write(img)
        fw.close()

        self.send_cmd('RUN')

    def function_generator(self, freq):
        """ set function generator """
        self.send_cmd('GENerator:FREQuency {:e}'.format(float(freq)))
