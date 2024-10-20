from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return (
        df.shape[0],
        sum(len(msg.split()) for msg in df['message']),
        df[df['message'] == '<Media omitted>\n'].shape[0],
        len([url for msg in df['message'] for url in extract.find_urls(msg)])
    )

def most_busy_users(df):
    user_count = df['user'].value_counts().head()
    user_percent = (df['user'].value_counts(normalize=True) * 100).reset_index().rename(columns={'user': 'user', 'proportion':'percentage'})
    return user_count, user_percent

def create_wordcloud(selected_user, df):
    stop_words = open('stop_hinglish.txt', 'r').read().split()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp_df = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    wordcloud = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=set(stop_words)).generate(" ".join(temp_df['message']))
    return wordcloud

def most_common_words(selected_user, df):
    stop_words = open('stop_hinglish.txt', 'r').read().split()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    words = [word for msg in df[df['message'] != '<Media omitted>\n']['message'] for word in msg.lower().split() if word not in stop_words]
    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Extract emojis
    emojis = [c for msg in df['message'] for c in msg if emoji.is_emoji(c)]

    # Count and get top 5 emojis
    emoji_counts = Counter(emojis)
    top_5_emojis = emoji_counts.most_common(5)

    # Convert to DataFrame
    emoji_df = pd.DataFrame(top_5_emojis, columns=['Emoji', 'Count'])
    
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heatmap_data = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    # Check if the DataFrame is empty
    if heatmap_data.empty:
        return None
    return heatmap_data
