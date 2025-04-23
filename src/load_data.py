import pandas as pd
import sys
import os.path as osp

DATA_SUBDIR = '../data/'
DATA_SUBDIR = osp.abspath(DATA_SUBDIR)
if DATA_SUBDIR not in sys.path:
    sys.path.insert(1, DATA_SUBDIR)

class LoadData:
    """
    A class to load Finch app JSON export data for activities and mood.

    Parameters:
    -----------
    data_location : str
        Path to the folder containing the Finch export data.
    export_date : str
        The date of the export in YYYY-MM-DD format, used to locate subfolders.
    """
    def __init__(self, data_location, export_date):
        
        self.data_location = DATA_SUBDIR+data_location
        self.export_date = export_date
    
    def load_activity_data(self):
        """
        Load activity (Bullet) data from the Finch JSON export.

        Returns:
        --------
        pd.DataFrame
            A flattened DataFrame containing activity entries, with one row per activity.
        """
        activity_path = self.data_location + f"FinchExport_{self.export_date}/Bullet.json"
        activity_series = pd.read_json(activity_path, typ='series')
        activity_data = pd.json_normalize(activity_series.data)

        return activity_data

    def load_mood_data(self):
        """
        Load mood data from the Finch JSON export.

        Returns:
        --------
        pd.DataFrame
            A flattened DataFrame containing mood entries, including feeling, motivation, and satisfaction.
        """
        mood_path = self.data_location + f"FinchExport_{self.export_date}/Mood.json"
        mood_series = pd.read_json(mood_path, typ='series')
        mood_data = pd.json_normalize(mood_series.data)

        return mood_data
