import streamlit as st
from datetime import datetime

st.set_page_config(page_title="FinTune")

st.title("FinTune | be in tune with your finances")

st.subheader("Your personal finance manager")

# Initialize session state for user management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False    # Track if user is currently logged in
if 'users' not in st.session_state:
    st.session_state.users = {}           # Dictionary to store user credentials and data

# Function to handle new account creation
def create_account():
    st.session_state.signup_error = None  # Reset any previous error messages
    username = st.session_state.new_username
    password = st.session_state.new_password
    confirm_password = st.session_state.confirm_password
    
    # Validate password confirmation
    if password != confirm_password:
        st.session_state.signup_error = "Passwords don't match!"
        return
    
    # Check if username is already taken
    if username in st.session_state.users:
        st.session_state.signup_error = "Username already exists!"
        return
    
    # Create new user profile    
    st.session_state.users[username] = {
        'password': password,
        'created_at': datetime.now()
    }
    st.success("Account created successfully! Please log in.")
    st.session_state.show_signup = False

# Function to handle user login
def login():
    username = st.session_state.username
    password = st.session_state.password
    
    # Verify credentials
    if username in st.session_state.users and st.session_state.users[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
    else:
        st.error("Invalid username or password")

# Main authentication interface
if not st.session_state.logged_in:
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Login tab contents
    with tab1:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=login)
    
    # Sign up tab contents
    with tab2:
        st.text_input("Choose Username", key="new_username")
        st.text_input("Choose Password", type="password", key="new_password")
        st.text_input("Confirm Password", type="password", key="confirm_password")
        st.button("Create Account", on_click=create_account)
        # Display any signup errors
        if 'signup_error' in st.session_state and st.session_state.signup_error:
            st.error(st.session_state.signup_error)

# Display logged-in user interface
else:
    st.write(f"Welcome, {st.session_state.current_user}!")
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()  # Refresh the page after logout


