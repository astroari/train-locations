import pandas as pd


def parse_eurologistic(df): # inform@eurologistic.su
    # df = pd.read_excel(path, header=None)
    
    # Build column names from rows 2 and 3 (merged header)
    row2 = df.iloc[2].fillna('')
    row3 = df.iloc[3].fillna('')
    names_to_remove = [5, 12, 14]
    for i in names_to_remove:
        row2.iloc[i]=''
    cols = [f"{a} {b}".strip() if b else a for a, b in zip(row2, row3)]
    data = df.iloc[4:].copy()
    data.columns = cols
    
    # Transform status sections into a status column
    statuses = data['Вагон'].where(pd.to_numeric(data.iloc[:, 0], errors='coerce').notna()==False).ffill()
    data['Статус'] = statuses
    
    # Keep only actual data rows: col 0 is a numeric wagon number
    data = data[pd.to_numeric(data.iloc[:, 0], errors='coerce').notna()]
    data = data.reset_index(drop=True)
    
    # Prep data for db
    columns_mapper = {
        "Вагон": "wagon_number",
        "Станция текущей дислокации": "current_location_station",
        "Оставшееся расстояние": "remaining_distance",
        "Станция назначения": "destination_station"
              }
    data.rename(columns=columns_mapper, inplace=True)
    data = data[["wagon_number", "current_location_station", "remaining_distance", "destination_station"]]
    data.fillna(value={"remaining_distance": 0}, inplace=True)

    return data.to_dict(orient="records")

def parse_railsoft(df): # stg-host-6@railsoft.ru
    # df = pd.read_excel(path, header=None)
    cols = df.iloc[1]
    
    data = df.iloc[2:].copy()
    data.columns = cols
    data = data.reset_index(drop=True)
    
    # Prep data for db
    columns_mapper = {
        "Номер вагона": "wagon_number",
        "Станция текущей дислокации": "current_location_station",
        "Расстояние осталось (от текущей станции)": "remaining_distance",
        "Станция назначения": "destination_station"
              }
    data.rename(columns=columns_mapper, inplace=True)
    data = data[["wagon_number", "current_location_station", "remaining_distance", "destination_station"]]
    data.fillna(value={"remaining_distance": 0}, inplace=True)

    return data.to_dict(orient="records")

def parse_incomtrans(df): # disl@incomtrans.su
    # df = pd.read_excel(path, header=None)
    cols = df.iloc[1]
    
    data = df.iloc[2:].copy()
    data.columns = cols
    data = data.reset_index(drop=True)
    
    # Prep data for db
    columns_mapper = {
        "Вагон": "wagon_number",
        "Ст. операц.": "current_location_station",
        "Раст": "remaining_distance",
        "Ст. назнач.": "destination_station"
              }
    data.rename(columns=columns_mapper, inplace=True)
    data = data[["wagon_number", "current_location_station", "remaining_distance", "destination_station"]]
    data.fillna(value={"remaining_distance": 0}, inplace=True)

    return data.to_dict(orient="records")

def parse_ilsi(df): # disl@ilsi.pro
    # df = pd.read_excel(path, header=None)
    cols = df.iloc[0]
    
    data = df.iloc[1:].copy()
    data.columns = cols
    data = data.reset_index(drop=True)
    
    # Prep data for db
    columns_mapper = {
        "Вагон": "wagon_number",
        "Ст. операц.": "current_location_station",
        "Раст": "remaining_distance",
        "Ст. назнач.": "destination_station"
              }
    data.rename(columns=columns_mapper, inplace=True)
    data = data[["wagon_number", "current_location_station", "remaining_distance", "destination_station"]]
    data.fillna(value={"remaining_distance": 0}, inplace=True)

    return data.to_dict(orient="records")

def parse_ultradecor(df): # e.mironova@ultradecor.com
    # df = pd.read_excel(path, header=None)
    
    cols = df.iloc[0]
    
    data = df.iloc[1:].copy()
    data.columns = cols
    data = data.reset_index(drop=True)
    
    # Prep data for db
    columns_mapper = {
        "Номер вагона": "wagon_number",
        "Станция операции": "current_location_station",
        "Расстояние до назначения (маршрута)": "remaining_distance",
        "Станция назначения": "destination_station"
              }
    data.rename(columns=columns_mapper, inplace=True)
    data = data[["wagon_number", "current_location_station", "remaining_distance", "destination_station"]]
    data.fillna(value={"remaining_distance": 0}, inplace=True)
    
    return data.to_dict(orient="records")