from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud

def fetch_stats(selected_user, df):
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        number_of_messages = df.shape[0]
        words = []
        for message in df['message']:
            words.extend(message.split())

        media_shared = df[df['message'] == '<Media omitted>\n'].shape[0]

        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))

        return number_of_messages, len(words), media_shared, len(links)
    except Exception as e:
        raise RuntimeError(f"Error fetching stats: {e}")

def most_busy_users(df):
    try:
        x = df['user'].value_counts().head()
        new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
            columns={'index': 'name', 'user': 'percentage'})
        return x, new_df
    except Exception as e:
        raise RuntimeError(f"Error finding most busy users: {e}")

def create_wordcloud(selected_user, df):
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(df['message'].str.cat(sep=" "))
        return df_wc
    except Exception as e:
        raise RuntimeError(f"Error creating word cloud: {e}")
