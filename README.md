# whatsapp-chat-analyzer
Whatsapp Chat Analyzer is a simple tool to analyze WhatsApp chats. Get insights like message activity, common words, emojis, activity heatmaps, and sentiment analysis. Features include word clouds, sentiment distribution, and PDF/Excel report downloads. Perfect for understanding group dynamics, trends, and interactions in chats.


# WhatsApp Chat Analyzer

## 🔎 Project Overview
The **WhatsApp Chat Analyzer** is an interactive and user-friendly tool designed to help you dive deep into your WhatsApp conversations. With just a few clicks, you can analyze your exported chat data to uncover trends, activity patterns, and insights about your communication habits. Whether it’s for personal reflection or group analysis, this tool provides everything you need to better understand your chats.

---

## 🔍 Key Features
- **📊 Detailed Statistics**: Gain insights into total messages, media shared, links sent, and more.
- **🧩 Participant Analysis**: Identify the most active members in group chats.
- **🌐 Word Cloud**: Visualize your most frequently used words.
- **😂 Emoji Trends**: Discover your most-used emojis at a glance.
- **⏳ Time-Based Trends**: Analyze message activity by hours, days, and weeks.
- **📈 Interactive Visualizations**: Get stunning, easy-to-read charts and graphs.
- **📢 Feedback Collection**: Includes a feedback feature to enhance future updates.
- **User Authentication**
    - Signup: Users can securely create accounts with password hashing (SHA-256).
    - Login: Users can log in to access chat analytics after successful password verification.
- **WhatsApp Chat Analysis**
    - Chat Upload: Upload WhatsApp chat files in .txt format for processing.
    - Statistics: Displays total messages, words, media shared, and links sent.

- **Visualizations**:

📅 Monthly & Daily Timelines: View message activity on both daily and monthly timelines.
📈 Weekly Activity Heatmap: Analyze user activity patterns across the week.
📊 Activity Breakdown: Get detailed activity breakdowns by day and month.
👥 Busiest Users: Identify the most active participants in the group chat.
🔠 Word Cloud: Generate a visual representation of the most frequently used words.
😂 Emoji Analysis: Discover the most commonly used emojis.
Sentiment Analysis:

📊 Sentiment Distribution: Visualize sentiment across different messages.
⏳ Sentiment Over Time: Track sentiment changes over the duration of the chat.
🔍 Top Positive and Negative Messages: Identify the most positive and negative messages.
3. Report Generation
Excel Report: Download chat analysis in .xlsx format for further review.
PDF Report: Download chat analysis in .pdf format for documentation and sharing.
4. Social Media Integration
🌐 Professional Links:
GitHub - Access the project's repository.
LinkedIn - Connect on LinkedIn.
Email: Reach out for queries or support.
5. User Experience
Styled Interface: The app features a clean, user-friendly interface built with HTML and CSS.
Error Handling: User-friendly error messages ensure smooth interaction.
6. 📊 Detailed Statistics
Gain insights into:

Total messages
Words sent
Media shared
Links sent
7. 🧩 Participant Analysis
Identify the most active participants in group chats.

8. 🌐 Word Cloud
Visualize the most frequently used words in the chat.

9. 😂 Emoji Trends
Discover and analyze the emojis most frequently used by participants.

10. ⏳ Time-Based Trends
Analyze message activity across different hours of the day, days of the week, and months.

11. 📈 Interactive Visualizations
Stunning charts and graphs to represent chat activity and trends clearly.
12. 📢 Feedback Collection
Users can provide feedback and suggestions for future updates.
- 

---

## 🌐 File Structure
```
whatsapp-chat-analyzer/
|-- app.py                  # Main application logic
|-- helper.py               # Helper functions for data processing
|-- preprocessor.py         # Preprocessing WhatsApp chat data
|-- requirements.txt        # List of dependencies
|-- stop_hinglish.txt       # Custom stop words for filtering
|-- user_feedback.csv       # CSV file for storing user feedback
|-- users.csv               # CSV file for storing user details
```

---

## 🛠️ Requirements
To run this project, you’ll need the following dependencies:

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- emoji
- nltk
- streamlit
- wordcloud
- vaderSentiment
- plotly
- reportlab
- urlextract




Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## 🔄 How to Use
1. **Export WhatsApp Chat**:
   - Open the desired chat in WhatsApp.
   - Select "Export Chat" from the options menu.
   - Choose "Without Media" for a smaller file size.

2. **Run the Application**:
   - Clone the repository:
     ```bash
     git clone https://github.com/Anish62027/whatsapp-chat-analyzer.git
     cd whatsapp-chat-analyzer
     ```
   - Start the application:
     ```bash
     streamlit run app.py
     ```

3. **Analyze Chat Data**:
   - Upload the exported `.txt` file through the app interface.
   - Explore interactive charts, trends, and statistics right from the app dashboard.

---

## 🖼 Screenshots
### 🎨 Dashboard Example
*Include screenshots of the app interface, charts, or results.*

---

## 🚀 Future Enhancements
- Sentiment analysis to classify conversations as positive, negative, or neutral.
- Multi-language support for analyzing chats in regional languages.
- Export analysis results as downloadable PDF or Excel reports.
- Integration with cloud-based storage for storing user feedback and chats securely.

---

## 🛠️ Contributing
Contributions are always welcome! If you’d like to contribute:

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request and explain your changes.

---

## ℹ️ License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 💡 Tips
- Ensure the `.txt` file is properly formatted after exporting the chat.
- Run the app in a stable Python environment for the best experience.

Enjoy analyzing your WhatsApp chats! 🌟 If you have any questions, feedback, or suggestions, feel free to reach out.

