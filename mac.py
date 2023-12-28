import subprocess
# ifconfig eth0 down
# ifconfig eth0 hw ether 00:00:00:00:00:01
# ifconfig eth0 up

class Mac_changer:
    def __init__(self):
        self.mac_address = None

    def get_mac_address(self, iface):
        output = subprocess.run(['ifconfig', iface], shell=False, capture_output=True)
        cmd_result = output.stdout.decode('utf-8').replace('\t','').split('\n')
        return cmd_result