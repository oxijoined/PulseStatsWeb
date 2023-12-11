import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle


class Pulse:
    def __init__(
        self,
        date,
        type,
        sourceName,
        sourceVersion,
        device,
        unit,
        creationDate,
        startDate,
        endDate,
        value,
    ):
        self.date = date
        self.type = type
        self.sourceVersion = sourceVersion
        self.unit = unit
        self.creationDate = creationDate
        self.startDate = startDate
        self.endDate = endDate
        self.value = float(value)


def read_apple_health_xml(file_path):
    pulse_records = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    for record in root.findall(".//Record"):
        if record.get("type") == "HKQuantityTypeIdentifierHeartRate":
            print(record.get("creationDate"))
            pulse = Pulse(
                date=pd.to_datetime(record.get("creationDate")),
                type=record.get("type"),
                sourceName=record.get("sourceName"),
                sourceVersion=record.get("sourceVersion"),
                device=record.get("device"),
                unit=record.get("unit"),
                creationDate=record.get("creationDate"),
                startDate=record.get("startDate"),
                endDate=record.get("endDate"),
                value=record.get("value"),
            )
            pulse_records.append(pulse)

    return pulse_records


# Считывание данных о пульсе
pulse_records = read_apple_health_xml("export.xml")

# Преобразование данных в DataFrame
data = pd.DataFrame([vars(pulse) for pulse in pulse_records])

# Сохранение данных в pickle файл
with open("pulse_data.pickle", "wb") as f:
    pickle.dump(data, f)
