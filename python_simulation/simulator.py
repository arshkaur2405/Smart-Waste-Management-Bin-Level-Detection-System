import csv
import os
import pandas as pd
from datetime import datetime

from python_simulation.data_generator import generate_distance
from python_simulation.config import *

# Maximum records to keep
MAX_RECORDS = 500


def calculate_fill(distance):

    fill = ((BIN_HEIGHT - distance) / BIN_HEIGHT) * 100

    return round(fill, 2)


def get_status(fill):

    if fill < WARNING_THRESHOLD:
        return "EMPTY"

    elif fill < FULL_THRESHOLD:
        return "HALF FULL"

    return "FULL"


def get_alert(fill):

    return "YES" if fill >= FULL_THRESHOLD else "NO"


def trim_csv():

    if not os.path.exists(CSV_FILE):
        return

    try:

        df = pd.read_csv(CSV_FILE)

        if len(df) > MAX_RECORDS:

            df = df.tail(MAX_RECORDS)

            df.to_csv(
                CSV_FILE,
                index=False
            )

    except Exception as e:

        print(
            f"CSV Trim Error: {e}"
        )


def save_record():

    distance = generate_distance()

    fill = calculate_fill(distance)

    status = get_status(fill)

    alert = get_alert(fill)

    timestamp = datetime.now()

    file_exists = os.path.exists(CSV_FILE)

    with open(
        CSV_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Timestamp",
                "Distance",
                "FillPercent",
                "Status",
                "Alert"
            ])

        writer.writerow([
            timestamp,
            distance,
            fill,
            status,
            alert
        ])

    # Keep only latest 500 records
    trim_csv()

    return {

        "distance": distance,

        "fill": fill,

        "status": status,

        "alert": alert

    }
    # ...