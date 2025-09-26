import streamlit as st
from googleapiclient.discovery import build
import random

# ----------------- CONFIG ------------------
API_KEY = 'AIzaSyDcf8lc7pbp-JzNr4DLWcNJO6VRvEZIO3g'  # Replace with your actual API key
SEARCH_ENGINE = 'youtube'

# ----------------- QUIZ QUESTIONS ------------------
quiz_questions = {
    "Data Science": [
        {'question': 'Which library is used for data manipulation in Python?', 'options': ['Matplotlib', 'Numpy', 'Pandas', 'Seaborn'], 'answer': 'Pandas'},
        {'question': 'What does CSV stand for?', 'options': ['Comma Separated Values', 'Column Specific Value', 'Character Separated Values', 'Comma Structured View'], 'answer': 'Comma Separated Values'},
        {'question': 'Which of the following is a supervised learning algorithm?', 'options': ['K-Means', 'Linear Regression', 'PCA', 't-SNE'], 'answer': 'Linear Regression'},
        {'question': 'What is the main goal of exploratory data analysis (EDA)?', 'options': ['Building models', 'Cleaning data', 'Understanding data patterns', 'Deploying apps'], 'answer': 'Understanding data patterns'},
        {'question': 'Which of the following is a classification algorithm?', 'options': ['K-Means', 'Linear Regression', 'Logistic Regression', 'PCA'], 'answer': 'Logistic Regression'},
        {'question': 'What is the primary use of NumPy?', 'options': ['Data visualization', 'Numerical computing', 'Web development', 'Database management'], 'answer': 'Numerical computing'},
        {'question': 'Which metric is used for evaluating classification models?', 'options': ['Mean Squared Error', 'R-squared', 'Accuracy', 'All of the above'], 'answer': 'Accuracy'},
        {'question': 'What does SQL stand for?', 'options': ['Structured Query Language', 'Simple Query Language', 'Standard Query Language', 'System Query Language'], 'answer': 'Structured Query Language'},
        {'question': 'Which of these is not a Python data structure?', 'options': ['List', 'Tuple', 'Array', 'Vector'], 'answer': 'Vector'},
        {'question': 'What is the purpose of a confusion matrix?', 'options': ['To confuse the model', 'To visualize model performance', 'To store model parameters', 'To optimize hyperparameters'], 'answer': 'To visualize model performance'},
        {'question': 'Which library is used for deep learning in Python?', 'options': ['Scikit-learn', 'TensorFlow', 'Pandas', 'Matplotlib'], 'answer': 'TensorFlow'},
        {'question': 'What is feature engineering?', 'options': ['Building features for a house', 'Creating new input features for ML models', 'Designing UI features', 'Engineering features for a car'], 'answer': 'Creating new input features for ML models'},
        {'question': 'What is overfitting?', 'options': ['When a model performs well on training data but poorly on test data', 'When a model fits too tightly', 'When a model is too simple', 'When a model is too large'], 'answer': 'When a model performs well on training data but poorly on test data'},
        {'question': 'What is the purpose of train_test_split?', 'options': ['To divide data into training and testing sets', 'To split a string into parts', 'To separate features and labels', 'To break data into chunks'], 'answer': 'To divide data into training and testing sets'},
        {'question': 'Which of these is a clustering algorithm?', 'options': ['Linear Regression', 'Decision Tree', 'K-Means', 'Support Vector Machine'], 'answer': 'K-Means'},
        {'question': 'What is the purpose of regularization?', 'options': ['To make a model more complex', 'To prevent overfitting', 'To speed up training', 'To improve accuracy'], 'answer': 'To prevent overfitting'},
        {'question': 'Which of these is not a supervised learning task?', 'options': ['Classification', 'Regression', 'Clustering', 'All are supervised'], 'answer': 'Clustering'},
        {'question': 'What is the purpose of cross-validation?', 'options': ['To validate across different datasets', 'To test model performance more robustly', 'To cross-check results', 'To validate user input'], 'answer': 'To test model performance more robustly'},
        {'question': 'What does API stand for?', 'options': ['Application Programming Interface', 'Automated Programming Interface', 'Application Process Integration', 'Automated Process Integration'], 'answer': 'Application Programming Interface'},
        {'question': 'What is the purpose of Git?', 'options': ['Data analysis', 'Version control', 'Web development', 'Machine learning'], 'answer': 'Version control'},
        {'question': 'Which of these is a NoSQL database?', 'options': ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite'], 'answer': 'MongoDB'},
        {'question': 'What is the purpose of Docker?', 'options': ['Data storage', 'Containerization', 'Web hosting', 'Machine learning'], 'answer': 'Containerization'},
        {'question': 'What is the primary use of Jupyter Notebooks?', 'options': ['Web development', 'Interactive computing', 'Database management', 'System administration'], 'answer': 'Interactive computing'},
        {'question': 'Which of these is a Python web framework?', 'options': ['Django', 'TensorFlow', 'Pandas', 'NumPy'], 'answer': 'Django'},
        {'question': 'What is the purpose of pytest?', 'options': ['Data visualization', 'Unit testing', 'Web development', 'Machine learning'], 'answer': 'Unit testing'}
    ],
    "Data Analysis": [
        {'question': 'What function in pandas shows summary statistics?', 'options': ['info()', 'mean()', 'describe()', 'stats()'], 'answer': 'describe()'},
        {'question': 'What does JSON stand for?', 'options': ['JavaScript Object Notation', 'Java Structure Object Notation', 'JavaScript Output Name', 'Java Syntax Object Name'], 'answer': 'JavaScript Object Notation'},
        {'question': 'Which command is used to install Python packages?', 'options': ['pip install', 'python get', 'pkg add', 'lib install'], 'answer': 'pip install'},
        {'question': 'Which one is a Python IDE?', 'options': ['Photoshop', 'VS Code', 'Premiere', 'After Effects'], 'answer': 'VS Code'},
        {'question': 'Which of the following is used for data visualization?', 'options': ['Pandas', 'Seaborn', 'Scikit-learn', 'NLTK'], 'answer': 'Seaborn'},
        {'question': 'What is the purpose of the GROUP BY clause in SQL?', 'options': ['To filter rows', 'To group rows with same values', 'To order results', 'To join tables'], 'answer': 'To group rows with same values'},
        {'question': 'Which function is used to read CSV files in pandas?', 'options': ['read_csv()', 'open_csv()', 'load_csv()', 'import_csv()'], 'answer': 'read_csv()'},
        {'question': 'What is the purpose of the HAVING clause in SQL?', 'options': ['To filter groups', 'To select columns', 'To sort results', 'To join tables'], 'answer': 'To filter groups'},
        {'question': 'Which of these is not a valid pandas data type?', 'options': ['DataFrame', 'Series', 'Array', 'Index'], 'answer': 'Array'},
        {'question': 'What does ETL stand for?', 'options': ['Extract, Transform, Load', 'Enter, Test, Leave', 'Evaluate, Train, Learn', 'Export, Transfer, Locate'], 'answer': 'Extract, Transform, Load'},
        {'question': 'Which method is used to handle missing data in pandas?', 'options': ['dropna()', 'fillna()', 'replace()', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the merge() function in pandas?', 'options': ['To combine DataFrames', 'To merge cells', 'To concatenate strings', 'To blend colors'], 'answer': 'To combine DataFrames'},
        {'question': 'Which of these is a window function in SQL?', 'options': ['SUM()', 'COUNT()', 'ROW_NUMBER()', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the pivot_table() function in pandas?', 'options': ['To rotate DataFrames', 'To create summary tables', 'To change data types', 'To filter rows'], 'answer': 'To create summary tables'},
        {'question': 'Which of these is a common data visualization type?', 'options': ['Bar chart', 'Pie chart', 'Histogram', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the apply() function in pandas?', 'options': ['To apply a function to data', 'To submit a form', 'To request data', 'To install packages'], 'answer': 'To apply a function to data'},
        {'question': 'Which of these is a common data cleaning task?', 'options': ['Handling missing values', 'Removing duplicates', 'Standardizing formats', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the corr() function in pandas?', 'options': ['To correct errors', 'To calculate correlations', 'To count values', 'To create columns'], 'answer': 'To calculate correlations'},
        {'question': 'Which of these is a common SQL join type?', 'options': ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the value_counts() function in pandas?', 'options': ['To count values', 'To calculate values', 'To create values', 'To delete values'], 'answer': 'To count values'},
        {'question': 'Which of these is a common data aggregation function?', 'options': ['sum()', 'mean()', 'count()', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the sort_values() function in pandas?', 'options': ['To sort data', 'To value data', 'To create values', 'To delete values'], 'answer': 'To sort data'},
        {'question': 'Which of these is a common data quality issue?', 'options': ['Missing values', 'Inconsistent formats', 'Duplicate data', 'All of the above'], 'answer': 'All of the above'},
        {'question': 'What is the purpose of the melt() function in pandas?', 'options': ['To transform wide data to long format', 'To melt ice', 'To combine columns', 'To delete data'], 'answer': 'To transform wide data to long format'},
        {'question': 'Which of these is a common statistical measure?', 'options': ['Mean', 'Median', 'Standard deviation', 'All of the above'], 'answer': 'All of the above'}
    ],
    "HTML/Web Development": [
        {'question': 'What does HTML stand for?', 'options': ['Hyper Trainer Marking Language', 'Hyper Text Markup Language', 'Hyper Text Marketing Language', 'None'], 'answer': 'Hyper Text Markup Language'},
        {'question': 'Which language is used for styling web pages?', 'options': ['HTML', 'Python', 'JavaScript', 'CSS'], 'answer': 'CSS'},
        {'question': 'Which tag is used to insert an image in HTML?', 'options': ['<img>', '<pic>', '<src>', '<image>'], 'answer': '<img>'},
        {'question': 'Which attribute specifies an alternate text for an image?', 'options': ['alt', 'src', 'title', 'href'], 'answer': 'alt'},
        {'question': 'Which language is used for client-side scripting?', 'options': ['PHP', 'Python', 'JavaScript', 'SQL'], 'answer': 'JavaScript'},
        {'question': 'What does CSS stand for?', 'options': ['Cascading Style Sheets', 'Computer Style Sheets', 'Creative Style Sheets', 'Colorful Style Sheets'], 'answer': 'Cascading Style Sheets'},
        {'question': 'Which HTML tag is used for the largest heading?', 'options': ['<h6>', '<heading>', '<h1>', '<head>'], 'answer': '<h1>'},
        {'question': 'Which HTML attribute specifies an element\'s unique identifier?', 'options': ['class', 'id', 'name', 'type'], 'answer': 'id'},
        {'question': 'Which HTML tag is used to define a hyperlink?', 'options': ['<link>', '<a>', '<href>', '<hyperlink>'], 'answer': '<a>'},
        {'question': 'Which CSS property is used to change the text color?', 'options': ['text-color', 'font-color', 'color', 'text-style'], 'answer': 'color'},
        {'question': 'Which HTML tag is used to define an unordered list?', 'options': ['<ol>', '<list>', '<ul>', '<dl>'], 'answer': '<ul>'},
        {'question': 'Which HTML tag is used to define a table row?', 'options': ['<td>', '<tr>', '<th>', '<table-row>'], 'answer': '<tr>'},
        {'question': 'Which CSS property is used to change the font?', 'options': ['font-family', 'font-style', 'font-weight', 'All of the above'], 'answer': 'font-family'},
        {'question': 'Which HTML tag is used to define a paragraph?', 'options': ['<para>', '<p>', '<paragraph>', '<pg>'], 'answer': '<p>'},
        {'question': 'Which CSS property is used to add background color?', 'options': ['background-color', 'bgcolor', 'color-background', 'background'], 'answer': 'background-color'},
        {'question': 'Which HTML tag is used to define a line break?', 'options': ['<lb>', '<break>', '<br>', '<newline>'], 'answer': '<br>'},
        {'question': 'Which CSS property is used to control the space between elements?', 'options': ['margin', 'padding', 'spacing', 'Both margin and padding'], 'answer': 'Both margin and padding'},
        {'question': 'Which HTML tag is used to define a form?', 'options': ['<form>', '<input>', '<fieldset>', '<submit>'], 'answer': '<form>'},
        {'question': 'Which CSS property is used to make text bold?', 'options': ['text-weight', 'font-bold', 'font-weight', 'text-style'], 'answer': 'font-weight'},
        {'question': 'Which HTML tag is used to define a drop-down list?', 'options': ['<input>', '<select>', '<dropdown>', '<list>'], 'answer': '<select>'},
        {'question': 'Which CSS property is used to change the text size?', 'options': ['text-size', 'font-size', 'text-style', 'size'], 'answer': 'font-size'},
        {'question': 'Which HTML tag is used to define a button?', 'options': ['<button>', '<input type="button">', '<btn>', 'Both <button> and <input type="button">'], 'answer': 'Both <button> and <input type="button">'},
        {'question': 'Which CSS property is used to add rounded corners?', 'options': ['border-radius', 'corner-radius', 'round-corner', 'border-style'], 'answer': 'border-radius'},
        {'question': 'Which HTML tag is used to define a division or section?', 'options': ['<div>', '<section>', '<span>', '<block>'], 'answer': '<div>'},
        {'question': 'Which CSS property is used to control the element positioning?', 'options': ['position', 'display', 'float', 'All of the above'], 'answer': 'All of the above'}
    ]
}

# ----------------- POST-COURSE ASSESSMENT QUESTIONS ------------------
post_course_quiz_questions = {
    "Data Science": [
        {'question': 'Which metric is best for imbalanced classification problems?', 
         'options': ['Accuracy', 'F1-Score', 'R2-Score', 'MAE'], 
         'answer': 'F1-Score',
         'explanation': 'F1-Score considers both precision and recall, making it better for imbalanced datasets.'},
        
        {'question': 'What does ROC AUC score represent?',
         'options': ['Model calibration', 'True positive rate vs false positive rate', 
                    'Feature importance', 'Clustering quality'],
         'answer': 'True positive rate vs false positive rate',
         'explanation': 'ROC AUC measures how well the model distinguishes between classes.'},
        
        {'question': 'Which technique helps prevent overfitting in neural networks?',
         'options': ['Increasing learning rate', 'Adding more layers', 
                    'Using dropout', 'Reducing training data'],
         'answer': 'Using dropout',
         'explanation': 'Dropout randomly deactivates neurons during training to prevent co-adaptation.'},
        
        {'question': 'What is the purpose of word embeddings in NLP?',
         'options': ['Compress text files', 'Represent words as dense vectors', 
                    'Count word frequencies', 'Correct spelling errors'],
         'answer': 'Represent words as dense vectors',
         'explanation': 'Embeddings capture semantic meaning in continuous vector space.'},
        
        {'question': 'Which algorithm would you use for anomaly detection?',
         'options': ['Linear Regression', 'K-Means', 
                    'Isolation Forest', 'Random Forest'],
         'answer': 'Isolation Forest',
         'explanation': 'Isolation Forest is specifically designed for anomaly detection.'}
    ],
    "Data Analysis": [
        {'question': 'Which SQL clause is used for filtering groups?',
         'options': ['WHERE', 'HAVING', 'GROUP BY', 'LIMIT'],
         'answer': 'HAVING',
         'explanation': 'HAVING filters groups after aggregation, while WHERE filters rows before grouping.'},
        
        {'question': 'What is the purpose of a window function?',
         'options': ['Perform calculations across rows', 'Create new tables', 
                    'Modify database schema', 'Handle missing values'],
         'answer': 'Perform calculations across rows',
         'explanation': 'Window functions perform calculations across sets of rows related to the current row.'},
        
        {'question': 'Which pandas method is most efficient for large datasets?',
         'options': ['iterrows()', 'apply()', 'vectorized operations', 'for loops'],
         'answer': 'vectorized operations',
         'explanation': 'Vectorized operations leverage NumPy\'s optimized C-based implementations.'},
        
        {'question': 'What does the ETL process stand for?',
         'options': ['Extract, Transform, Load', 'Enter, Test, Leave', 
                    'Evaluate, Train, Learn', 'Export, Transfer, Locate'],
         'answer': 'Extract, Transform, Load',
         'explanation': 'ETL is the process of extracting data from sources, transforming it, and loading into a destination.'},
        
        {'question': 'Which visualization is best for showing distributions?',
         'options': ['Pie chart', 'Bar chart', 'Histogram', 'Line graph'],
         'answer': 'Histogram',
         'explanation': 'Histograms display the distribution of continuous data through bins.'}
    ],
    "HTML/Web Development": [
        {'question': 'What does CSS Grid layout primarily solve?',
         'options': ['Color schemes', 'Complex 2D layouts', 'Browser compatibility', 
                    'Animation timing'],
         'answer': 'Complex 2D layouts',
         'explanation': 'CSS Grid excels at creating complex responsive layouts with rows and columns.'},
        
        {'question': 'What is semantic HTML?',
         'options': ['Using meaningful tags', 'Adding comments', 
                    'Minifying code', 'Using CSS variables'],
         'answer': 'Using meaningful tags',
         'explanation': 'Semantic HTML uses tags that convey meaning about the content (like <article>, <nav>).'},
        
        {'question': 'Which method is most secure for storing user passwords?',
         'options': ['Plain text', 'Hashing with salt', 'Basic encoding', 'Encryption'],
         'answer': 'Hashing with salt',
         'explanation': 'Hashing with salt provides one-way protection against rainbow table attacks.'},
        
        {'question': 'What is the virtual DOM in React?',
         'options': ['A lightweight copy of the real DOM', 'A 3D rendering engine', 
                    'A browser plugin', 'A testing framework'],
         'answer': 'A lightweight copy of the real DOM',
         'explanation': 'The virtual DOM allows React to efficiently update only what changed in the real DOM.'},
        
        {'question': 'What does CORS stand for?',
         'options': ['Cross-Origin Resource Sharing', 'Centralized Object Request System', 
                    'Cascading Order Resolution Style', 'Compressed Object Response Standard'],
         'answer': 'Cross-Origin Resource Sharing',
         'explanation': 'CORS is a security mechanism for cross-domain requests in web applications.'}
    ]
}

# ----------------- FUNCTION TO FETCH COURSES ------------------
def fetch_courses(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=3
    )
    response = request.execute()
    
    courses = []
    for item in response['items']:
        title = item['snippet']['title']
        url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        thumbnail = item['snippet']['thumbnails']['high']['url']
        courses.append((title, url, thumbnail))
    return courses

# ----------------- STREAMLIT UI ------------------
st.set_page_config(page_title="Skill Mastery Platform", layout="wide")
st.title("🎯 Multi-Skill Learning Platform")

# Initialize session state variables
if 'initial_score' not in st.session_state:
    st.session_state.initial_score = 0
if 'show_course_recs' not in st.session_state:
    st.session_state.show_course_recs = False
if 'show_final_assessment' not in st.session_state:
    st.session_state.show_final_assessment = False
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'final_answers' not in st.session_state:
    st.session_state.final_answers = {}
if 'track' not in st.session_state:
    st.session_state.track = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'final_questions' not in st.session_state:
    st.session_state.final_questions = []
if "pages" not in st.session_state:
    st.session_state.pages = 0
from PIL import Image
image="skill.jpg"  #add image name
def homepage():
    st.subheader("Welcome to Course Recommender")
    st.write("")
    st.write("")
    col1,col2=st.columns(2)
    with col1:
        st.info("We Reffer a Course On Your **knowledge** Capability")
        col1,col3=st.columns(2)
        with col3:
            if st.button("Get Started"):
                st.session_state["pages"]=1
                st.rerun()
            
    with col2:
        img=Image.open(image)
        st.image(img)
# ----------------- USER PROFILE SECTION ------------------
def login():
    with st.form("Login"):
        with st.expander("👤 User Profile", expanded=True):
            st.header("Enter Your Details")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
                education = st.selectbox("Highest Education", 
                                    ["High School", "Bachelor's", "Master's", "PhD"])
            with col2:
                field = st.text_input("Field of Study")
                goals = st.text_area("Career Goals")
            col1, col2 = st.columns(2)
            with col2:
                if st.form_submit_button("Login"):
                    if not name  or not education  or not field :
                        st.toast("Fill Up the Cells")
                    else:
                        st.session_state["pages"]=2
                        st.rerun()
                    
# ----------------- INITIAL ASSESSMENT SECTION ------------------
def intial():
        with st.expander("📝 Initial Assessment", expanded=not st.session_state.show_course_recs):
            st.header("Choose Area of Interest")
            track = st.selectbox("Select a track", list(quiz_questions.keys()), key='track_select')
            
            # Initialize or update questions if track changes
            if st.session_state.track != track:
                st.session_state.track = track
                # Select 15 random questions from the pool of 20-25 questions
                st.session_state.questions = random.sample(quiz_questions[track], k=15)
                st.session_state.answers = {i: None for i in range(len(st.session_state.questions))}
            
            st.header("Step 3: Take Initial Assessment (15 Questions)")
            
            with st.form("quiz_form"):
                user_answers = {}
                for i, q in enumerate(st.session_state.questions):
                    # Get index of previously selected answer if exists
                    selected_index = None
                    if i in st.session_state.answers and st.session_state.answers[i] in q['options']:
                        selected_index = q['options'].index(st.session_state.answers[i])
                    
                    answer = st.radio(
                        q['question'],
                        q['options'],
                        key=f"q_{i}",
                        index=selected_index
                    )
                    user_answers[i] = answer
                submitted = st.form_submit_button("Submit Assessment")

            if submitted:
                # Store answers in session state
                if len(user_answers) == 15 :
                    
                    st.session_state.answers = user_answers
                    
                    
                    # Calculate initial score
                    score = 0
                    for i, q in enumerate(st.session_state.questions):
                        if user_answers[i] == q['answer']:
                            score += 1
                    
                    # Store in session state
                    st.session_state.initial_score = score
                    st.session_state.show_course_recs = True
                    
                    # Display results
                    st.success(f"You scored {score} out of {len(st.session_state.questions)}")
                    if score <= 5:
                        level = "Beginner"
                    elif score <= 10:
                        level = "Intermediate"
                    else:
                        level = "Advanced"
                    
                    st.info(f"Recommended Level: {level}")
                    st.session_state.recommended_level = level
                    
                    if st.button("Recommend Courses"):
                        st.session_state["pages"]=3
                        st.rerun()
                else:
                    st.toast(f"You forgot Answering{len(user_answers) - 15}")

# ----------------- COURSE RECOMMENDATION SECTION ------------------
def recommendation():
    if st.session_state.show_course_recs and not st.session_state.show_final_assessment:
        st.header("📚 Recommended Learning Path")
        
        # Display level-specific courses
        st.subheader(f"{st.session_state.recommended_level} {st.session_state.track} Courses")
        course_query = f"{st.session_state.recommended_level} {st.session_state.track} course 2024"
        courses = fetch_courses(course_query)
        
        cols = st.columns(3)
        for i, (title, url, thumbnail) in enumerate(courses):
            with cols[i]:
                st.image(thumbnail, use_container_width=True)
                st.markdown(f"[{title}]({url})")
                st.caption(f"Recommended {st.session_state.recommended_level} content")
        
        # Add practice resources section
        st.subheader("🧠 Practice Resources")
        practice_query = f"{st.session_state.track} practice exercises {st.session_state.recommended_level}"
        practice_resources = fetch_courses(practice_query)
        
        for title, url, _ in practice_resources[:2]:
            st.markdown(f"- [{title}]({url})")
        
        # Add final assessment trigger
        st.divider()
        if st.button("🚀 Take Final Assessment After Completion", 
                    help="Complete this after finishing recommended courses"):
            st.session_state.show_final_assessment = True
            st.session_state["pages"]= 4
            st.rerun()

# ----------------- FINAL ASSESSMENT SECTION ------------------
def final():
    if st.session_state.show_final_assessment:
        st.header("📝 Final Knowledge Assessment")
        st.write("""
        This advanced test will:
        - Validate your learning progress
        - Identify remaining knowledge gaps
        - Suggest next steps
        """)
        
        # Select questions - include some from initial test for comparison
        if not st.session_state.final_questions:
            initial_questions = random.sample(quiz_questions[st.session_state.track], k=2)
            advanced_questions = random.sample(post_course_quiz_questions[st.session_state.track], k=3)
            st.session_state.final_questions = initial_questions + advanced_questions
            st.session_state.final_answers = {i: None for i in range(len(st.session_state.final_questions))}
        
        # Assessment form
        with st.form("final_assessment"):
            st.subheader("Core Concepts")
            for i, q in enumerate(st.session_state.final_questions[:2]):
                selected_index = None
                if i in st.session_state.final_answers and st.session_state.final_answers[i] in q['options']:
                    selected_index = q['options'].index(st.session_state.final_answers[i])
                
                answer = st.radio(
                    q['question'],
                    q['options'],
                    key=f"core_q_{i}",
                    index=selected_index
                )
                st.session_state.final_answers[i] = answer
            
            st.subheader("Advanced Application")
            for i, q in enumerate(st.session_state.final_questions[2:], start=2):
                selected_index = None
                if i in st.session_state.final_answers and st.session_state.final_answers[i] in q['options']:
                    selected_index = q['options'].index(st.session_state.final_answers[i])
                
                answer = st.radio(
                    q['question'],
                    q['options'],
                    key=f"adv_q_{i}",
                    index=selected_index
                )
                st.session_state.final_answers[i] = answer
            
            submitted_final = st.form_submit_button("Submit Assessment")

        # Results processing
        if submitted_final:
            # Calculate scores
            initial_correct = 0
            advanced_correct = 0
            
            for i, q in enumerate(st.session_state.final_questions[:2]):
                if st.session_state.final_answers[i] == q['answer']:
                    initial_correct += 1
                    
            for i, q in enumerate(st.session_state.final_questions[2:], start=2):
                if st.session_state.final_answers[i] == q['answer']:
                    advanced_correct += 1
                    
            total_score = initial_correct + advanced_correct
            
            # Calculate improvement from initial assessment
            initial_ratio = st.session_state.initial_score / len(st.session_state.questions)
            improvement = initial_correct - (initial_ratio * 2)
            
            # Display comprehensive results
            st.header("📊 Your Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Core Concepts", 
                        f"{initial_correct}/2", 
                        f"{improvement:+.1f} from initial")
            with col2:
                st.metric("Advanced Concepts", 
                        f"{advanced_correct}/3")
            
            # Progress visualization
            progress = total_score / len(st.session_state.final_questions)
            st.progress(progress)
            st.caption(f"Overall mastery: {progress:.0%}")
            
            # Detailed feedback
            st.subheader("🔍 Feedback")
            if advanced_correct >= 2:
                st.success("*Excellent progress!* You're ready for more advanced topics.")
                next_steps = fetch_courses(f"Advanced {st.session_state.track} specialization")
                st.subheader("🚀 Next Steps")
                for title, url, _ in next_steps[:2]:
                    st.markdown(f"- [{title}]({url})")
            else:
                st.info("*Good foundation!* Focus on practicing these areas:")
                for i, q in enumerate(st.session_state.final_questions[2:]):
                    if st.session_state.final_answers[i+2] != q['answer']:
                        st.markdown(f"- *{q['question']}*: {q['explanation']}")
                
                st.subheader("🔄 Recommended Review")
                review_materials = fetch_courses(f"{st.session_state.track} concepts tutorial")
                for title, url, _ in review_materials[:2]:
                    st.markdown(f"- [{title}]({url})")
            
            # Reset states
            st.session_state.show_final_assessment = False
            st.balloons()

if st.session_state["pages"] == 0:
    homepage()
if st.session_state["pages"] == 1:
    login()
elif st.session_state["pages"] == 2:
    intial()
elif st.session_state["pages"] == 3:
    recommendation()
elif st.session_state["pages"] == 4:
    final()