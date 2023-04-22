import time
import sys
sys.path.append('./drive')
import SPI
import SSD1305

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = 22     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware SPI:
disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
time.sleep(2)

# Set font to use
font = ImageFont.truetype('04B_08__.TTF',8)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('04B_08__.TTF',8)
counter = 0


while True:

    try:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "/usr/bin/vcgencmd measure_temp"
        Temp = subprocess.check_output(cmd, shell = True)
        cmd = 'date +"%T"'
        Time = subprocess.check_output(cmd, shell = True )

        # Write two lines of text.
        draw.text((x, top),       "IP: " + str(IP.decode('utf-8')),  font=font, fill=255)
        draw.text((x, top+8),    str(MemUsage.decode('utf-8')),  font=font, fill=255)
        draw.text((x, top+16),     str(Temp.decode("utf-8")),  font=font, fill=255)
        draw.text((x, top+25),       "DOCKERPI ::: " + str(Time.decode("utf-8")),  font=font, fill=255)

        # Display image.
        
        if counter < 30:
            disp.image(image)
            disp.display()
            time.sleep(.1)
            counter += 1
            
        elif counter < 60:


            draw.rectangle((0,0,width,height), outline=0, fill=0)


            #Sida2
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            cmd = 'date +"%T"'
            Time = subprocess.check_output(cmd, shell = True )
            cmd = 'date +"%A %d %B"'
            datum = subprocess.check_output(cmd, shell = True)
            

            draw.text((x, top),    str(Disk.decode('utf-8')),  font=font, fill=255)
            draw.text((x, top+8),    "~~~~~~~~~~~~~~~~~~~",  font=font, fill=255)
            draw.text((x, top+16),    str(datum.decode("utf-8")),  font=font, fill=255)
            draw.text((x, top+25),     "DOCKERPI ::: " + str(Time.decode("utf-8")),  font=font, fill=255)


            disp.image(image)
            disp.display()
            time.sleep(.1)
            counter += 1
        else:

            draw.rectangle((0,0,width,height), outline=0, fill=0)


            #Sida3| 
            cmd = 'date +"%T"'
            Time = subprocess.check_output(cmd, shell = True )
            cmd = 'date +"%A %d %B"'
            datum = subprocess.check_output(cmd, shell = True)
            cmd = "service docker status | grep active | awk '{print $2 $3}'"
            Docker = subprocess.check_output(cmd, shell = True)
            cmd = "uptime | awk '{print $3 $4 $5}'"
            upTime = subprocess.check_output(cmd, shell = True)


            draw.text((x, top),       "Uptime: " + str(upTime.decode("utf-8")),  font=font, fill=255)
            draw.text((x, top+8),     str(Docker.decode("utf-8")),  font=font, fill=255)
            draw.text((x, top+16),    "~~~~~~~~~~~~~~~~~~~",  font=font, fill=255)
            draw.text((x, top+25),    "DOCKERPI ::: " + str(Time.decode("utf-8")),  font=font, fill=255)

            disp.image(image)
            disp.display()
            time.sleep(.1)
            counter += 1
            if counter > 90:
                counter = 0
            else:
                pass

    except(KeyboardInterrupt):
        print("\n")
        break