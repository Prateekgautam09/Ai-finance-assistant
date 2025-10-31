from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import os
from datetime import datetime
import google.generativeai as genai
import numpy as np
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load environment variables from .env file
load_dotenv()

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
# Try to use the latest model, fallback to gemini-pro if not available
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

# Global variable to store current data
current_data = None

def convert_to_json_serializable(obj):
    """Convert numpy types to JSON serializable types"""
    if hasattr(obj, 'item'):
        return obj.item()
    elif hasattr(obj, 'tolist'):
        return obj.tolist()
    else:
        return obj

class FinancialAnalyzer:
    def __init__(self, df):
        self.df = df
        self.df['Month'] = pd.to_datetime(self.df['Month'])
        
    def get_income_trend(self):
        """Generate income trend chart"""
        fig = go.Figure()
        
        # Convert to JSON serializable types
        x_values = [str(date) for date in self.df['Month'].dt.strftime('%Y-%m')]
        y_values = [float(val) for val in self.df['Income']]
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name='Income',
            line=dict(color='#2E8B57', width=3)
        ))
        fig.update_layout(
            title='Monthly Income Trend',
            xaxis_title='Month',
            yaxis_title='Amount (₹)',
            template='plotly_white'
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def get_expense_breakdown(self):
        """Generate expense breakdown pie chart"""
        expense_columns = ['Rent', 'Utilities', 'Insurance', 'Loan_Payments', 
                          'Groceries', 'Transportation', 'Entertainment', 
                          'Healthcare', 'Shopping', 'Dining_Out', 'Subscriptions']
        
        total_expenses = self.df[expense_columns].sum()
        
        # Convert to JSON serializable types
        labels = [str(label) for label in total_expenses.index]
        values = [float(val) for val in total_expenses.values]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3
        )])
        fig.update_layout(
            title='Annual Expense Breakdown',
            template='plotly_white'
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def get_monthly_expenses(self):
        """Generate monthly expenses bar chart"""
        fig = go.Figure()
        
        expense_columns = ['Rent', 'Utilities', 'Insurance', 'Loan_Payments', 
                          'Groceries', 'Transportation', 'Entertainment', 
                          'Healthcare', 'Shopping', 'Dining_Out', 'Subscriptions']
        
        for col in expense_columns:
            # Convert to JSON serializable types
            x_values = [str(date) for date in self.df['Month'].dt.strftime('%Y-%m')]
            y_values = [float(val) for val in self.df[col]]
            
            fig.add_trace(go.Bar(
                name=col,
                x=x_values,
                y=y_values
            ))
        
        fig.update_layout(
            title='Monthly Expenses by Category',
            xaxis_title='Month',
            yaxis_title='Amount (₹)',
            barmode='stack',
            template='plotly_white'
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def get_savings_analysis(self):
        """Generate savings and investment analysis"""
        fig = go.Figure()
        
        # Convert to JSON serializable types
        x_values = [str(date) for date in self.df['Month'].dt.strftime('%Y-%m')]
        savings_values = [float(val) for val in self.df['Savings']]
        investment_values = [float(val) for val in self.df['Investments']]
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=savings_values,
            mode='lines+markers',
            name='Savings',
            line=dict(color='#4169E1', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=investment_values,
            mode='lines+markers',
            name='Investments',
            line=dict(color='#FF6347', width=3)
        ))
        
        fig.update_layout(
            title='Savings and Investments Trend',
            xaxis_title='Month',
            yaxis_title='Amount (₹)',
            template='plotly_white'
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def get_net_income_trend(self):
        """Generate net income trend"""
        fig = go.Figure()
        
        # Convert to JSON serializable types
        x_values = [str(date) for date in self.df['Month'].dt.strftime('%Y-%m')]
        y_values = [float(val) for val in self.df['Net_Income']]
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name='Net Income',
            line=dict(color='#32CD32', width=3),
            fill='tonexty'
        ))
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="red", 
                     annotation_text="Break-even Line")
        
        fig.update_layout(
            title='Monthly Net Income Trend',
            xaxis_title='Month',
            yaxis_title='Amount (₹)',
            template='plotly_white'
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def get_financial_summary(self):
        """Generate financial summary statistics"""
        total_income = float(self.df['Income'].sum())
        total_expenses = float(self.df['Total_Expenses'].sum())
        total_savings = float(self.df['Savings'].sum())
        total_investments = float(self.df['Investments'].sum())
        
        # Calculate actual savings rate based on net income
        # If expenses > income, savings rate should be negative or zero
        net_income = total_income - total_expenses
        if net_income > 0:
            # Positive net income: calculate savings rate as (savings / net_income) * 100
            actual_savings_rate = float((total_savings / net_income) * 100) if net_income > 0 else 0
        else:
            # Negative net income: savings rate is not meaningful, show as 0
            actual_savings_rate = 0.0
        
        # Calculate traditional savings rate (savings / income)
        traditional_savings_rate = float((total_savings / total_income) * 100) if total_income > 0 else 0
        
        summary = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'total_investments': total_investments,
            'net_income': net_income,
            'average_monthly_income': float(self.df['Income'].mean()),
            'average_monthly_expenses': float(self.df['Total_Expenses'].mean()),
            'average_monthly_savings': float(self.df['Savings'].mean()),
            'savings_rate': actual_savings_rate,
            'traditional_savings_rate': traditional_savings_rate,
            'months_in_deficit': int((self.df['Net_Income'] < 0).sum()),
            'largest_expense_category': str(self.df[['Rent', 'Utilities', 'Insurance', 'Loan_Payments', 
                                               'Groceries', 'Transportation', 'Entertainment', 
                                               'Healthcare', 'Shopping', 'Dining_Out', 'Subscriptions']].sum().idxmax())
        }
        return summary

def generate_financial_advice(data_summary, user_question):
    """Generate financial advice using Gemini AI"""
    try:
        context = f"""
        Financial Data Summary:
        - Annual Income: ₹{data_summary['total_income']:,.2f}
        - Annual Expenses: ₹{data_summary['total_expenses']:,.2f}
        - Net Income: ₹{data_summary['net_income']:,.2f}
        - Savings: ₹{data_summary['total_savings']:,.2f}
        - Investments: ₹{data_summary['total_investments']:,.2f}
        - Savings Rate: {data_summary['savings_rate']:.1f}%
        - Months in Deficit: {data_summary['months_in_deficit']}
        - Largest Expense: {data_summary['largest_expense_category']}
        
        Please provide structured, concise financial advice. Format your response as:
        
        ## 🎯 **Key Issues**
        - List 2-3 main problems
        
        ## 💡 **Immediate Actions** 
        - 3-4 specific steps to take now
        
        ## 📊 **Budget Recommendations**
        - Specific expense reduction targets
        - Income improvement suggestions
        
        ## 🎯 **Next Steps**
        - 2-3 follow-up actions
        
        Keep each section brief and actionable. Use bullet points and be specific with amounts and percentages.
        """
        
        prompt = f"{context}\n\nUser Question: {user_question}\n\nPlease provide detailed financial advice and recommendations:"
        
        # Try different models in order of preference
        models_to_try = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']
        
        for model_name in models_to_try:
            try:
                current_model = genai.GenerativeModel(model_name)
                response = current_model.generate_content(prompt)
                return response.text
            except Exception as model_error:
                print(f"Model {model_name} failed: {str(model_error)}")
                continue
        
        # If all models fail, return a basic response
        return f"""## 🎯 **Key Issues**
- {'Spending ₹' + str(abs(data_summary['net_income'])) + ' more than you earn annually' if data_summary['net_income'] < 0 else 'Living within your means'}
- {data_summary['months_in_deficit']} months in deficit spending
- Largest expense: {data_summary['largest_expense_category']}

## 💡 **Immediate Actions**
- Reduce {data_summary['largest_expense_category']} expenses by 15-20%
- Create a detailed monthly budget
- Track every expense for 30 days
- Look for ways to increase income

## 📊 **Budget Recommendations**
- Target: Reduce expenses by ₹{abs(data_summary['net_income']) + 10000:,.0f} annually
- Focus on: {data_summary['largest_expense_category']} optimization
- Build emergency fund: 3-6 months expenses

## 🎯 **Next Steps**
- Set up expense tracking app
- Review and negotiate {data_summary['largest_expense_category']} costs
- Explore additional income sources

*Note: AI service temporarily unavailable. This is basic guidance based on your data.*"""
        
    except Exception as e:
        return f"Sorry, I encountered an error while generating advice: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_data
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            current_data = pd.read_csv(filepath)
            return jsonify({'message': 'File uploaded successfully', 'rows': len(current_data)})
        except Exception as e:
            return jsonify({'error': f'Error reading CSV file: {str(e)}'}), 400
    else:
        return jsonify({'error': 'Please upload a CSV file'}), 400

@app.route('/analyze')
def analyze_data():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        analyzer = FinancialAnalyzer(current_data)
        
        analysis = {
            'income_trend': analyzer.get_income_trend(),
            'expense_breakdown': analyzer.get_expense_breakdown(),
            'monthly_expenses': analyzer.get_monthly_expenses(),
            'savings_analysis': analyzer.get_savings_analysis(),
            'net_income_trend': analyzer.get_net_income_trend(),
            'summary': analyzer.get_financial_summary()
        }
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': f'Error analyzing data: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    data = request.get_json()
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        analyzer = FinancialAnalyzer(current_data)
        summary = analyzer.get_financial_summary()
        advice = generate_financial_advice(summary, user_question)
        
        return jsonify({'response': advice})
    except Exception as e:
        return jsonify({'error': f'Error generating response: {str(e)}'}), 500

@app.route('/load_sample')
def load_sample_data():
    global current_data
    
    try:
        current_data = pd.read_csv('financial_data.csv')
        return jsonify({'message': 'Sample data loaded successfully', 'rows': len(current_data)})
    except Exception as e:
        return jsonify({'error': f'Error loading sample data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
