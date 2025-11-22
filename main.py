"""
Task & Workflow Automation Agent
Using Streamlit and Google Gemini API
"""

import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
from datetime import datetime, timedelta
import random
import io

# Page configuration
st.set_page_config(
    page_title="Task Automation Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .task-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .status-success { color: #28a745; font-weight: 600; }
    .status-pending { color: #ffc107; font-weight: 600; }
    .status-error { color: #dc3545; font-weight: 600; }
    .workflow-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "gemini_configured" not in st.session_state:
    st.session_state.gemini_configured = False
if "task_history" not in st.session_state:
    st.session_state.task_history = []
if "workflows" not in st.session_state:
    st.session_state.workflows = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def configure_gemini(api_key):
    """Configure Gemini API"""
    try:
        genai.configure(api_key=api_key)
        # Try models in order of preference (newest to older)
        models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash-latest']
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'connected' in one word")
                st.session_state.gemini_configured = True
                st.session_state.model = model
                st.session_state.model_name = model_name
                return True
            except Exception:
                continue
        
        st.error("No compatible Gemini model found. Please check your API key.")
        return False
    except Exception as e:
        st.error(f"Failed to configure Gemini: {str(e)}")
        return False


def get_ai_response(prompt, context=""):
    """Get response from Gemini AI"""
    if not st.session_state.gemini_configured:
        return "Please configure your Gemini API key first."
    
    try:
        full_prompt = f"""You are a Task & Workflow Automation Agent. 
        Your role is to help automate repetitive tasks across applications.
        
        Context: {context}
        
        User Request: {prompt}
        
        Provide a helpful, actionable response. If the user wants to automate a task,
        break it down into clear steps. Format your response clearly."""
        
        response = st.session_state.model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error getting AI response: {str(e)}"


def generate_report_data(report_type):
    """Generate sample report data"""
    if report_type == "Sales Report":
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Revenue": [random.randint(50000, 150000) for _ in range(6)],
            "Units Sold": [random.randint(100, 500) for _ in range(6)],
            "Growth %": [round(random.uniform(-5, 15), 2) for _ in range(6)]
        }
    elif report_type == "HR Report":
        data = {
            "Department": ["Engineering", "Sales", "Marketing", "HR", "Finance"],
            "Headcount": [random.randint(20, 100) for _ in range(5)],
            "Open Positions": [random.randint(0, 10) for _ in range(5)],
            "Attrition %": [round(random.uniform(2, 15), 2) for _ in range(5)]
        }
    elif report_type == "Finance Report":
        data = {
            "Category": ["Revenue", "COGS", "Gross Profit", "OpEx", "Net Income"],
            "Q1": [random.randint(100000, 500000) for _ in range(5)],
            "Q2": [random.randint(100000, 500000) for _ in range(5)],
            "Q3": [random.randint(100000, 500000) for _ in range(5)],
            "Q4": [random.randint(100000, 500000) for _ in range(5)]
        }
    else:
        data = {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
    
    return pd.DataFrame(data)


def create_presentation_outline(topic):
    """Use Gemini to create presentation outline"""
    prompt = f"""Create a professional presentation outline for: {topic}
    
    Format the response as JSON with this structure:
    {{
        "title": "Presentation Title",
        "slides": [
            {{"slide_number": 1, "title": "Slide Title", "bullet_points": ["point1", "point2", "point3"]}}
        ]
    }}
    
    Include 5-7 slides with relevant content."""
    
    response = get_ai_response(prompt)
    return response


def execute_workflow(workflow_name, params):
    """Simulate workflow execution"""
    steps = []
    
    if workflow_name == "Employee Onboarding":
        steps = [
            ("Create employee record", "success"),
            ("Generate credentials", "success"),
            ("Assign to department", "success"),
            ("Send welcome email", "success"),
            ("Schedule orientation", "success")
        ]
    elif workflow_name == "Sales Pipeline Update":
        steps = [
            ("Fetch CRM data", "success"),
            ("Update deal stages", "success"),
            ("Calculate forecasts", "success"),
            ("Generate pipeline report", "success"),
            ("Notify sales managers", "success")
        ]
    elif workflow_name == "Invoice Processing":
        steps = [
            ("Extract invoice data", "success"),
            ("Validate amounts", "success"),
            ("Match with PO", "success"),
            ("Route for approval", "success"),
            ("Update accounting system", "success")
        ]
    elif workflow_name == "Monthly Close":
        steps = [
            ("Reconcile accounts", "success"),
            ("Post adjusting entries", "success"),
            ("Generate trial balance", "success"),
            ("Create financial statements", "success"),
            ("Archive documents", "success")
        ]
    
    return steps


# Main UI
st.markdown('<h1 class="main-header">🤖 Task & Workflow Automation Agent</h1>', unsafe_allow_html=True)
st.markdown("Automate repetitive tasks across your applications with AI-powered workflows")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input("Gemini API Key", type="password", 
                            help="Get your API key from Google AI Studio")
    
    if st.button("Configure API", type="primary"):
        if api_key:
            if configure_gemini(api_key):
                st.success("✅ Gemini API configured!")
        else:
            st.warning("Please enter your API key")
    
    st.divider()
    
    st.header("📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tasks Run", len(st.session_state.task_history))
    with col2:
        st.metric("Workflows", len(st.session_state.workflows))
    
    st.divider()
    
    st.header("🕐 Recent Activity")
    for task in st.session_state.task_history[-5:]:
        st.caption(f"✓ {task['name']} - {task['time']}")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 AI Assistant", 
    "📊 Reports", 
    "📑 Presentations",
    "⚡ Workflows",
    "📋 Sheet Updates"
])

# Tab 1: AI Assistant
with tab1:
    st.header("AI-Powered Task Assistant")
    st.markdown("Describe what you want to automate, and I'll help you set it up.")
    
    # Chat interface
    user_input = st.text_area("What would you like to automate?", 
                              placeholder="E.g., 'I need to update my sales sheet every Monday with data from CRM'",
                              height=100)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Get Help", type="primary"):
            if user_input:
                with st.spinner("Analyzing your request..."):
                    response = get_ai_response(user_input)
                    st.session_state.chat_history.append({
                        "user": user_input,
                        "assistant": response,
                        "time": datetime.now().strftime("%H:%M")
                    })
    
    # Display chat history
    for chat in st.session_state.chat_history[-5:]:
        with st.container():
            st.markdown(f"**You ({chat['time']}):** {chat['user']}")
            st.markdown(f"**Agent:** {chat['assistant']}")
            st.divider()

# Tab 2: Reports
with tab2:
    st.header("📊 Automated Report Generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox("Select Report Type", 
                                   ["Sales Report", "HR Report", "Finance Report", "Custom Report"])
        
        date_range = st.date_input("Report Period", 
                                   value=(datetime.now() - timedelta(days=30), datetime.now()))
        
        include_charts = st.checkbox("Include Charts", value=True)
        
        if st.button("📥 Generate Report", type="primary"):
            with st.spinner("Generating report..."):
                df = generate_report_data(report_type)
                st.session_state.current_report = df
                st.session_state.task_history.append({
                    "name": f"Generated {report_type}",
                    "time": datetime.now().strftime("%H:%M")
                })
                st.success(f"✅ {report_type} generated successfully!")
    
    with col2:
        if "current_report" in st.session_state:
            st.dataframe(st.session_state.current_report, use_container_width=True)
            
            # Download button
            csv = st.session_state.current_report.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            if include_charts:
                st.bar_chart(st.session_state.current_report.select_dtypes(include=['int64', 'float64']))

# Tab 3: Presentations
with tab3:
    st.header("📑 AI Presentation Creator")
    
    pres_topic = st.text_input("Presentation Topic", 
                               placeholder="E.g., Q3 Sales Performance Review")
    
    col1, col2 = st.columns(2)
    with col1:
        num_slides = st.slider("Number of Slides", 3, 10, 5)
    with col2:
        style = st.selectbox("Presentation Style", 
                            ["Professional", "Creative", "Minimal", "Data-Driven"])
    
    if st.button("🎨 Create Presentation", type="primary"):
        if pres_topic:
            with st.spinner("Creating presentation outline..."):
                outline = create_presentation_outline(f"{pres_topic} in {style} style with {num_slides} slides")
                
                st.subheader("Generated Presentation Outline")
                st.markdown(outline)
                
                st.session_state.task_history.append({
                    "name": f"Created presentation: {pres_topic}",
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.success("✅ Presentation outline created!")
        else:
            st.warning("Please enter a topic for your presentation")

# Tab 4: Workflows
with tab4:
    st.header("⚡ Workflow Automation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Available Workflows")
        
        workflows = [
            {"name": "Employee Onboarding", "icon": "👤", "dept": "HR"},
            {"name": "Sales Pipeline Update", "icon": "💰", "dept": "Sales"},
            {"name": "Invoice Processing", "icon": "📄", "dept": "Finance"},
            {"name": "Monthly Close", "icon": "📅", "dept": "Finance"}
        ]
        
        selected_workflow = st.radio(
            "Select a workflow to run:",
            [f"{w['icon']} {w['name']} ({w['dept']})" for w in workflows]
        )
        
        workflow_name = selected_workflow.split(" ", 1)[1].rsplit(" (", 1)[0]
        
        st.divider()
        
        # Workflow parameters
        st.subheader("Parameters")
        if "Onboarding" in workflow_name:
            emp_name = st.text_input("Employee Name")
            emp_dept = st.selectbox("Department", ["Engineering", "Sales", "Marketing", "HR"])
            start_date = st.date_input("Start Date")
        elif "Sales" in workflow_name:
            region = st.selectbox("Region", ["North", "South", "East", "West", "All"])
            period = st.selectbox("Period", ["Daily", "Weekly", "Monthly"])
        elif "Invoice" in workflow_name:
            vendor = st.text_input("Vendor Name")
            amount = st.number_input("Amount", min_value=0.0)
        else:
            month = st.selectbox("Month", ["January", "February", "March", "April"])
            year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
    
    with col2:
        st.subheader("Workflow Execution")
        
        if st.button("▶️ Run Workflow", type="primary"):
            with st.spinner(f"Executing {workflow_name}..."):
                steps = execute_workflow(workflow_name, {})
                
                progress = st.progress(0)
                status_container = st.empty()
                
                for i, (step_name, status) in enumerate(steps):
                    import time
                    time.sleep(0.5)
                    progress.progress((i + 1) / len(steps))
                    
                    with status_container.container():
                        for j, (s_name, s_status) in enumerate(steps[:i+1]):
                            if s_status == "success":
                                st.markdown(f"✅ {s_name}")
                            elif s_status == "pending":
                                st.markdown(f"⏳ {s_name}")
                            else:
                                st.markdown(f"❌ {s_name}")
                
                st.session_state.task_history.append({
                    "name": f"Ran workflow: {workflow_name}",
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.success(f"✅ Workflow '{workflow_name}' completed successfully!")
                
                # Generate AI summary
                summary = get_ai_response(
                    f"Provide a brief summary of a completed {workflow_name} workflow execution with all steps successful."
                )
                st.info(f"**AI Summary:** {summary}")

# Tab 5: Sheet Updates
with tab5:
    st.header("📋 Automated Sheet Updates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configure Update")
        
        update_type = st.selectbox("Update Type", [
            "Append New Data",
            "Update Existing Records",
            "Sync from External Source",
            "Calculate & Update Formulas"
        ])
        
        source = st.selectbox("Data Source", [
            "CRM System",
            "ERP Database",
            "API Endpoint",
            "Manual Input",
            "Uploaded File"
        ])
        
        schedule = st.selectbox("Schedule", [
            "Run Once",
            "Daily",
            "Weekly",
            "Monthly",
            "On Trigger"
        ])
        
        if source == "Uploaded File":
            uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
    
    with col2:
        st.subheader("Preview & Execute")
        
        # Sample data preview
        sample_data = pd.DataFrame({
            "ID": [1001, 1002, 1003, 1004, 1005],
            "Name": ["Product A", "Product B", "Product C", "Product D", "Product E"],
            "Current Value": [100, 200, 150, 300, 250],
            "New Value": [110, 195, 160, 320, 245],
            "Status": ["Update", "Update", "Update", "Update", "Update"]
        })
        
        st.dataframe(sample_data, use_container_width=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Execute Update", type="primary"):
                with st.spinner("Updating sheet..."):
                    import time
                    time.sleep(1.5)
                    
                    st.session_state.task_history.append({
                        "name": f"Sheet update: {update_type}",
                        "time": datetime.now().strftime("%H:%M")
                    })
                    
                    st.success("✅ Sheet updated successfully!")
                    st.metric("Records Updated", 5)
        
        with col_b:
            if st.button("📅 Schedule Update"):
                st.session_state.workflows.append({
                    "name": f"Scheduled: {update_type}",
                    "schedule": schedule,
                    "source": source
                })
                st.success(f"✅ Update scheduled: {schedule}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 Task & Workflow Automation Agent | Powered by Google Gemini AI</p>
    <p style='font-size: 0.8rem;'>Automate your repetitive tasks and focus on what matters</p>
</div>
""", unsafe_allow_html=True)
