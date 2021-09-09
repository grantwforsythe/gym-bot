from datetime import datetime 

def convert_to_RFC_datetime(hour, minute=0):
    NOW = datetime.now()
    return datetime(NOW.year, NOW.month, NOW.day, hour, minute).isoformat() + 'Z'
