# 💰 Financial Analysis Dashboard

A comprehensive web application for analyzing personal financial data with AI-powered insights and interactive visualizations.

## ✨ Features

- **📊 Interactive Charts**: Multiple visualization types including line charts, pie charts, and bar charts
- **🤖 AI-Powered Chatbot**: RAG-based financial assistant using Google Gemini API
- **📈 Financial Insights**: Comprehensive analysis of income, expenses, savings, and investments
- **📁 CSV Upload**: Easy file upload with drag-and-drop support
- **🎯 Budget Planning**: Personalized financial advice and recommendations
- **📱 Responsive Design**: Modern, mobile-friendly interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (for AI chatbot feature)

### Installation

1. **Clone or download the project files**

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Configure Gemini API**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - The setup script will create a `.env` file for you
   - Open `.env` and replace `your_gemini_api_key_here` with your actual API key

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## 🔧 Environment Configuration

The application uses a `.env` file to store sensitive configuration like API keys. The setup script will create this file for you.

### .env File Format:
```env
# Financial Analysis Dashboard Environment Variables
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: Flask Configuration
# FLASK_ENV=development
# FLASK_DEBUG=True
```

**Important**: Never commit the `.env` file to version control. It contains sensitive information.

## 📊 Data Format

The application expects CSV files with the following columns:
- `Month`: Date in YYYY-MM format
- `Income`: Monthly income
- `Rent`, `Utilities`, `Insurance`, `Loan_Payments`: Fixed expenses
- `Groceries`, `Transportation`, `Entertainment`, `Healthcare`, `Shopping`, `Dining_Out`, `Subscriptions`: Variable expenses
- `Savings`, `Investments`: Savings and investment amounts
- `Total_Expenses`, `Net_Income`: Calculated fields

## 🎯 Usage

1. **Upload Data**: Either upload your own CSV file or use the provided sample data
2. **View Analysis**: Explore interactive charts showing your financial patterns
3. **Ask Questions**: Use the AI chatbot to get personalized financial advice
4. **Get Insights**: Review summary statistics and recommendations

## 🤖 AI Chatbot Features

The AI assistant can help you with:
- Spending pattern analysis
- Budget optimization suggestions
- Savings rate improvements
- Investment recommendations
- Financial goal planning
- Expense categorization advice

## 📈 Available Visualizations

- **Income Trend**: Monthly income over time
- **Expense Breakdown**: Annual expense distribution by category
- **Monthly Expenses**: Stacked bar chart of monthly expenses
- **Savings & Investments**: Trend analysis of savings and investments
- **Net Income Trend**: Monthly net income with break-even line

## 🛠️ Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Plotly.js
- **AI**: Google Gemini API
- **Data Processing**: Pandas, NumPy

## 📝 Sample Questions for AI Assistant

- "How can I improve my savings rate?"
- "What's my biggest expense category?"
- "Am I spending too much on entertainment?"
- "How much should I save each month?"
- "What's my average monthly spending?"
- "How can I reduce my expenses?"

## 🔧 Customization

You can easily customize the application by:
- Modifying chart colors and styles in `templates/index.html`
- Adding new analysis functions in `app.py`
- Extending the AI prompt context for more specific advice
- Adding new chart types in the `FinancialAnalyzer` class

## 📋 Requirements

See `requirements.txt` for the complete list of Python packages.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Financial Planning! 💰📈**
