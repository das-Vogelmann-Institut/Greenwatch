import time
import psutil
from notifypy import Notify

# Credits to https://stackoverflow.com/a/36397520

"""
Each GB of data you download results in 3kg of CO2 emissions. https://www.emergeinteractive.com/insights/detail/does-irresponsible-web-development-contribute-to-global-warming/
"""
GB_to_CO2 = 3

def main():
    old_value = 0  
    converted_value = 0
    total_kg_usage = 0

    while True:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        if old_value:
            new_converted_value = send_stat(new_value - old_value)
            converted_value = converted_value + new_converted_value
            if converted_value > 8 : # I Gbit = 0.125 GB
                # source for count https://www.fastcompany.com/90171268/internet_impact_visualized
                print("gotcha!!")
                total_kg_usage = total_kg_usage + 1
                notification = Notify()
                notification.title = "Greenwatch"
                notification.message = f"U have just used {GB_to_CO2} KG of CO2. Total KGs used since start of Greenwatch: {total_kg_usage*GB_to_CO2}"
                #notification.icon = "path/to/icon.png"
                #notification.audio = "path/to/audio/file.wav"
                notification.send()
                converted_value = 0


        old_value = new_value
        time.sleep(1)

def convert_to_gbit(value):
    return value/1024./1024./1024.*8

def send_stat(value):
    converted_value =  convert_to_gbit(value)
    print(format(converted_value,".3f") + " gbit used")
    return converted_value

main()
