import streamlit as st
import preprocessor
import helper
import nltk
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image

nltk.download('vader_lexicon')

st.set_page_config(page_title="Chat Analysis", page_icon="🗨", initial_sidebar_state="expanded")
uploaded_file = st.file_uploader("Choose a file")

st.sidebar.title("Whatsapp Chat and Sentiment Analyzer")



if uploaded_file:
    st.markdown("These are all the texts in DataFrame")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # preprocessor file
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetching unique ysers
    names = df['name'].unique().tolist()
    # names.remove('group_notification')
    names.sort()
    names.insert(0,'Overall')

    name = st.sidebar.selectbox("show analysis of ",names)
    st.markdown('----') 
            

    if st.sidebar.button('Show Analysis'):
        st.header("Analysis On Messages")
        # helper file
        msg_count,words_count,total_media,total_urls = helper.selected_name(name,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(msg_count)

        with col2:
            st.subheader("Total Words")
            st.title(words_count)
        
        with col3:
            st.subheader("Media Files")
            st.title(total_media)
        
        with col4:
            st.subheader("Links")
            st.title(total_urls)
        st.markdown('----')


        # to see the most frequent users
        if name == 'Overall':
            st.header("Most Frequent Users")

            freq_users,d = helper.most_frequent_user(df)

            col1,col2 = st.columns([2,3])

            # show top 5 user and percentage
            with col1:
                st.subheader("Top 5 users")
                st.dataframe(freq_users)

            # show barchart pf top users
            with col2:
                st.subheader("Bar Chart ")
                fig = plt.figure(figsize=(10,5))
                sns.barplot(x=d.index,y=d.values, alpha=0.8)
                plt.xticks(rotation=45,fontsize=16)
                plt.ylabel("No of Messages", fontsize=20)
                plt.xlabel("Names", fontsize=20)
                warnings.filterwarnings("ignore")
                st.pyplot(fig)

            st.markdown('----')
    


# creating a word cloud
        l = helper.word_cloud(name,df)
        st.subheader("Wordcloud")

        fig, ax = plt.subplots()
        python_mask = np.array(Image.open("whatsappimage.png"))
        # python_mask = np.array(PIL.Image.open("E:\Whatsapp chat Analyzer\Chat Analyzer\whatsappimage.png"))
        wc = WordCloud(mask=python_mask,background_color='white').generate(l)
        ax.imshow(wc)
        plt.axis("off")
        plt.show()
        st.pyplot(fig)

        st.markdown('----')


        df_msg = helper.most_sent_msg(name,df)
        st.subheader("Most Commonly Used Messages")
        fig,ax = plt.subplots()
        ax.barh(df_msg.index,df_msg[0])
        st.pyplot(fig)
        st.markdown('----')



        e_df = helper.calculate_emojis(name,df)
        col1,col2 = st.columns(2)

        with col1:
            st.subheader("Emoji Used")
            st.dataframe(e_df)

        with col2:
            st.subheader("Pie Charts of Frequent Words")

            fig1,ax1 = plt.subplots()
            ax1.pie(e_df['No.'],labels=e_df['Emojis'],autopct='%1.1f%%', startangle=90)
            st.pyplot(fig1)
        st.markdown('----')


        # monthly active users
        msg_time = helper.timeline(name,df)
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Monthly Users Timeline")
            fig,ax = plt.subplots()
            ax.plot(msg_time['month-year'],msg_time['messages'])
            plt.xticks(rotation=45)
            plt.show()
            st.pyplot(fig)

        # Daily active users
        daily_messages = helper.daily_timeline(name,df)
        with col2:
            st.subheader("Daily Users Timeline")
            fig,ax = plt.subplots()
            ax.plot(daily_messages['daily_date'],daily_messages['messages'])
            plt.xticks(rotation=45)
            plt.show()
            st.pyplot(fig)

        st.markdown('----')









                            # Sentiment analysis 
####################################################################

        st.title("Sentiment Analysis")

        sentiments = SentimentIntensityAnalyzer()

        # Creating different columns for (Positive/Negative/Neutral)
        df["positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["messages"]] # Positive
        df["negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["messages"]] # Negative
        df["neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["messages"]] # Neutral

        # To indentify true sentiment per row in message column
        def sentiment(df):
            # for positice return 1
            if df["positive"] >= df["negative"] and df["positive"] >= df["neutral"]:
                return 1
            # for negative return -1
            if df["negative"] >= df["positive"] and df["negative"] >= df["neutral"]:
                return -1
            # for neutral return 0
            if df["neutral"] >= df["positive"] and df["neutral"] >= df["negative"]:
                return 0

        df['value'] = df.apply(lambda row: sentiment(row), axis=1)
        # removing group notificationa nd media ommeted
        notgn_df = df[df['name'] != 'group_notification']
        n_df = notgn_df[notgn_df['messages'] != "<Media omitted>\n"]


        # neutral users
        neutral_percet = n_df[n_df['value'] == 0][['name','value']].value_counts().reset_index()[:9]
        positive_percet = n_df[n_df['value'] == 1][['name','value']].value_counts().reset_index()[:9]
        negative_percet = n_df[n_df['value'] == -1][['name','value']].value_counts().reset_index()[:9]


        if name == 'Overall':
            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader("Top Positive Texts")
                fig = plt.figure()
                sns.barplot(x = positive_percet.name,y = positive_percet[0])
                plt.xticks(rotation=45,fontsize=16)
                plt.ylabel("No of Positive Messages", fontsize=20)
                plt.xlabel("Names", fontsize=20)
                warnings.filterwarnings("ignore")
                st.pyplot(fig)

            with col2:
                st.subheader("Top Negative Texts")
                fig = plt.figure()
                sns.barplot(x=negative_percet['name'],y=negative_percet[0])
                plt.xticks(rotation=45,fontsize=16)
                plt.ylabel("No of Positive Messages", fontsize=20)
                plt.xlabel("Names", fontsize=20)
                warnings.filterwarnings("ignore")
                st.pyplot(fig)

            with col3:
                st.subheader("Top Neutral Texts")
                fig = plt.figure()
                sns.barplot(x=neutral_percet['name'],y=neutral_percet[0])
                plt.xticks(rotation=45,fontsize=16)
                plt.ylabel("No of Positive Messages", fontsize=20)
                plt.xlabel("Names", fontsize=20)
                warnings.filterwarnings("ignore")
                st.pyplot(fig)



# creating wordcloud for positve, negative and neurtral
        po_words,ne_words,un_words = helper.sentiment_wordcloud(n_df,name)
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("Positive Word Cloud")
            fig, ax = plt.subplots()
            wc = WordCloud().generate(po_words)
            ax.imshow(wc)
            plt.axis("off")
            plt.show()
            st.pyplot(fig)

        with col2:
            st.subheader("Negative Word Cloud")
            fig, ax = plt.subplots()
            wc = WordCloud().generate(ne_words)
            ax.imshow(wc)
            plt.axis("off")
            plt.show()
            st.pyplot(fig)

        with col3:
            st.subheader("Neutral Word Cloud")
            fig, ax = plt.subplots()
            wc = WordCloud().generate(un_words)
            ax.imshow(wc)
            plt.axis("off")
            plt.show()
            st.pyplot(fig)

