from python_simulation.simulator import save_record
import time

print("Smart Waste Management System Started...\n")

while True:

    result = save_record()

    print(
        f"""
========================================
Distance : {result['distance']} cm
Fill     : {result['fill']} %
Status   : {result['status']}
Alert    : {result['alert']}
========================================
"""
    )

    time.sleep(5)