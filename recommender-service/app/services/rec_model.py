from datetime import datetime
import os
from re import X
import pandas as pd
import numpy as np

from app.schemas import DeviceRecordSchema, DeviceSchema, SceneRecSchema

DATA_FOLDER_NAME = "recommender_data"
os.makedirs(DATA_FOLDER_NAME, exist_ok=True)

class RecModel:

    def __init__(self):
        self._is_trained : bool = False
        self._model = None
        self._data = pd.DataFrame() 

        #Data is limited to two weeks; loading it into memory
        csv_files = [f for f in os.listdir(DATA_FOLDER_NAME) if f.endswith(".csv")]
        if csv_files:
            latest_csv = max(
                [os.path.join(DATA_FOLDER_NAME, f) for f in csv_files],
                key=os.path.getmtime,
            )
            self._data = pd.read_csv(latest_csv)

    def update_data(self, records: list[DeviceRecordSchema], devices: list[DeviceSchema]):
        if not records or not devices:
            return

        device_types_by_id = {dev._id: dev.type for dev in devices}
        device_names_by_id = {dev._id: dev.name for dev in devices}

        records_dicts = [record.model_dump() for record in records]
        self._data = pd.DataFrame(records_dicts)
        self._data["type"] = self._data["device_id"].map(device_types_by_id)
        self._data["device_id"] = self._data["device_id"].replace(device_names_by_id)
        self._data["timestamp"] = pd.to_datetime(self._data["timestamp"], errors='coerce')
        self._preprocess_data()
        self._store_data(delete_older=True)

    #Pending
    def fit_data(self):
        if self._data is None or self._data.empty:
            raise ValueError("Empty data to model training")
       
        model = None

        self._model = model
        self._is_trained = True

    #To-do: Implementar o algoritmo de recomendação de cenas
    def recommend(self) -> list[SceneRecSchema]:
        if not self._is_trained:
            self.fit_data()

        recommendations = []

        return recommendations


    def _preprocess_data(self):
        # feature/target device distinguishment
        self._data['device_id'] = np.where(
            self._data['type'] == 'sensor',
            "X_" + self._data['device_id'].astype(str),
            "Y_" + self._data['device_id'].astype(str)
        )

        #build the home global state
        states = {state: 0 for state in self._data["device_id"].unique()}
        new_data = []
        for _, row in self._data.iterrows():
            states[row['device_id']] =row['value']
            new_row = {"timestamp": row['timestamp'], **states}
            new_data.append(new_row) 
        new_df = pd.DataFrame(new_data)

        #Forward Fill strategy, 1 minute
        new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
        new_df = new_df.set_index('timestamp')
        new_df = new_df.resample('1min').ffill()
        new_df = new_df.iloc[1:]
        new_df = new_df.reset_index()

        cols_to_parse_int = [x for x in new_df.columns if x!= 'timestamp']
        new_df[cols_to_parse_int] = new_df[cols_to_parse_int].astype(int)

        #Creates days and hours columns. Used only in non-sequential models
        new_df['hour'] = new_df['timestamp'].apply(lambda x: x.hour)
        new_df = pd.get_dummies(new_df,columns=['hour'],prefix='H', dtype=int, drop_first=True)
        days = ['mon','tue','wed','thu','fri','sat','sun']
        new_df['day'] = new_df['timestamp'].apply(lambda x: days[x.weekday()])
        new_df = pd.get_dummies(new_df,columns=['dia'],prefix='dia', dtype=int, drop_first=True)

        self._data = new_df
        self._is_trained = False

    def _store_data(self, delete_older = True):
        if delete_older:
            for file in os.listdir(DATA_FOLDER_NAME):
                if file.endswith(".csv"):
                    os.remove(os.path.join(DATA_FOLDER_NAME, file))

        time_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._data.to_csv(f"{DATA_FOLDER_NAME}/{time_file_name}.csv", index=False)
        
