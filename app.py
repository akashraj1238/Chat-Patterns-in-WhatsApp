import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# App Title
st.sidebar.title("WhatsApp Conversation Tracker")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload your WhatsApp chat file (txt format)")

# Process file when uploaded
if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    # List of users excluding group notifications
    users = df['user'].unique().tolist()
    if 'group_notification' in users:
        users.remove('group_notification')
    users.sort()
    users.insert(0, "Overall")  # Add option for overall stats

    # User selection dropdown
    selected_user = st.sidebar.selectbox("Analyze chat for", users)

    # Display Analysis
    if st.sidebar.button("Generate Analysis"):

        # Top Statistics
        st.title("Chat Summary")
        num_messages, total_words, media_messages, link_count = helper.fetch_stats(selected_user, df)
        st.write("**Total Messages:**", num_messages)
        st.write("**Total Words:**", total_words)
        st.write("**Media Files Shared:**", media_messages)
        st.write("**Links Shared:**", link_count)

        # Monthly Activity Timeline
        st.title("Monthly Chat Activity")
        monthly_data = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_data['time'], monthly_data['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Activity Timeline
        st.title("Daily Chat Activity")
        daily_data = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_data['only_date'], daily_data['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Distribution (Days and Months)
        st.title("Activity Patterns")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Active Days")
            busy_days = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_days.index, busy_days.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Most Active Months")
            busy_months = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_months.index, busy_months.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap for User Activity
        st.title("Hourly Activity Heatmap")
        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heatmap_data, ax=ax, cmap="coolwarm")
        st.pyplot(fig)

        # Most Active Users (Group-Level)
        if selected_user == "Overall":
            st.title("Most Active Users")
            top_users, user_percent = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(top_users.index, top_users.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.write(user_percent)

        # Wordcloud
        st.title("Frequent Words")
        wordcloud = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        st.pyplot(fig)

        # Most Common Words
        st.title("Most Common Words")
        common_words = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_words[0], common_words[1], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Usage")
        emoji_data = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.write(emoji_data)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_data[1].head(), labels=emoji_data[0].head(), autopct="%0.2f")
            st.pyplot(fig)
