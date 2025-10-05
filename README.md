SpendMood
By Bilash Sarkar, Yuki Li, and Chloe Velez
SpendMood is a full-stack web application that tracks your spending habits and analyzes the emotional patterns behind your purchases. Using AI-powered insights from Google Gemini, SpendMood helps users understand not just what they spend on, but why—connecting financial decisions to mood, time of day, and personal triggers.
This project combines modern web technologies with artificial intelligence to create a personalized financial wellness companion that goes beyond traditional expense trackers.
The goal of SpendMood is to deliver:

An intuitive React-based interface for logging and visualizing expenses
AI-driven insights that connect spending patterns to emotional states
Secure user authentication and personalized data management
Real-time transaction syncing with banking APIs
Interactive mood tracking alongside financial data


Technologies Used
Frontend:

React (with Vite for fast development and build)
HTML5, CSS3, JavaScript (ES6+)
Responsive design with custom styling
JSON for data exchange

Backend:

Python with FastAPI (modern, high-performance API framework)
RESTful API architecture
Authentication using auth() middleware
Integration with Google Gemini AI for intelligent spending analysis

External APIs:

Nessie API for banking/transaction data
Google Gemini API for AI-powered mood and spending insights

Tools:

Visual Studio Code
GitHub for version control
Postman for API testing
npm/Node.js for package management


Setup & Installation
Prerequisites

Python 3.8+ installed
Node.js and npm installed
API keys for Gemini and Nessie

Backend Setup

Clone the repository:

bash   git clone https://github.com/bsarkr/SpendMood.git
   cd SpendMood

Set up Python virtual environment:

bash   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Python dependencies:

bash   pip install fastapi uvicorn python-multipart

Configure environment variables:

Create a .env file in the root directory
Add your API keys:



     GEMINI_API_KEY=your_gemini_key_here
     NESSIE_API_KEY=your_nessie_key_here
     SECRET_KEY=your_secret_key_for_auth

Start the FastAPI server:

bash   uvicorn main:app --reload

Backend runs on http://localhost:8000

Frontend Setup

Navigate to the frontend directory:

bash   cd frontend

Install dependencies:

bash   npm install

Start the development server:

bash   npm run dev

Frontend runs on http://localhost:5173


How to Use
Sign Up / Log In:

Create an account or log in using the secure auth() system
All data is user-specific and protected

Log Expenses:

Manually add transactions with amount, category, and notes
Sync automatically with Nessie API for real-time banking data

Track Your Mood:

Tag each expense with your emotional state (happy, stressed, impulsive, etc.)
Add context notes to remember what influenced the purchase

View Insights:

Dashboard displays spending by category, time, and mood
Gemini AI analyzes patterns and provides personalized recommendations
Interactive charts show correlations between emotions and spending

Get AI Recommendations:

Ask Gemini questions like "Why do I spend more when stressed?" or "What's my biggest impulse category?"
Receive actionable tips for better financial wellness


Key Learnings & Challenges
Building SpendMood was an exercise in integrating cutting-edge AI with practical financial tools. The biggest challenge was designing a seamless flow between user input, AI analysis, and real-time API data while keeping the interface clean and intuitive.
Technical Challenges:

FastAPI + React integration: Setting up CORS properly and managing state between frontend and backend
Gemini AI prompts: Crafting effective prompts to get meaningful, personalized insights rather than generic advice
Nessie API data parsing: Handling different transaction formats and mapping them to our custom schema
Auth security: Implementing JWT tokens and protecting routes with auth() middleware

What I Learned:

How to build a modern async API with FastAPI
Integrating AI APIs effectively for real-world applications
Managing React state with Vite's fast refresh
Secure authentication flows in a full-stack app
The importance of UX when dealing with sensitive financial data


Roadmap & Future Features
Planned enhancements for future versions:
Advanced AI Features:

Predictive spending alerts based on past mood patterns
Weekly AI-generated financial wellness reports
Voice-to-text expense logging with sentiment analysis

Social & Gamification:

Anonymous mood-spending comparisons with other users
Achievement badges for meeting savings goals
Accountability partners/groups for financial goals

Enhanced Data:

Multi-account support (checking, savings, credit cards)
Budget creation with smart category limits
Export spending reports as PDF/CSV
Calendar view with mood + spending timeline

Mobile Experience:

Progressive Web App (PWA) support
Mobile-optimized React interface
Push notifications for spending alerts
