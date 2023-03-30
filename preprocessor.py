import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)    
    df = pd.DataFrame({'message':message,'date':date})
    df['date'] = df['date'].str.rstrip(" -")
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y, %H:%M')
    name = []
    messages = []
    for a in df['message']:
        first_name = re.split('([\w\W]+?):\s', a)
        # print(first_name)
        if first_name[1:]:
            name.append(first_name[1])
            messages.append(first_name[2])
        else:
            name.append('group_notification')
            messages.append(first_name[0])
    df['name'] = name
    df['messages'] = messages
    df.drop(columns=['message'],inplace=True)
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df



