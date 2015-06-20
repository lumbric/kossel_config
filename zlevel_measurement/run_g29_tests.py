from serial import Serial
from time import sleep, time


class Rubinstein(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=250000, timeout=0.25):
        self.serial = Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.busy = False

    def command(self, cmd, timeout=float('inf')):
        # FIXME needs mutex!
        if self.busy or self.serial.read():
            raise RuntimeError("busy")
        self.busy = True
        self.serial.write("{}\n".format(cmd))
        response = ''
        start = time()
        while time() - start < timeout:
            sleep(0.2)
            line = self.serial.readline()
            if line == 'ok\n':
                # FIXME missing try/finally for busy=False
                self.busy = False
                return response
            if len(line) > 0:
                print line,
            response += line
        else:
            raise RuntimeError(
                "timeout when waiting for command {}".format(cmd))


TEMPS = [50, 70]
REPETITIONS = 3
SLEEP_BETWEEN = 120

rubinstein = Rubinstein()
rubinstein.command('M114')

for temp in TEMPS:
    for i in range(REPETITIONS):
        # set bed temp, and wait
        rubinstein.command('M190 R{}'.format(int(temp)))

        rubinstein.command('G28')
        zlevel = rubinstein.command('G29')
        # move slowly to center for better G28 next time
        rubinstein.command('G1 X0 Y0 F2000')

        with open("zlevel_log_temp{}.log".format(temp), 'w') as f:
            f.write(zlevel)

        sleep(SLEEP_BETWEEN)
