"""
Step 5: Streamlit Dashboard (Enhanced Design)
Interactive web dashboard for SmartSpend AI expense tracking.
Features: AI-powered categorization, analytics, and spending visualization.
"""

import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config at the very top, before any other Streamlit commands
st.set_page_config(
    page_title="SmartSpend AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_operations import insert_expense, fetch_all_expenses, fetch_by_category
from src.predict import predict_category


# ==================== CUSTOM CSS STYLING ====================
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #0066CC;
        --secondary-color: #00B4D8;
        --accent-color: #90E0EF;
        --success-color: #06D6A0;
        --danger-color: #EF476F;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 102, 204, 0.1);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0066CC;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-card-title {
        font-size: 0.9rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card-value {
        font-size: 1.8rem;
        color: #0066CC;
        font-weight: 700;
    }
    
    /* Input form styling */
    .input-section {
        background: #F8F9FA;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
    }
    
    /* Success message styling */
    .success-box {
        background: linear-gradient(135deg, #06D6A0 0%, #00B4D8 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .predicted-category {
        display: inline-block;
        background: #0066CC;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%);
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-header h2 {
        margin: 0.5rem 0;
        font-size: 1.3rem;
    }
    
    .sidebar-stat {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #00B4D8;
    }
    
    .sidebar-stat-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    .sidebar-stat-value {
        font-size: 1.5rem;
        color: #0066CC;
        font-weight: 700;
        margin-top: 0.3rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F2F6;
        border-radius: 8px 8px 0px 0px;
        color: #666;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] [data-baseweb="tab"] {
        background-color: #0066CC;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 50px;
        background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.2);
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 12px rgba(0, 102, 204, 0.3);
        transform: translateY(-2px);
    }
    
    /* Divider styling */
    hr {
        background: linear-gradient(to right, transparent, #0066CC, transparent);
        height: 2px;
        border: none;
        margin: 2rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        padding: 2rem 0;
        border-top: 1px solid #E9ECEF;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== DATA LOADING ====================
def load_expenses_from_db():
    """Load all expenses from the database."""
    expenses = fetch_all_expenses("database/expenses.db")
    if expenses:
        df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Amount', 'Description', 
                                             'Category', 'Predicted_Category'])
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()


def add_new_expense(date, amount, description):
    """Add a new expense with AI prediction."""
    try:
        cleaned_description = description.lower().strip()
        predicted_category = predict_category(cleaned_description)
        
        success = insert_expense(
            date=date.strftime("%Y-%m-%d"),
            amount=amount,
            description=cleaned_description,
            category=predicted_category,
            predicted_category=predicted_category,
            db_path="database/expenses.db"
        )
        
        if success:
            return True, predicted_category
        else:
            return False, "Failed to insert expense"
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== CHART FUNCTIONS ====================
def create_pie_chart(df):
    """Create interactive pie chart with hover labels."""
    category_spending = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    fig = px.pie(
        values=category_spending.values,
        names=category_spending.index,
        title="💰 Spending Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=True,
        height=400,
        template='plotly_white',
        font=dict(size=12)
    )
    
    return fig


def create_trend_chart(df):
    """Create interactive line chart with area fill."""
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_spending = df.groupby('Month')['Amount'].sum().reset_index().sort_values('Month')
    
    fig = go.Figure()
    
    # Add filled area
    fig.add_trace(go.Scatter(
        x=monthly_spending['Month'],
        y=monthly_spending['Amount'],
        fill='tozeroy',
        fillcolor='rgba(0, 180, 216, 0.2)',
        line=dict(color='#00B4D8', width=3),
        mode='lines+markers',
        name='Spending',
        hovertemplate='<b>%{x}</b><br>Total: ₹%{y:,.2f}<extra></extra>',
        marker=dict(size=8, color='#0066CC')
    ))
    
    fig.update_layout(
        title='📈 Monthly Spending Trend',
        xaxis_title='Month',
        yaxis_title='Total Amount (₹)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=False,
        font=dict(size=12)
    )
    
    fig.update_xaxes(tickangle=-45)
    
    return fig


def create_category_bar_chart(df):
    """Create category spending bar chart."""
    category_data = df.groupby('Category').agg({
        'Amount': 'sum',
        'ID': 'count'
    }).reset_index().sort_values('Amount', ascending=False)
    category_data.columns = ['Category', 'Total Amount', 'Count']
    
    fig = px.bar(
        category_data,
        x='Category',
        y='Total Amount',
        title='📊 Category Spending Overview',
        color='Total Amount',
        color_continuous_scale='Blues',
        text='Total Amount',
        hover_data={'Count': True, 'Total Amount': ':.2f'}
    )
    
    fig.update_traces(
        texttemplate='₹%{y:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Amount: ₹%{customdata[1]:,.2f}<br>Transactions: %{customdata[0]}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        template='plotly_white',
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig




# ==================== MAIN APP ====================
def main():
    """Main Streamlit application."""
    
    # ========== HEADER ==========
    st.markdown("""
        <div class="header-container">
            <h1>💰 SmartSpend AI</h1>
            <p>AI-Powered Expense Tracking & Intelligent Categorization</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Load data
    df = load_expenses_from_db()
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <h2>📊 Dashboard</h2>
                <p style="margin: 0; opacity: 0.9;">SmartSpend AI</p>
            </div>
            """, unsafe_allow_html=True)
        
        if len(df) > 0:
            st.markdown("""
                <div class="sidebar-stat">
                    <div class="sidebar-stat-label">Total Expenses</div>
                    <div class="sidebar-stat-value">₹{:,.0f}</div>
                </div>
                """.format(df['Amount'].sum()), unsafe_allow_html=True)
            
            st.markdown("""
                <div class="sidebar-stat">
                    <div class="sidebar-stat-label">Total Transactions</div>
                    <div class="sidebar-stat-value">{}</div>
                </div>
                """.format(len(df)), unsafe_allow_html=True)
            
            top_category = df['Category'].value_counts().idxmax()
            st.markdown("""
                <div class="sidebar-stat">
                    <div class="sidebar-stat-label">Top Category</div>
                    <div class="sidebar-stat-value">{}</div>
                </div>
                """.format(top_category), unsafe_allow_html=True)
            
            st.markdown("""
                <div class="sidebar-stat">
                    <div class="sidebar-stat-label">Average Transaction</div>
                    <div class="sidebar-stat-value">₹{:,.0f}</div>
                </div>
                """.format(df['Amount'].mean()), unsafe_allow_html=True)
        else:
            st.info("📭 No expenses yet. Add your first expense to see stats!")
        
        st.divider()
        
        st.markdown("**About SmartSpend AI**")
        st.markdown("""
        An AI-powered expense tracker that automatically categorizes 
        your spending using machine learning. Track, analyze, and 
        optimize your finances with ease.
        
        **Features:**
        - 🤖 AI-powered categorization
        - 📊 Interactive analytics
        - 💾 Persistent storage
        - 📱 Responsive design
        """)
        
        st.divider()
        
        st.markdown("**Version:** 1.0  \n**Status:** ✓ Active")
    
    # ========== MAIN CONTENT - TABS ==========
    tab1, tab2, tab3 = st.tabs(["📝 Add Expense", "📋 All Expenses", "📊 Analytics"])
    
    # ==================== TAB 1: ADD EXPENSE ====================
    with tab1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            expense_date = st.date_input(
                "📅 Date",
                value=datetime.now().date(),
                label_visibility="visible"
            )
        
        with col2:
            amount = st.number_input(
                "💵 Amount (₹)",
                min_value=0.0,
                step=1.0,
                value=0.0,
                label_visibility="visible"
            )
        
        description = st.text_input(
            "📝 Description",
            placeholder="e.g., 'Starbucks coffee', 'Uber ride', 'Netflix subscription'",
            label_visibility="visible"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add Expense button
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("➕ Add Expense", use_container_width=True, type="primary"):
                if amount <= 0:
                    st.error("❌ Amount must be greater than 0", icon="⚠️")
                elif not description.strip():
                    st.error("❌ Please enter a description", icon="⚠️")
                else:
                    success, result = add_new_expense(expense_date, amount, description)
                    
                    if success:
                        st.balloons()
                        st.markdown(f"""
                            <div class="success-box">
                            <h3 style="margin-top: 0;">✅ Expense Added Successfully!</h3>
                            <p style="margin: 0.5rem 0 0 0;">
                            Predicted Category: <span class="predicted-category">{result}</span>
                            </p>
                            </div>
                            """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.error(f"❌ {result}", icon="⚠️")
        
        st.divider()
        
        # Quick summary
        if len(df) > 0:
            st.subheader("💹 Quick Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                    <div class="metric-card-title">Total Spent</div>
                    <div class="metric-card-value">₹{df['Amount'].sum():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                    <div class="metric-card-title">Transactions</div>
                    <div class="metric-card-value">{len(df)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                    <div class="metric-card-title">Average</div>
                    <div class="metric-card-value">₹{df['Amount'].mean():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                    <div class="metric-card-title">Highest</div>
                    <div class="metric-card-value">₹{df['Amount'].max():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ==================== TAB 2: ALL EXPENSES ====================
    with tab2:
        st.subheader("All Expenses")
        
        if len(df) == 0:
            st.info("📭 No expenses recorded yet. Add your first expense to get started!")
        else:
            # Category filter
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                categories = ["All"] + sorted(df['Category'].unique().tolist())
                selected_category = st.selectbox(
                    "Filter by Category",
                    categories,
                    label_visibility="collapsed"
                )
            
            # Filter dataframe
            if selected_category == "All":
                filtered_df = df.copy()
            else:
                filtered_df = df[df['Category'] == selected_category]
            
            # Display table with column config
            display_df = filtered_df[['Date', 'Amount', 'Description', 'Category', 'Predicted_Category']].copy()
            display_df = display_df.sort_values('Date', ascending=False).reset_index(drop=True)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                    "Amount": st.column_config.NumberColumn("Amount", format="₹ %.2f"),
                    "Description": st.column_config.TextColumn("Description", width="large"),
                    "Category": st.column_config.TextColumn("Category"),
                    "Predicted_Category": st.column_config.TextColumn("Predicted Category")
                },
                hide_index=True
            )
            
            # Summary for filtered data
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", f"₹{filtered_df['Amount'].sum():,.2f}")
            with col2:
                st.metric("Count", len(filtered_df))
            with col3:
                st.metric("Average", f"₹{filtered_df['Amount'].mean():,.2f}")
    
    # ==================== TAB 3: ANALYTICS ====================
    with tab3:
        if len(df) == 0:
            st.warning("📊 No expense data available yet. Add expenses to see analysis!")
        else:
            # Metrics cards
            st.subheader("📈 Summary Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Spent", f"₹{df['Amount'].sum():,.2f}", 
                         delta=f"{len(df)} transactions")
            
            with col2:
                st.metric("Average Transaction", f"₹{df['Amount'].mean():,.2f}")
            
            with col3:
                top_cat = df['Category'].value_counts().idxmax()
                st.metric("Top Category", top_cat, 
                         delta=f"{df['Category'].value_counts().max()} times")
            
            with col4:
                st.metric("Highest Expense", f"₹{df['Amount'].max():,.2f}")
            
            st.divider()
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_pie_chart(df), use_container_width=True)
            
            with col2:
                st.plotly_chart(create_trend_chart(df), use_container_width=True)
            
            st.plotly_chart(create_category_bar_chart(df), use_container_width=True)
            
            # Category summary table
            st.subheader("📊 Category Breakdown")
            
            category_summary = df.groupby('Category').agg({
                'Amount': ['sum', 'count', 'mean', 'max']
            }).round(2)
            category_summary.columns = ['Total Spent', 'Count', 'Average', 'Max']
            category_summary = category_summary.sort_values('Total Spent', ascending=False)
            
            st.dataframe(
                category_summary,
                use_container_width=True,
                column_config={
                    "Total Spent": st.column_config.NumberColumn("Total Spent", format="₹ %.2f"),
                    "Count": st.column_config.NumberColumn("Count"),
                    "Average": st.column_config.NumberColumn("Average", format="₹ %.2f"),
                    "Max": st.column_config.NumberColumn("Max", format="₹ %.2f")
                }
            )
    
    # ========== FOOTER ==========
    st.markdown("""
        <div class="footer">
        <p>SmartSpend AI v1.0 | AI-powered expense categorization | Built with Streamlit & Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
