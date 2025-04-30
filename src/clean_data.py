import pandas as pd
from datetime import datetime, timedelta, date
import sys
import os.path as osp

# Setup project root and config
ROOT_PATH = osp.abspath('../')
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)
    
from project_config import CONFIG

# Config variables
DATE_COL = CONFIG["raw_date_col_name"]
MORNING_SHIFT_HOURS = CONFIG["morning_cutoff_hour"]
RAW_DATE_FORMAT = CONFIG["raw_date_format"]

# -----------------------
# Helper Functions
# -----------------------

def safe_parse(x):
    """Safely parse a raw date string to datetime, or return NaT if invalid"""
    if not x or x.strip() == "":
        return pd.NaT
    try:
        return datetime.strptime(x.strip(), RAW_DATE_FORMAT)
    except ValueError:
        print(f"Unparseable date: {x}")
        return pd.NaT

def to_datetime(df):
    """Apply safe_parse to the configured date column and add 'Record_Datetime'."""
    df['Record_Datetime'] = df[DATE_COL].map(safe_parse)
    return df

# -----------------------
# Cleaner Class
# -----------------------

class CleanData:
    """Class for cleaning and transforming mood and activity data."""
    
    def __init__(self):
        pass

    def clean_mood_data(self, df):
        """
        Clean mood data and return one row per day, with average or daily values for each mood type.
        """
        df['value'] = pd.to_numeric(df['value'])
        
        df = to_datetime(df)
        df = df.drop([DATE_COL,'updated_time'],axis=1)

        # Time adjustment for early morning entries
        time_shift = timedelta(hours=MORNING_SHIFT_HOURS)
        df['Adjusted_Datetime'] = df['Record_Datetime'] - time_shift
        df['Record_Date'] = df['Adjusted_Datetime'].dt.date
        
        # cut off the last day because usually the export date isn't a completed day
        start_date = df['Record_Date'].min()
        end_date = df['Record_Date'].max() - timedelta(days=1)
        all_days = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Aggregate per mood type
        dfs = {}
        for mood_type in ('feeling','satisfaction','motivation'):
            type_df = df[df['mood_type'] == mood_type].copy()
            
            if mood_type == 'feeling':
                agg_df = type_df.groupby('Record_Date')['value'].mean()
            else:
                # TODO: these should only have 1 value a day, shouldn't do first!
                agg_df = type_df.groupby('Record_Date')['value'].first() 
            
            # Reindex to full date range
            agg_df = agg_df.reindex(all_days)
            agg_df.name = mood_type
            dfs[mood_type] = agg_df
            
        # Combine all mood types into one dataframe
        mood_df = pd.concat(dfs.values(), axis=1)
        mood_df.index.name = 'Record_Date'
        mood_df = mood_df.reset_index()
        mood_df = mood_df.rename(columns={'feeling':'average_feeling'})
        
        return mood_df
        
    def clean_activity_data(self, df):
        """
        Clean and standardize activity data: format dates, remove duplicates, filter relevant activities.
        """
        df = to_datetime(df)
        df['Record_Date'] = df['Record_Datetime'].dt.date
        
        # filtering relevant columns
        df = df[['Record_Date','bullet_type','text','bullet_status']]
        df = df.query("bullet_type == 1")
        df = df.drop('bullet_type',axis=1)
        
        # cleaning text
        df['text'] = df['text'].str.replace("#","")
        
        # replace {old_name: new name}
        duplicates_dict = {
            "Laundry":"Start a load of laundry",
            "Walk around the neighborhood":"Mindfulness Walk",
            "Make a gratitude list before sleeping":"Gratitude Jar",
            "Reflect on how friends makes me feel gratitude lately":"Gratitude Jar",
            "Express gratitude to a friend I'm thankful for":"Gratitude Jar"
        }
        df['text'] = df['text'].replace(duplicates_dict)
        
        return df