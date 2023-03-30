from urlextract import URLExtract
import pandas as pd
import emoji
import calendar

extract = URLExtract()

def selected_name(name,df):
    if name == 'Overall':
        # 1- no. of messages
        msg_count = df.shape[0]
        # 2- no. of words
        words_count = count_alphabtes(df,name)
        # 3- media files
        media =  len(df[df['messages'] == '<Media omitted>\n'])
        # 4- total urls
        total_urls = len(extract.find_urls(str(df['messages'].to_list())))

        return msg_count,words_count,media,total_urls
    else:
        # 1- no. of messages
        msg_count = df[df['name'] == name]['messages'].count()
        # 2- no. of words
        words_count = count_alphabtes(df,name)
        # 3- no of media files
        media = len(df[(df['messages'] == '<Media omitted>\n') & (df['name'] == name)])
        # 4- total urls
        total_urls = len(extract.find_urls(str(df[df['name'] == name]['messages'].to_list())))

        return msg_count,words_count,media,total_urls
    

def most_frequent_user(df):
    # show top 5 users
    top_five_users = round((df['name'].value_counts()[:5]/df.shape[0])*100,2).reset_index().rename(columns = {'index':'Names','name':'Chat %'})
    # plot top 5 users
    d = df['name'].value_counts()[:4]

    return top_five_users,d


def word_cloud(name,df):
    notifications = ['<Media omitted>','This message was deleted','You deleted this message']
    if name == 'Overall':
        l=""
        for a in df['messages'].str.strip():
            if a not in notifications:
                l = l + ((''.join(a)))
        l = l.replace(' ',', ')

    else:
        l=""
        for a in df[df['name']==name]['messages'].str.strip():
            if a not in notifications:
                l = l + ((''.join(a)))
        l = l.replace(' ',', ')

    return l

def most_sent_msg(name,df):
    if name == 'Overall':
        r_df = df[df['name'] != 'group_notification']
        n_df = r_df[r_df['messages'] != "<Media omitted>\n"]
        l = []
        for a in n_df['messages']:
            l.extend(a.split())
        most_msg = pd.Series(l).value_counts()
        df_msg = pd.DataFrame(most_msg)[:20]
    else:
        r_df = df[df['name'] != 'group_notification']
        n_df = r_df[r_df['messages'] != "<Media omitted>\n"]
        n_df = n_df[n_df['name'] == name]
        l = []
        for a in n_df['messages']:
            l.extend(a.split())
        most_msg = pd.Series(l).value_counts()
        df_msg = pd.DataFrame(most_msg)[:20]

    return df_msg



# calculating the emojis used
def calculate_emojis(name,df):
    emoji_list = [] 
    if name == 'Overall':
        for message in df['messages']:
            emoji_list.extend([e for e in message if emoji.emoji_list(e)])
            s = pd.Series(emoji_list).value_counts()
            e_df = s.reset_index()[:9].rename(columns = {'index':'Emojis',0:'No.'})
    else:
        for message in df[df['name']==name]['messages']:
            emoji_list.extend([e for e in message if emoji.emoji_list(e)])
            s = pd.Series(emoji_list).value_counts()
            e_df = s.reset_index()[:9].rename(columns = {'index':'Emojis',0:'No.'})
    return e_df



def timeline(name,df):
    df['monthName'] = df['month'].apply(lambda x: calendar.month_name[x])
    if name == 'Overall':
        msg_time = df.groupby(['year','monthName','month']).count()['messages'].reset_index()
        time = []
        for a in range(msg_time.shape[0]):
            time.append(msg_time['monthName'][a]+"-"+str(msg_time['year'][a]))
        msg_time['month-year'] = time
    else:    
        msg_time = df[df['name']==name].groupby(['year','monthName','month']).count()['messages'].reset_index()
        time = []
        for a in range(msg_time.shape[0]):
            time.append(msg_time['monthName'][a]+"-"+str(msg_time['year'][a]))
        msg_time['month-year'] = time        

    return msg_time[:9]


def daily_timeline(name,df):
    df['daily_date'] = df['date'].dt.date
    if name == 'Overall':
        daily_messages = df.groupby('daily_date').count()['messages'].reset_index()
    else:
        daily_messages = df[df['name']==name].groupby('daily_date').count()['messages'].reset_index()

    return daily_messages[:9]
    

# count the words
def count_alphabtes(df,name):
    if name == 'Overall':
        items = df[df['name'] != "group_notification"]['messages'].str.rstrip()
    else:
        items = df[df['name'] == name]['messages'].str.rstrip()

    alphabets = 0
    for a in items:
        if a == "<Media omitted>":
            pass
        else:
            alphabets = alphabets + len(a.split())
    return alphabets






####################################################################
                            # Sentiment analysis 


def sentiment_wordcloud(n_df,name):
    if name == 'Overall':
        po_words = n_df[n_df['value'] == 1]['messages'].to_string()
        ne_words = n_df[n_df['value'] == -1]['messages'].to_string()
        un_words = n_df[n_df['value'] == 0]['messages'].to_string()
        return po_words,ne_words,un_words
    else:
        po_words = n_df[(n_df['name']==name)&(n_df['value'] == 1)]['messages'].to_string()
        ne_words = n_df[(n_df['name']==name)&(n_df['value'] == -1)]['messages'].to_string()
        un_words = n_df[(n_df['name']==name)&(n_df['value'] == 0)]['messages'].to_string()
        return po_words,ne_words,un_words

