def get_custom_css():
    """Returns custom CSS for the Streamlit application."""
    
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global Styles - FORCE DARK TEXT */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1F2937 !important; /* Force dark text globally */
        }
        
        /* App Background */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* Streamlit Header (Hide default decoration but keep functionality) */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* [Removed Dashboard Styles] */
        
        /* Override Streamlit Chat Message Backgrounds */
        .stChatMessage {
            background-color: transparent !important;
        }
        
        div[data-testid="stChatMessage"] {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }

        /* Assistant Message */
        div[data-testid="stChatMessage"][data-test-role="assistant"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            color: #1F2937 !important;
        }

        /* User Message */
        div[data-testid="stChatMessage"][data-test-role="user"] {
            background-color: #F8FAFC !important;
            color: #1F2937 !important;
        }
        
        /* Markdown Text Color Fix */
        .stMarkdown p {
            color: #1F2937 !important;
        }
        
        /* -------------------------------------------------------------------------- */
        /* Sidebar & Inputs */
        /* -------------------------------------------------------------------------- */
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Also force dark text in sidebar markdown */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #1F2937 !important;
        }
        
        /* Input Fields */
        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1;
            border-radius: 0.375rem;
            padding: 0.5rem;
            color: #1F2937 !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #F59E0B !important;
            box-shadow: 0 0 0 1px #F59E0B !important;
        }
        
        /* File Uploader */
        div[data-testid="stFileUploader"] {
            border: 1px dashed #CBD5E1;
            border-radius: 0.5rem;
            padding: 1rem;
            background-color: #F8FAFC;
        }
        div[data-testid="stFileUploader"] div {
            color: #1F2937 !important;
        }
        
        /* Button Styles */
         div.stButton > button[kind="primary"] {
            background-color: #F59E0B !important;
            color: white !important;
            border: 1px solid #D97706 !important;
        }

        /* Custom Header Styling - Light Mode */
        .custom-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.5rem;
            border: 2px solid #F59E0B; /* Orange Border */
            border-radius: 12px;
            background-color: #FFFFFF; /* White background */
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .header-title {
            font-size: 2rem;
            font-weight: 800;
            color: #111827; /* Dark Text */
            margin: 0;
            background: linear-gradient(to right, #111827, #D97706);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header-logo {
            height: 45px;
            width: auto;
            object-fit: contain;
        }

        /* -------------------------------------------------------------------------- */
        /* GLOBAL LIGHT THEME OVERRIDES */
        /* -------------------------------------------------------------------------- */
        
        /* App Background - Clean White */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* Text Color - Dark Gray for readability */
        html, body, p, h1, h2, h3, h4, h5, h6, span, div, label, li {
            color: #1F2937 !important;
        }
        
        /* Sidebar - Very Light Gray */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Sidebar Markdown Text */
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown li {
            color: #4B5563 !important; 
        }
        
        /* Input Fields - White w/ Border */
        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #F59E0B !important;
            box-shadow: 0 0 0 1px #F59E0B !important;
        }
        
        /* Selectbox / Dropdown - White Background */
        div[data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB;
        }
        div[data-testid="stSelectbox"] > div > div:hover {
            border-color: #F59E0B;
        }
        
        /* Fix Dropdown Menu Options (The Popover) */
        div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
        }
        
        div[data-baseweb="popover"] ul {
            background-color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] li {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }
        
        div[data-baseweb="popover"] li:hover {
            background-color: #FFF7ED !important; /* Light Orange Hover */
            color: #D97706 !important;
        }
        
        /* Fix Tooltip Content */
        div[data-baseweb="tooltip"] {
            background-color: #111827 !important; /* Dark Background */
            border: 1px solid #374151 !important;
        }
        
        div[data-baseweb="tooltip"] * {
            color: #FFFFFF !important; /* Force ALL internal text to white */
            background-color: transparent !important;
        }
        
        /* Expander - White Background */
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        }
        .streamlit-expanderHeader:hover {
            color: #D97706 !important;
            border-color: #F59E0B;
            background-color: #FFF7ED !important;
        }
        div[data-testid="stExpander"] {
            background-color: #FFFFFF !important;
            border: none;
        }
        div[data-testid="stExpander"] .stMarkdown {
            color: #4B5563 !important;
        }
        
        /* Standard Buttons (Secondary) - White with Orange Border */
        div.stButton > button {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px;
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            background-color: #FFF7ED !important; /* Light Orange */
            color: #D97706 !important; /* Dark Orange Text */
            border-color: #F59E0B !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        
        /* Adjust Top Padding (Moved Down) */
        .block-container {
            padding-top: 3.5rem !important; /* Increased spacing */
            padding-bottom: 5rem !important;
        }

        /* Primary Button Override */
        div.stButton > button[kind="primary"] {
            background-color: #F59E0B !important;
            color: #FFFFFF !important;
            border: 1px solid #D97706 !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #D97706 !important;
            box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.4);
        }

        /* File Uploader - Light Gray */
        div[data-testid="stFileUploader"] {
            border: 1px dashed #F59E0B;
            background-color: #FFF7ED; /* Very light orange tint */
            border-radius: 8px;
        }
        div[data-testid="stFileUploader"] section {
            background-color: #FFF7ED !important;
        }
        div[data-testid="stFileUploader"] span, 
        div[data-testid="stFileUploader"] div,
        div[data-testid="stFileUploader"] small {
            color: #4B5563 !important;
        }
        
        /* Browse Files Button */
        div[data-testid="stFileUploader"] button {
            background-color: #FED7AA !important; /* Light Orange */
            color: #9A3412 !important; /* Darker Orange Text */
            border: 1px solid #F97316 !important;
        }
        div[data-testid="stFileUploader"] button:hover {
            background-color: #FDBA74 !important;
            border-color: #EA580C !important;
        }

        /* Chat Input - White Area */
        .stChatInput textarea {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #F59E0B !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            caret-color: #000000 !important; /* Black Cursor */
        }
        
        .stChatInput textarea::placeholder {
            color: #6B7280 !important; /* Visible Gray Placeholder */
            -webkit-text-fill-color: #6B7280 !important;
            opacity: 1 !important;
        }
        
        div[data-testid="stChatInput"] {
            background-color: transparent !important;
        }
        
        /* Chat Input Container (Bottom Bar) - Force White */
        div[data-testid="stBottom"] {
            background-color: #FFFFFF !important;
            border-top: 1px solid #E5E7EB;
        }
        div[data-testid="stBottom"] > div {
            background-color: #FFFFFF !important;
        }
        
        /* Chat Input Send Button */
        div[data-testid="stChatInput"] button {
            color: #F59E0B !important; /* Orange Icon */
            background-color: transparent !important;
            border: none !important;
            transition: all 0.3s ease !important;
            border-radius: 50% !important;
            height: 2.5rem !important;
            width: 2.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin-right: 0.5rem !important;
        }
        
        div[data-testid="stChatInput"] button:hover {
            color: #FFFFFF !important;
            background-color: #F59E0B !important;
            transform: scale(1.15) !important;
            box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.4) !important;
        }
        
        /* Chat Messages */
        div[data-testid="stChatMessage"] {
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            border: 1px solid transparent;
        }

        /* Assistant Message - White with Shadow */
        div[data-testid="stChatMessage"][data-test-role="assistant"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        /* User Message - Light Orange */
        div[data-testid="stChatMessage"][data-test-role="user"] {
            background-color: #FFF7ED !important; /* Orange-50 */
            border: 1px solid #FED7AA; /* Orange-200 */
        }

    </style>
    """

