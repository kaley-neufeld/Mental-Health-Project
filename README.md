### Overview
This project explores the relationship between self-care activities and emotional well-being, using personal self-tracking data collected over time through Finch Self-Care App [https://finchcare.com/]. The aim is to better understand which behaviors (like yoga, meditation, eating meals, or taking mindful walks) have a measurable impact on mood.

### Problem
When looking at mental health, doctors will ask how symptoms are improving or worsening with treatment. This question can be difficult to answer because there are so many factors, and the outcome is hard to quantify. Inspired by Mark Watney I have decided to “science the sh!t” out of the problem. Thank you Andy Weir

### Data
The dataset includes:

- **Mood Ratings:** Recorded multiple times per day on a 1–5 scale
- **Other Scores:** Motivation (morning) and satisfaction (night) scores
- **Self-Care Activities:** Tracked daily (e.g., yoga, meditation, mindful walks, meals)
- **Timestamps:** Used to align mood data and activities, with lag features engineered (e.g., yoga yesterday, walk 3 days ago)

### Features & Engineering
- Time series alignment and lag feature creation (1-day, 3-day, etc.)
- Aggregation of mood ratings to daily averages or medians
- Binary indicators of whether a given activity occurred on given days
- Normalization of irregular entries and resolution of inconsistencies in raw data

### Analysis & Modeling
- **Exploratory Visualizations:** Boxplots comparing mood distributions after different activities
- **Statistical Trends:** Mood stability over time, IQR shifts, and median changes
- **Regression Models:** Evaluating which features have predictive power for mood (mean and end-of-day satisfaction)
- **Mindfulness Feature:** Grouped feature combining meditation, yoga, and mindful walks

### Current Learnings
- Mood isn't always higher on self-care days—but variability often decreases, suggesting emotional regulation may be a key benefit.
- Certain activities appear to have a delayed influence (e.g., a walk two or three days ago).

### Roadmap
- Clean up notebooks and modularize code
- Develop dashboard or visualization interface
- Test more advanced models (e.g., random forest or XGBoost)
- Include missing data analysis and data completeness tracking

### Notes
This is a personal project intended for educational purposes. No external data sources were used. The project is inspired by a desire to improve self-awareness and emotional health using real-world data. Problem statement quote borrowed from *The Martian* by Andy Weir

