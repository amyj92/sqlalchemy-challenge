# sqlalchemy-challenge

In this SQLAlchemy Challenge, I have used Python and SQLAlchemy (specifically SQLAlchemy ORM queries, Pandas, and Matplotlib) to do a basic climate analysis and data exploration of the climate database of Honolulu, Hawaii. I have also designed a Flask API based on the queries developed.

The following are available routes within the app:

    Displays a dictionary of the precipitation analysis of the last 12 months of data:
    
        /api/v1.0/precipitation
    
    Displays a list of stations from the dataset:
        
        /api/v1.0/stations

    Displays the dates and temperature observations of the most-active station for the previous year of data:
    
        /api/v1.0/tobs
    
    Aggregate tobs data for all dates greater than a specific start date - enter format in yyyy-mm-dd:
    
        /api/v1.0/<start>
    
    Aggregate tobs data for between specific start and end dated - enter format in yyyy-mm-dd:
    
        /api/v1.0/<start>/<end>
