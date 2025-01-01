import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import os
import hashlib



USER_DATA_FILE = "users.csv"

# Initialize the user data file if it doesn't exist
if not os.path.exists(USER_DATA_FILE):
    df = pd.DataFrame(columns=["Username", "Password"])
    df.to_csv(USER_DATA_FILE, index=False)

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify password
def verify_password(stored_password, entered_password):
    return stored_password == hash_password(entered_password)

# Function to handle signup
def signup(username, password):
    df = pd.read_csv(USER_DATA_FILE)
    if username in df["Username"].values:
        return False  # Username already exists
    new_user = pd.DataFrame({"Username": [username], "Password": [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DATA_FILE, index=False)
    return True

# Function to handle login
def login(username, password):
    df = pd.read_csv(USER_DATA_FILE)
    if username not in df["Username"].values:
        return False  # Username not found
    stored_password = df.loc[df["Username"] == username, "Password"].values[0]
    return verify_password(stored_password, password)

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Sidebar navigation
options = st.sidebar.radio("Choose a section:", ["Login", "ChatFlow Analyzer", "Review Flow"])

if options == "Login":
    # Login and Signup logic
    option = st.sidebar.selectbox("Choose Option", ["Signup", "Login"])
    
    if option == "Signup":
        st.title("Create an Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if password == confirm_password:
                if signup(username, password):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Username already exists!")
            else:
                st.error("Passwords do not match.")
    
    if option == "Login":
        st.title("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username} ! You are now logged in.")
            else:
                st.error("Invalid username or password.")



if options == "ChatFlow Analyzer":
    if st.session_state.logged_in:
    
        st.sidebar.markdown("<hr style='border:2px solid green'>", unsafe_allow_html=True)
        
        st.sidebar.markdown("# Whatsapp Chat Analyzer")
        
        st.sidebar.markdown("<hr style='border:2px solid green'>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            .sidebar-title {
                color: green;
                font-size: 35px;
                font-weight: bold;
                text-align: center;  /* This will center the text */
            }
            </style>
            <div class="sidebar-title">Whatsapp Chat Analyzer</div>
            """,
            unsafe_allow_html=True
        )


        st.sidebar.markdown("### Upload your exported WhatsApp chat in `.txt` format")



        
        # Add a colored divider line
        st.markdown("<hr style='border:2px solid red'>", unsafe_allow_html=True)

        


        # Add a "Scroll to Top" button




        uploaded_file = st.sidebar.file_uploader("Choose a file")

        if uploaded_file is not None:
            with st.spinner('Processing the uploaded file...'):
                bytes_data = uploaded_file.getvalue()
                data = bytes_data.decode("utf-8")
                df = preprocessor.preprocess(data)

            st.success('File has been uploaded successfully 🎉')
            

            # fetch unique users
            user_list = df['user'].unique().tolist()
            user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0,"Overall")

            selected_user = st.sidebar.selectbox("Select user for analysis",user_list)

            if st.sidebar.button("Show Analysis"):
                # Stats Area
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)

                # Add a colored divider line
                st.markdown("<hr style='border: 1px solid #4CAF50;'>", unsafe_allow_html=True)  # Green line

                st.subheader("📊 Key Statistics")
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total Messages", num_messages)
                col2.metric("Total Words", words)
                col3.metric("Media Shared", num_media_messages)
                col4.metric("Links Shared", num_links)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid green'>", unsafe_allow_html=True)
                
                # Monthly Timeline
                st.subheader("📅 Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig = px.line(timeline, x='time', y='message', title="Messages Over Time", markers=True)
                fig.update_layout(xaxis_title="Time", yaxis_title="Messages", template="plotly_dark")
                st.plotly_chart(fig)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                # daily timeline
                st.subheader("📆 Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig = px.line(daily_timeline, x='only_date', y='message', title="Messages Per Day", markers=True)
                fig.update_layout(xaxis_title="Date", yaxis_title="Messages", template="plotly_white")
                st.plotly_chart(fig)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                # activity map
                st.subheader("🗺️ Activity Map")
                col1,col2 = st.columns(2)

                with col1:
                    st.header("Most busy day")
                    busy_day = helper.week_activity_map(selected_user,df)
                    fig,ax = plt.subplots()
                    ax.bar(busy_day.index,busy_day.values,color='purple')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.header("Most busy month")
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values,color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                
                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                # Weekly Activity Heatmap
                st.subheader("📅 Weekly Activity Heatmap")
                user_heatmap = helper.activity_heatmap(selected_user, df)

                if not user_heatmap.empty:
                    fig, ax = plt.subplots()
                    ax = sns.heatmap(user_heatmap)
                    st.pyplot(fig)
                else:
                    st.write("No activity data available for the selected user.")

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                # finding the busiest users in the group(Group level)
                if selected_user == 'Overall':
                    st.subheader("👥 Most Active Users")
                    x, new_df = helper.most_busy_users(df)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.bar_chart(x)
                    with col2:
                        st.dataframe(new_df)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                # WordCloud
                st.subheader("🔤 Most Common Words")
                df_wc = helper.create_wordcloud(selected_user,df)
                fig,ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)


                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)


                # Most Common Words
                st.subheader("🔤 Most Common Words")
                most_common_df = helper.most_common_words(selected_user, df)
                fig = px.bar(most_common_df, x=0, y=1, title="Most Common Words", labels={"0": "Words", "1": "Frequency"})
                st.plotly_chart(fig)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)


                # Emoji Analysis
                st.subheader("😊 Emoji Analysis")
                emoji_df = helper.emoji_helper(selected_user, df)
                if not emoji_df.empty:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(emoji_df.head())
                    with col2:
                        fig = px.pie(emoji_df.head(), values=1, names=0, title="Top Emojis", labels={"0": "Emoji", "1": "Count"})
                        st.plotly_chart(fig)
                else:
                    st.warning("No emoji data available for the selected user.")
                

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)


                # Sentiment Analysis Section
                st.subheader("🧠 Sentiment Analysis")

                sentiment_df = df[df['user'] == selected_user] if selected_user != "Overall" else df
                sentiment_counts = sentiment_df['sentiment_category'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']

                col1, col2 = st.columns(2)

                with col1:
                    st.write("Sentiment Distribution")
                    st.dataframe(sentiment_counts)

                with col2:
                    fig = px.pie(sentiment_counts, values='Count', names='Sentiment', title="Sentiment Distribution",
                                color='Sentiment',
                                color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#FFC107', 'Negative': '#F44336'})
                    st.plotly_chart(fig)

                # Add a colored divider line
                st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)


                # Ensure 'sentiment' column is numeric and handle any conversion issues
                if 'sentiment' not in sentiment_df.columns:
                    st.warning("Sentiment column is missing. Please perform sentiment analysis.")
                else:

                    # Convert sentiment to numeric, coercing errors to NaN
                    sentiment_df['sentiment'] = pd.to_numeric(sentiment_df['sentiment'], errors='coerce')
                    
                    # Drop rows with NaN values in 'sentiment' column
                    sentiment_df = sentiment_df.dropna(subset=['sentiment'])

                    # Check if sentiment column contains any valid data
                    if sentiment_df.empty:
                        st.warning("No sentiment data available.")
                    else:
                        # Sentiment Over Time Plot
                        st.subheader("📈 Sentiment Over Time")
                        sentiment_df['only_date'] = pd.to_datetime(sentiment_df['only_date'], errors='coerce')  # Ensure the date column is in proper format
                        sentiment_timeline = sentiment_df.groupby('only_date')['sentiment'].mean().reset_index()

                        # If the sentiment_timeline is empty, issue a warning
                        if sentiment_timeline.empty:
                            st.warning("No sentiment data available to display the graph.")
                        else:
                            fig = px.line(sentiment_timeline, x='only_date', y='sentiment', title="Average Sentiment Over Time")
                            fig.update_layout(xaxis_title="Date", yaxis_title="Sentiment", template="plotly_dark")
                            st.plotly_chart(fig)


                        # Add a colored divider line
                        st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

                        # Top Positive & Negative Messages
                        st.subheader("🔝 Top Positive & Negative Messages")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("#### Positive Messages 😊")
                            positive_messages = sentiment_df[sentiment_df['sentiment'] > 0.5].sort_values(by='sentiment', ascending=False).head(5)
                            if positive_messages.empty:
                                st.warning("No positive messages found.")
                            else:
                                for _, message in positive_messages.iterrows():
                                    st.write(f"📩 {message['message']} (Sentiment: {message['sentiment']:.2f})")

                        with col2:
                            st.write("#### Negative Messages 😔")
                            negative_messages = sentiment_df[sentiment_df['sentiment'] < -0.5].sort_values(by='sentiment').head(5)
                            if negative_messages.empty:
                                st.warning("No negative messages found.")
                            else:
                                for _, message in negative_messages.iterrows():
                                    st.write(f"📩 {message['message']} (Sentiment: {message['sentiment']:.2f})")




                # Add a colored divider line
                st.markdown("<hr style='border: 1px solid blue;'>", unsafe_allow_html=True)  # Green line

                
                col1, col2 = st.columns(2)

                with col1:
                
                    if st.button("Download Excel Report"):
                        excel_buffer = helper.generate_excel(df)
                        st.download_button(
                            label="Download Excel",
                            data=excel_buffer,
                            file_name="chat_analysis_report.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                
                with col2:

                    if st.button("Download PDF Report", key="download_pdf_button"):
                        pdf_buffer = helper.generate_pdf(df)
                        st.download_button(
                            label="Download PDF",
                            data=pdf_buffer,
                            file_name="chat_analysis_report.pdf",
                            mime="application/pdf",
                            key="pdf_download_button"
                        )
                        

                st.markdown("<hr style='border: 1px solid blue;'>", unsafe_allow_html=True)  # Green line


                # Social Media Buttons
                st.subheader("🌐 Connect with Me")

                st.markdown("<hr style='border:1px solid black'>", unsafe_allow_html=True)

                
                col1, col2, col3 = st.columns(3)

                # GitHub Link
                with col1:
                    st.markdown("""
                        <div style="text-align: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" style="margin-bottom: 5px;"/>
                            <br/>
                            <a href="https://github.com/Anish62027" target="_blank" style="text-decoration: none; font-size: 16px; color: #333;">
                                GitHub
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                # LinkedIn Link
                with col2:
                    st.markdown("""
                        <div style="text-align: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" style="margin-bottom: 5px;"/>
                            <br/>
                            <a href="https://www.linkedin.com/in/anish-kumar-32a701213?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank" style="text-decoration: none; font-size: 16px; color: #0077B5;">
                                LinkedIn
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                # Email Link
                with col3:
                    st.markdown("""
                        <div style="text-align: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email" width="30" style="margin-bottom: 5px;"/>
                            <br/>
                            <a href="mailto:your-email@example.com" style="text-decoration: none; font-size: 16px; color: #333;">
                                Email
                            </a>
                        </div>
                        """, unsafe_allow_html=True)


                # Add a colored divider line
                st.markdown("<hr style='border:2px solid red'>", unsafe_allow_html=True)

                st.markdown(
                            """
                            <style>
                            .footer {
                                color: black;
                                font-size: 16px;
                                font-weight: bold; /* Makes the text bold */
                                text-align: center; /* Centers the text */
                                margin-top: 50px; /* Adds space above the footer */
                            }
                            </style>
                            <div class="footer">Crafted with ❤️ for Your Chat Analytics Built Using Streamlit</div>
                            """,
                            unsafe_allow_html=True,
                        )
    else:
        st.warning("You must log in to access this section.")
        st.stop()
         

elif options == "Review Flow":
    if st.session_state.logged_in:
        
    

        st.markdown(
            """
            <style>
            .sidebar-title {
                color: green;
                font-size: 28px;
                font-weight: bold;
                text-align: center;  /* This will center the text */
            }
            </style>
            <div class="sidebar-title">Whatsapp Chat Analyzer</div>
            """,
            unsafe_allow_html=True
        )

    
        st.markdown("<hr style='border:2px solid red'>", unsafe_allow_html=True)

        feedback_file = "user_feedback.csv"

        
        if not os.path.exists(feedback_file):
            pd.DataFrame(columns=["Name", "Email", "Rating", "Feedback"]).to_csv(feedback_file, index=False)

        section = st.sidebar.selectbox("Choose a section:", ["Provide Feedback", "View Feedback"])

        # Provide Feedback Section
        if section == "Provide Feedback":
            st.markdown("### 💬 Provide Your Feedback")
            
            with st.form("feedback_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                rating = st.slider("Rate the project (1 to 5 stars)", 1, 5, 3)
                feedback = st.text_area("Please provide your feedback here: Your Feedback")

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if name and email and feedback:
                        feedback_df = pd.read_csv(feedback_file)
                        new_feedback = pd.DataFrame([[name, email, rating, feedback]], columns=["Name", "Email", "Rating", "Feedback"])
                        feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
                        feedback_df.to_csv(feedback_file, index=False)
                        st.success("Thank you for your feedback! 😊")
                    else:
                        st.error("Please fill in all the fields before submitting.")

        # View Feedback Section
        elif section == "View Feedback":
            st.markdown("### 📋 View Submitted Feedback")
            
            # Read the feedback data from the CSV file
            feedback_df = pd.read_csv(feedback_file)
            
            if not feedback_df.empty:
                st.write("Here are the feedback submissions:")
                st.dataframe(feedback_df)
            else:
                st.write("No feedback has been submitted yet.")

        st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)

        # Social Media Buttons
        st.subheader("🌐 Connect with Me")

        st.markdown("<hr style='border:1px solid blue'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)

        # GitHub Link
        with col1:
            st.markdown("""
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" style="margin-bottom: 5px;"/>
                    <br/>
                    <a href="https://github.com/Anish62027" target="_blank" style="text-decoration: none; font-size: 16px; color: #333;">
                        GitHub
                    </a>
                </div>
                """, unsafe_allow_html=True)

        # LinkedIn Link
        with col2:
            st.markdown("""
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" style="margin-bottom: 5px;"/>
                    <br/>
                    <a href="https://www.linkedin.com/in/anish-kumar-32a701213?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank" style="text-decoration: none; font-size: 16px; color: #0077B5;">
                        LinkedIn
                    </a>
                </div>
                """, unsafe_allow_html=True)

        # Email Link 
        with col3:
            st.markdown("""
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email" width="30" style="margin-bottom: 5px;"/>
                    <br/>
                    <a href="mailto:your-email@example.com" style="text-decoration: none; font-size: 16px; color: #333;">
                        Email
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
        st.markdown("<hr style='border:2px solid red'>", unsafe_allow_html=True)

        

        st.markdown(
                    """
                    <style>
                    .footer {
                        color: black;
                        font-size: 16px;
                        font-weight: bold; /* Makes the text bold */
                        text-align: center; /* Centers the text */
                        margin-top: 50px; /* Adds space above the footer */
                    }
                    </style>
                    <div class="footer">Crafted with ❤️ for Your Chat Analytics Built Using Streamlit</div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.warning("You must log in to access this section.")
        st.stop()

else:
    st.markdown(
                            """
                            <style>
                            .footer {
                                color: black;
                                font-size: 16px;
                                font-weight: bold; /* Makes the text bold */
                                text-align: center; /* Centers the text */
                                margin-top: 50px; /* Adds space above the footer */
                            }
                            </style>
                            <div class="footer">Crafted with ❤️ for Your Chat Analytics Built Using Streamlit</div>
                            """,
                            unsafe_allow_html=True,
                        )
        
