import os
from serial import Serial
from time import sleep, time, strftime

TEMPS = [45, 50, 60]
#TEMPS = [0, 70]
REPETITIONS = 8
SLEEP_BETWEEN = 60


class Rubinstein(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=250000, timeout=0.25):
        self.serial = Serial(port=port, baudrate=baudrate, timeout=timeout)
        # FIXME don't know why initialization stops with this line
        while self.serial.readline() != 'echo:SD init fail\n':
            sleep(0.2)
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


rubinstein = Rubinstein()
#rubinstein.command('M114')

log_folder = strftime("%Y-%m-%d_%H%M")
os.mkdir(log_folder)

for temp in TEMPS:
    if temp != 0:
        # set bed temp, and wait
        rubinstein.command('M190 R{}'.format(int(temp)))
    else:
        # this is meant for cold bed only!
        #temp = 18  # TODO get temp from sensor!
        pass

    start_for_temp = time()

    for i in range(REPETITIONS):
        rubinstein.command('G28')
        zlevel = rubinstein.command('G29')
        # move slowly to center for better G28 next time
        rubinstein.command('G1 X0 Y0 F2000')
        fname = "zlevel_{}degC_after_{}s_{:02d}.log".format(
            temp, int(time() - start_for_temp), i)
        with open(os.path.join(log_folder, fname), 'w') as f:
            f.write(zlevel)

        # no need for sleeping without heat up
        if temp != 0:
            sleep(SLEEP_BETWEEN)
