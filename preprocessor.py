import re
import pandas as pd

def preprocess(data):
    # Adjusted pattern to handle both 12-hour and 24-hour timestamps
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s?-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Using dayfirst=True to handle day/month order
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce', dayfirst=True)

    # Fallback to 24-hour format in case 12-hour parsing fails
    df['message_date'] = df['message_date'].fillna(pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce', dayfirst=True))

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name exists
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date and time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Creating time periods for better analysis
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(f"{hour}:00-00:00")
        else:
            period.append(f"{hour}:00-{hour + 1}:00")

    df['period'] = period

    return df
