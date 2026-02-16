def get_custom_css():
    """Returns custom CSS for the Streamlit application."""
    
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global Styles */
        html, body, [class*="st-"] {
            font_family: 'Inter', sans-serif;
            color: #1F2937;
        }
        
        /* App Background */
        .stApp {
            background-color: #F3F4F6;
        }

        /* Streamlit Header - Transparent but functional (for Sidebar Toggle) */
        header[data-testid="stHeader"] {
            background: transparent;
        }
        footer {
            display: none;
        }

        /* Navbar Styling */
        .navbar {
            background-color: #FFFFFF;
            padding: 1rem 2rem;
            border-bottom: 1px solid #E5E7EB;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            /* Sticky positioning */
            position: sticky; /* Fixed invalid 'upper' */
            top: 0;
            z-index: 100;
        }

        /* [Skipping unchanged blocks...] */

        /* Streamlit Element Overrides */
        .stChatMessage {
            background-color: transparent;
            border: none;
        }
        
        div[data-testid="stChatMessage"] {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        div[data-testid="stChatMessage"][data-test-role="assistant"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        div[data-testid="stChatMessage"][data-test-role="user"] {
            background-color: #F3F4F6;
        }
        
        /* Input Field Styling */
        .stChatInput textarea {
            border-radius: 0.5rem;
            border: 1px solid #E5E7EB;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            background-color: #FFFFFF;
            color: #111827;
        }
        .stChatInput textarea:focus {
            border-color: #F59E0B;
            box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2);
        }
        
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: #111827;
        }
        
        .navbar-icon {
            background-color: #F59E0B;
            color: white;
            padding: 0.5rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .user-profile {
            background-color: #EEF2FF;
            color: #4F46E5;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.875rem;
            border: 1px solid #C7D2FE;
        }
        
        .navbar-logo-img {
             height: 48px;
             width: auto;
             max-width: 200px;
             object-fit: contain;
        }

        /* Metric Card Styling */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
            height: 100%;
        }
        
        .metric-title {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #9CA3AF;
            margin-bottom: 0.25rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #111827;
        }
        
        .metric-status {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
        }
        
        .status-active {
            background-color: #ECFDF5;
            color: #10B981;
        }
        
        .status-waiting {
            background-color: #FFFBEB;
            color: #F59E0B;
        }

        /* Chat Interface Styles */
        .chat-header {
            background-color: white;
            padding: 1rem;
            border-top-left-radius: 0.75rem;
            border-top-right-radius: 0.75rem;
            border-bottom: 1px solid #E5E7EB;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .chat-title {
            font-weight: 700;
            color: #1F2937;
        }

        /* Streamlit Element Overrides */
        .stChatMessage {
            background-color: transparent;
            border: none;
        }
        
        div[data-testid="stChatMessage"] {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        div[data-testid="stChatMessage"][data-test-role="assistant"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        div[data-testid="stChatMessage"][data-test-role="user"] {
            background-color: #F3F4F6;
        }
        
        /* Input Field Styling */
        /* Input Field Styling */
        /* Input Field Styling */
        /* Input Field Styling */
        .stChatInput textarea {
            border-radius: 0.5rem;
            border: 1px solid #F59E0B !important; /* Forced Orange Border */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            background-color: #FFFFFF !important;
            color: #111827 !important;
            caret-color: #111827 !important; /* Fixed: Cursor color */
        }
        .stChatInput textarea:focus {
            border-color: #F59E0B !important;
            box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2) !important;
        }
        
        /* Ensure Container is not Gray */
        div[data-testid="stChatInput"] {
            background-color: transparent !important;
        }
        
        /* Toolbar (Three Dots) Styling */
        [data-testid="stToolbar"] {
            right: 2rem;
            top: 1rem;
        }
        [data-testid="stToolbar"] button {
            color: #F59E0B !important; /* Orange Icons */
            border: none !important;
        }
        [data-testid="stToolbar"] button:hover {
            color: #D97706 !important;
            background-color: #FFFBEB !important;
        }

        /* Bottom Container - make it White */
        div[data-testid="stBottom"] {
            background-color: #FFFFFF !important;
            border-top: 1px solid #E5E7EB;
        }
        div[data-testid="stBottom"] > div {
            background-color: #FFFFFF !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #F3F4F6;
        }
        
        /* Sidebar Navigation/Elements */
        section[data-testid="stSidebar"] .stMarkdown {
            color: #111827;
        }
        
        /* Button Styling */
        div.stButton > button {
            background-color: #FFFFFF;
            color: #111827;
            border: 1px solid #E5E7EB;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            border-color: #F59E0B;
            color: #F59E0B;
            background-color: #FFFBEB;
        }
        div.stButton > button:active {
            box-shadow: none;
            transform: translateY(1px);
        }

        /* Primary Button Override */
        div.stButton > button[kind="primary"] {
            background-color: #F59E0B;
            color: white;
            border: 1px solid #F59E0B;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #D97706;
            border-color: #D97706;
            color: white;
        }

        /* File Uploader - White */
        div[data-testid="stFileUploader"] {
            background-color: #FFFFFF;
            border: 1px dashed #F59E0B;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        div[data-testid="stFileUploader"] section {
            background-color: #FFFFFF;
        }
        
        /* Input Fields - White */
        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            color: #111827;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #F59E0B;
            box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2);
        }

        /* Expander Header - White */
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            color: #111827 !important;
        }
        
        /* File Uploader Button */
        div[data-testid="stFileUploader"] button {
            background-color: #FFF7ED;
            color: #C2410C;
            border: 1px solid #FDBA74;
        }
        div[data-testid="stFileUploader"] button:hover {
            background-color: #FFEDD5;
            border-color: #F97316;
            color: #9A3412;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #F3F4F6; 
        }
        ::-webkit-scrollbar-thumb {
            background: #D1D5DB; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9CA3AF; 
        }

        /* -------------------------------------------------------------------------- */
        /* Pop Up Menu & Dropdown Styling (Fixing the Gray Issue) */
        /* -------------------------------------------------------------------------- */
        
        /* Base Web Popover (Used for Main Menu, Selectbox, st.popover) */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        div[role="dialog"] {
            background-color: #FFFFFF !important;
            border-radius: 0.75rem !important; /* Slightly more rounded */
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important; /* Stronger shadow for depth */
            border: 1px solid #F3F4F6 !important;
        }
        
        /* Ensure the arrow/tip is also white */
        div[data-baseweb="popover"] > div {
             background-color: #FFFFFF !important;
        }

        /* List Items inside Popovers */
        li, [data-baseweb="menu"] li {
             background-color: #FFFFFF !important;
        }
        
        /* Hover State for Menu Items */
        li:hover, [data-baseweb="menu"] li:hover {
             background-color: #FFF7ED !important; /* Light Orange Tint on Hover */
             color: #C2410C !important;
        }


    </style>
    """
