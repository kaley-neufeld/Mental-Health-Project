import pandas as pd

class LoadData:
    # data_location is folder containing exported JSON files
    # export_data in string format YYYY-MM-DD
    def __init__(self, data_location, export_date):
        self.data_location = data_location
        self.export_date = export_date
    
    # load activity data as JSON from local folder and return Pandas df
    def load_activity_data(self):
        # load data
        activity_filename = '/Bullet.json'
        activity_data_location = self.data_location+'FinchExport_'+self.export_date+activity_filename
        
        # read JSON and convert to flat dataframe
        activity_series = pd.read_json(activity_data_location, typ='series')
        activity_data = pd.json_normalize(activity_series.data)

        return activity_data

    # load mood data as JSON from local folder and return Pandas df
    def load_mood_data(self):
        # load data
        mood_filename = '/Mood.json'
        mood_data_location = self.data_location+'FinchExport_'+self.export_date+mood_filename

        # read JSON and convert to flat dataframe
        mood_series = pd.read_json(mood_data_location, typ='series')
        mood_data = pd.json_normalize(mood_series.data)

        return mood_data
