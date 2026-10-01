import streamlit as st
from modules.module1_user import register_user, login_user
from modules.module2_client import add_client, get_clients
from modules.module3_project import add_project, get_projects
from modules.module4_analytics import add_performance_log, get_performance_logs

st.set_page_config(page_title="Freelancing App", page_icon="💻", layout="wide")

st.title("🚀 Intelligent Improvisation for Digital Entrepreneurs")
st.subheader("Freelancer Project Management Web Dashboard")

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Register":
        st.subheader("Create New Freelancer Account")
        reg_username = st.text_input("Username")
        reg_email = st.text_input("Email")
        reg_password = st.text_input("Password", type="password")
        reg_skills = st.text_area("Skills & Portfolio Details")
        
        if st.button("Register"):
            if reg_username and reg_email and reg_password:
                success, message = register_user(reg_username, reg_email, reg_password, reg_skills)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please fill all required fields!")

    elif choice == "Login":
        st.subheader("Freelancer Login")
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            success, result = login_user(login_email, login_password)
            if success:
                st.success(f"Welcome back, {result['username']}!")
                st.session_state['user'] = result
                st.rerun()
            else:
                st.error(result)

else:
    user = st.session_state['user']
    st.sidebar.success(f"Logged in as: {user['username']}")
    
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()

    app_menu = ["Dashboard Home", "Client Management", "Project Execution", "Performance & Analytics"]
    selected_tab = st.sidebar.selectbox("Module Menu", app_menu)

    if selected_tab == "Dashboard Home":
        st.subheader(f"Welcome, {user['username']}! 👋")
        st.write("Use the sidebar to navigate through your project modules.")
        st.info(f"Your Registered Skills: {user['skills']}")

    elif selected_tab == "Client Management":
        st.subheader("🤝 Client & Lead Operations (Module 2)")
        
        with st.form("client_form"):
            st.write("Add New Client / Lead")
            c_name = st.text_input("Client Name")
            comp_name = st.text_input("Company Name")
            c_email = st.text_input("Contact Email")
            c_status = st.selectbox("Lead Status", ["Lead", "Active", "Completed"])
            
            submitted = st.form_submit_button("Save Client")
            if submitted:
                if c_name and c_email:
                    success, msg = add_client(user['user_id'], c_name, comp_name, c_email, c_status)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Client Name and Email are required!")

        st.divider()
        st.subheader("Your Clients List")
        clients = get_clients(user['user_id'])
        if clients:
            for client in clients:
                st.write(f"**Name:** {client['client_name']} | **Company:** {client['company_name']} | **Email:** {client['contact_email']} | **Status:** {client['status']}")
        else:
            st.info("No clients added yet.")

    elif selected_tab == "Project Execution":
        st.subheader("📊 Project Execution & Workflow (Module 3)")
        
        clients = get_clients(user['user_id'])
        if not clients:
            st.warning("Please add a client first before creating a project!")
        else:
            client_options = {c['client_name']: c['client_id'] for c in clients}
            
            with st.form("project_form"):
                st.write("Create New Project & Set Milestones")
                selected_client_name = st.selectbox("Select Client", list(client_options.keys()))
                proj_name = st.text_input("Project Name")
                milestones = st.text_area("Milestones Description (Sub-modules / Tasks)")
                deadline = st.date_input("Project Deadline")
                proj_status = st.selectbox("Project Status", ["Pending", "In Progress", "Finished"])
                
                proj_submitted = st.form_submit_button("Save Project")
                if proj_submitted:
                    if proj_name and milestones:
                        client_id = client_options[selected_client_name]
                        success, msg = add_project(client_id, proj_name, milestones, deadline, proj_status)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                    else:
                        st.warning("Project Name and Milestones are required!")

            st.divider()
            st.subheader("Active Projects List")
            projects = get_projects(user['user_id'])
            if projects:
                for proj in projects:
                    st.write(f"**Project:** {proj['project_name']} | **Client:** {proj['client_name']} | **Deadline:** {proj['deadline']} | **Status:** {proj['project_status']}")
                    st.text(f"Milestones: {proj['milestones']}")
                    st.markdown("---")
            else:
                st.info("No projects added yet.")

    elif selected_tab == "Performance & Analytics":
        st.subheader("📈 Performance & Analytics (Module 4)")
        
        projects = get_projects(user['user_id'])
        if not projects:
            st.warning("Please create a project first to log performance analytics!")
        else:
            project_options = {p['project_name']: p['project_id'] for p in projects}
            
            with st.form("analytics_form"):
                st.write("Log Project Income, Feedback & Improvisation Notes")
                selected_proj_name = st.selectbox("Select Project", list(project_options.keys()))
                income = st.number_input("Income Generated ($ / INR)", min_value=0.0, format="%.2f")
                feedback = st.slider("Client Feedback Score (1 to 10)", min_value=1, max_value=10, value=5)
                notes = st.text_area("Improvisational Strategy Notes / Learnings")
                
                analytics_submitted = st.form_submit_button("Save Analytics Log")
                if analytics_submitted:
                    proj_id = project_options[selected_proj_name]
                    success, msg = add_performance_log(proj_id, income, feedback, notes)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

            st.divider()
            st.subheader("Performance Analytics Reports")
            logs = get_performance_logs(user['user_id'])
            if logs:
                for log in logs:
                    st.write(f"**Project:** {log['project_name']} | **Client:** {log['client_name']}")
                    st.write(f"💰 **Income Generated:** {log['income_generated']} | ⭐ **Feedback Score:** {log['feedback_score']}/10")
                    st.text(f"Improvisation Notes: {log['improvisation_notes']}")
                    st.markdown("---")
            else:
                st.info("No performance logs recorded yet.")