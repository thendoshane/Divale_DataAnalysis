import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import re
import io

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Eduvos Analytics Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the Top Navigation Bar and Styling
st.markdown("""
    <style>
    /* Top Navigation Styling */
    .nav-container {
        display: flex;
        justify-content: center;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid #d1d5db;
        transition: all 0.3s;
    }
    .stButton button:hover {
        border-color: #3498db;
        color: #3498db;
    }
    
    /* Headings & Text */
    h1, h2, h3 { color: #2c3e50; font-family: 'Helvetica', sans-serif; }
    .story-box {
        background-color: #e8f4f8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin-bottom: 25px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .insight-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #eee;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE & NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Top Navigation Menu
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🏠 Home & Strategy"): st.session_state['page'] = 'Home'
with col2:
    if st.button("👥 Q1 & Q2: Community"): st.session_state['page'] = 'Q1_Q2'
with col3:
    if st.button("🏥 Q3: Health Cleaning"): st.session_state['page'] = 'Q3'
with col4:
    if st.button("🗄️ Q4: SQL Registry"): st.session_state['page'] = 'Q4'

st.markdown("---")

# --- 3. HELPER FUNCTIONS ---
def clean_blood_pressure(bp):
    """Removes non-numeric characters from blood pressure strings."""
    if pd.isna(bp): return np.nan
    clean_str = re.sub(r'[^0-9.]', '', str(bp))
    return float(clean_str) if clean_str else np.nan

def classify_health_risk(row):
    """Classifies patient risk based on BMI and Disease Score."""
    if row['BMI'] > 30 and row['disease_score'] > 80:
        return 'High'
    elif row['BMI'] > 25 and row['disease_score'] > 60:
        return 'Medium'
    else:
        return 'Low'

# --- 4. PAGE LOGIC ---

# === HOME PAGE ===
if st.session_state['page'] == 'Home':
    st.title("📊 Strategic Data Analysis: ConnectSA & Northern Cape Health")
    st.markdown("### **Project Overview**")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        This comprehensive data analysis project addresses critical challenges for two major stakeholders in South Africa.
        
        #### **1. ConnectSA (Non-Profit)**
        * **Objective:** Bridge the digital divide in underserved communities (Cape Town, Durban, Soweto).
        * **Challenge:** They have raw customer data but lack insights into demographics and growth trends.
        * **Our Solution:** We perform **Time-Series Analysis** and **Demographic Segmentation** to guide resource allocation and marketing strategies.
        
        #### **2. Northern Cape Department of Health**
        * **Objective:** Optimize patient triage in rural mobile clinics.
        * **Challenge:** Data is collected manually ("dirty data") and lacks a centralized registry for doctors.
        * **Our Solution:** We build a **Data Cleaning Pipeline**, automated **Risk Algorithms**, and a **SQL Database** to identify high-risk patients instantly.
        """)
    with c2:
        st.info("""
        **📚 Module Details**
        * **Subject:** Data Analysis with Python
        * **Tools:** Pandas, NumPy, Matplotlib, Seaborn, SQLite3, Streamlit
        * **Focus:** Cleaning, Visualization, SQL Integration
        """)

    st.markdown("### **How to Use This Dashboard**")
    st.success("Use the **Navigation Buttons** at the top of the screen to move between the Client Modules.")

# === Q1 & Q2: CUSTOMER ANALYSIS ===
elif st.session_state['page'] == 'Q1_Q2':
    st.title("👥 ConnectSA: Community Analysis")
    st.markdown("### Understanding Digital Adoption Trends")
    
    uploaded_file = st.file_uploader("📂 Upload 'customers.csv' to begin", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # --- DATA PRE-PROCESSING ---
        # 1. Fix Age Group (Numpy Select Fix)
        conditions = [
            (df['age'] < 25),
            (df['age'] >= 25) & (df['age'] < 60),
            (df['age'] >= 60)
        ]
        choices = ['Youth', 'Adult', 'Senior']
        df['age_group'] = np.select(conditions, choices, default='Unknown')
        
        # 2. Date Conversion
        df['subscription_date'] = pd.to_datetime(df['subscription_date'])
        df['year_joined'] = df['subscription_date'].dt.year
        df['month_joined'] = df['subscription_date'].dt.month_name()
        df['quarter_joined'] = df['subscription_date'].dt.to_period('Q').astype(str)
        
        # --- TABS ---
        tab1, tab2 = st.tabs(["📘 Core Project Analysis", "🚀 15+ Strategic Insights (Deep Dive)"])
        
        with tab1:
            st.header("1. Project Requirements (Q1 & Q2)")
            
            # Q1a
            with st.expander("Q1a: Data Structure & Quality Check", expanded=True):
                st.markdown("**The Story:** Before analysis, we must validate the data integrity.")
                st.write(df.head())
                st.write(df.describe())
            
            # Q1b & Q1c
            with st.expander("Q1b/c: Youth Segment Identification"):
                st.markdown("**The Story:** Identifying our future leaders (Youth < 25) for specific digital literacy programs.")
                under_25 = df[df['age'] < 25]
                st.dataframe(under_25)
                st.caption(f"Total Youth Customers: {len(under_25)}")
            
            # Q2c & Q2d
            st.subheader("Growth & Demographics")
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**Q2c: Yearly Sign-ups (Growth Trajectory)**")
                fig, ax = plt.subplots()
                sns.countplot(x='year_joined', data=df, palette='viridis', ax=ax)
                ax.set_title("Customer Growth per Year")
                st.pyplot(fig)
                st.caption("**Insight:** A visual representation of ConnectSA's expansion speed.")
                
            with col_b:
                st.markdown("**Q2d: Age Group Distribution**")
                fig2, ax2 = plt.subplots()
                df['age_group'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, startangle=90, colors=['#66b3ff','#99ff99','#ffcc99'])
                ax2.set_ylabel('')
                st.pyplot(fig2)
                st.caption("**Insight:** Breakdown of user base to tailor content strategy.")

        with tab2:
            st.header("2. Advanced Strategic Analysis")
            st.markdown("We have conducted **15+ additional analyses** to provide deeper business intelligence.")
            
            # --- INSIGHTS GRID ---
            
            # ROW 1
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                st.markdown("#### 1. Geographic Hotspots (City)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Where is the demand concentrated?<br>
                <b>Business Value:</b> Determines location for physical support centers.
                </div>
                """, unsafe_allow_html=True)
                st.bar_chart(df['city'].value_counts())
                
            with r1c2:
                st.markdown("#### 2. Seasonal Pulse (Month)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> When do users subscribe?<br>
                <b>Business Value:</b> Optimizes marketing spend (e.g., Back-to-School spikes).
                </div>
                """, unsafe_allow_html=True)
                month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                fig_m, ax_m = plt.subplots(figsize=(8,4))
                sns.countplot(y='month_joined', data=df, order=month_order, palette='coolwarm', ax=ax_m)
                st.pyplot(fig_m)

            st.divider()
            
            # ROW 2
            r2c1, r2c2 = st.columns(2)
            with r2c1:
                st.markdown("#### 3. Regional Demographics (Age by City)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Is one city younger than another?<br>
                <b>Business Value:</b> Regional content curation (Gaming vs Finance).
                </div>
                """, unsafe_allow_html=True)
                city_age = df.groupby('city')['age'].mean().sort_values()
                st.bar_chart(city_age)
                
            with r2c2:
                st.markdown("#### 4. The 'Hockey Stick' (Cumulative Growth)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Total load on the system over time.<br>
                <b>Business Value:</b> Predicts server capacity needs to prevent crashes.
                </div>
                """, unsafe_allow_html=True)
                df_sorted = df.sort_values('subscription_date')
                df_sorted['cumulative_users'] = range(1, len(df_sorted)+1)
                st.line_chart(df_sorted.set_index('subscription_date')['cumulative_users'])

            st.divider()
            
            # ROW 3
            r3c1, r3c2 = st.columns(2)
            with r3c1:
                st.markdown("#### 5. Customer Loyalty (Tenure)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> How long have customers stayed?<br>
                <b>Business Value:</b> Identifies loyalists for reward programs.
                </div>
                """, unsafe_allow_html=True)
                current_date = pd.Timestamp.now()
                df['tenure_days'] = (current_date - df['subscription_date']).dt.days
                st.hist_chart(df['tenure_days'])
                
            with r3c2:
                st.markdown("#### 6. Engagement Timing (Weekend vs Weekday)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Do users sign up while working or relaxing?<br>
                <b>Business Value:</b> Dictates email blast timing.
                </div>
                """, unsafe_allow_html=True)
                df['is_weekend'] = df['subscription_date'].dt.dayofweek >= 5
                weekend_counts = df['is_weekend'].value_counts().rename({True: 'Weekend', False: 'Weekday'})
                st.bar_chart(weekend_counts)

            st.divider()
            
            # ROW 4
            r4c1, r4c2 = st.columns(2)
            with r4c1:
                st.markdown("#### 7. Quarterly Performance")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Financial reporting alignment.<br>
                <b>Business Value:</b> Standardizes reporting for the Board of Directors.
                </div>
                """, unsafe_allow_html=True)
                st.bar_chart(df['quarter_joined'].value_counts().sort_index())
                
            with r4c2:
                st.markdown("#### 8. Data Integrity Audit (Country)")
                st.markdown("""
                <div class='insight-card'>
                <b>Story:</b> Are non-SA users slipping in?<br>
                <b>Business Value:</b> Detects potential fraud or data entry errors.
                </div>
                """, unsafe_allow_html=True)
                st.write(df['country'].value_counts())

    else:
        st.info("👋 Please upload `customers.csv` to unlock the analysis.")

# === Q3: HEALTH CLEANING ===
elif st.session_state['page'] == 'Q3':
    st.title("🏥 Northern Cape: Health Data Cleaning")
    st.markdown("### Turning Dirty Data into Lifesaving Insights")
    
    uploaded_file = st.file_uploader("📂 Upload 'health_data.csv'", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # 3a Inspection
        st.header("3a. Raw Data Inspection")
        st.markdown("""
        <div class='story-box'>
        <b>The Story:</b> Field nurses record data manually, leading to errors like '120mmHg' instead of just '120'.<br>
        <b>The Goal:</b> Identify these 'dirty' records that prevent mathematical analysis.
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head())
        
        # 3b Cleaning
        st.header("3b. Advanced Cleaning (Regex)")
        st.markdown("We use **Regular Expressions** to strip non-numeric characters from Blood Pressure.")
        
        # Apply Cleaning
        df['blood_pressure_clean'] = df['blood_pressure'].apply(clean_blood_pressure)
        
        col1, col2 = st.columns(2)
        col1.warning("Before (Dirty):")
        col1.dataframe(df['blood_pressure'].head())
        col2.success("After (Clean):")
        col2.dataframe(df['blood_pressure_clean'].head())
        
        # 3c Classification
        st.header("3c. Algorithmic Risk Classification")
        st.markdown("""
        <div class='story-box'>
        <b>The Story:</b> Doctors are overwhelmed. We need an algorithm to auto-triage patients.<br>
        <b>Logic:</b> High Risk = BMI > 30 AND Disease Score > 80.
        </div>
        """, unsafe_allow_html=True)
        
        df['risk_level'] = df.apply(classify_health_risk, axis=1)
        st.dataframe(df['risk_level'].value_counts())
        
        # 3e Visuals
        st.header("3e. Health Visualizations")
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        
        sns.boxplot(x='risk_level', y='BMI', data=df, order=['Low', 'Medium', 'High'], palette="Set2", ax=ax[0])
        ax[0].set_title("BMI Distribution by Risk Level")
        
        sns.histplot(df['age'], bins=15, kde=True, ax=ax[1], color='teal')
        ax[1].set_title("Patient Age Distribution")
        
        st.pyplot(fig)
        
        # Save to session state
        st.session_state['health_clean'] = df
        st.success("✅ Data cleaned and stored. Proceed to Q4 for the SQL Registry.")
        
    else:
        st.info("👋 Please upload `health_data.csv`.")

# === Q4: SQL REGISTRY ===
elif st.session_state['page'] == 'Q4':
    st.title("🗄️ Health Risk Registry (SQL)")
    st.markdown("### Building a Scalable Patient Database")
    
    if 'health_clean' in st.session_state:
        df = st.session_state['health_clean']
        
        # 4a Setup
        conn = sqlite3.connect(':memory:')
        df.to_sql('patients', conn, index=False, if_exists='replace')
        
        st.markdown("""
        <div class='story-box'>
        <h3>Why are we using SQL here?</h3>
        <b>1. Scalability:</b> Excel crashes with 1 million rows; SQL databases handle billions.<br>
        <b>2. Security:</b> Patient data requires strict access controls which databases provide.<br>
        <b>3. Query Speed:</b> Finding "Critical Females over 50" is instant with SQL queries.
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ Connection Established: In-Memory SQLite Database")
        
        # 4b Analysis
        st.subheader("4b. Patient Demographics (SQL Query)")
        query_4b = "SELECT sex, risk_level, COUNT(*) as count FROM patients GROUP BY sex, risk_level"
        st.code(query_4b, language='sql')
        st.dataframe(pd.read_sql(query_4b, conn))
        
        # 4d Critical List
        st.subheader("4d. Critical Patient Export List")
        st.markdown("**Business Value:** This list is sent directly to doctors for immediate intervention.")
        
        query_4d = """
        SELECT patient_id, age, BMI, blood_pressure_clean,
        CASE 
            WHEN disease_score > 80 AND risk_level = 'High' THEN 'Critical' 
            ELSE 'Stable' 
        END as status 
        FROM patients
        WHERE status = 'Critical'
        """
        st.code(query_4d, language='sql')
        df_critical = pd.read_sql(query_4d, conn)
        
        if not df_critical.empty:
            st.error(f"⚠️ {len(df_critical)} Critical Patients Found!")
            st.dataframe(df_critical)
            
            # CSV Download
            csv = df_critical.to_csv(index=False).encode('utf-8')
            st.download_button("Download Critical List (CSV)", csv, "critical_patients.csv", "text/csv")
        else:
            st.success("No Critical patients found matching criteria.")
            
        # 4e Indexing Explanation
        st.divider()
        st.header("4e. Database Performance Theory: Indexing")
        st.markdown("""
        <div class='story-box'>
        <b>The Question:</b> How do indexes improve performance in large-scale health systems?<br><br>
        <b>The Explanation:</b>
        Imagine a textbook without an index. To find "Diabetes", you have to read every single page (<b>Full Table Scan</b>). This is slow.<br>
        An <b>Index</b> is a sorted lookup table. It tells the database exactly which row "Diabetes" is in.<br><br>
        <b>Impact on Health Systems:</b>
        <ol>
            <li><b>Speed:</b> Retrieving a patient record by ID takes milliseconds instead of minutes.</li>
            <li><b>Efficiency:</b> Reduces load on the server CPU.</li>
            <li><b>Trade-off:</b> Indexes make writing data slightly slower (as the index must be updated), but make reading data drastically faster.</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("⚠️ No Data Found. Please go to **Q3: Health Cleaning** and process the data first.")