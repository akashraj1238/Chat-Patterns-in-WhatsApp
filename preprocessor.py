import re
import pandas as pd

def preprocess(data):
    try:
        pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{2}:\d{2}\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

        if not messages or not dates:
            raise ValueError("No valid messages found in the file.")

        df = pd.DataFrame({"user_message": messages, "date": dates})
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M - ')

        users = []
        messages = []
        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        return df
    except Exception as e:
        raise RuntimeError(f"Error in preprocessing: {e}")
