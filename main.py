import time
import datetime
import subprocess
from luma.core.render import canvas
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

def main():
    serial = i2c(port=1, address=0x3C)

    device = sh1106(serial)

    padding = 2

    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")

            cmd = "date +'%H:%M:%S - %d %b %Y'"
            date = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "hostname"
            hostname = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

            # Write four lines of text.

            draw.text((padding, padding + 0), date, fill=255)
            draw.text((padding, padding + 10), "Hostname: " + hostname, fill=255)
            draw.text((padding, padding + 20), "IP: " + IP, fill=255)
            draw.text((padding, padding + 30), CPU, fill=255)
            draw.text((padding, padding + 40), MemUsage, fill=255)
            draw.text((padding, padding + 50), Disk, fill=255)

            time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
