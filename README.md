# ✈️ AI Smart Travel Planner

An intelligent, full-stack travel planning and booking assistant powered by **FastAPI**, **Streamlit**, and **LangGraph**. This application uses Generative AI (Google Gemini) to act as a conversational agent that guides users through trip planning, extracts requirements, validates locations, verifies users via email OTP, processes payments using Razorpay, and dispatches HTML E-Tickets.

---

## 🏗️ System Architecture & Working Flow

The system is divided into a robust FastAPI backend and an interactive Streamlit frontend. Here is the end-to-end user journey:

### 1. Conversational Extraction (Powered by LangGraph)
* The user interacts with the AI Assistant on the Streamlit chat interface.
* The chat messages are sent to the FastAPI backend where **LangGraph** orchestrates the state machine.
* The AI dynamically extracts required fields (`source`, `destination`, `journey_date`, `travel_mode`, `budget`).
* **Guardrails:** A custom City Gazetteer automatically corrects spelling mistakes (e.g., "Banglore" $\rightarrow$ "Bangalore") and rejects gibberish inputs.

### 2. Provider Search & Recommendation
* Once all travel details are collected, the graph transitions to the `ProviderNode`.
* It fetches real/mock travel data (Flights, Trains, Buses) based on the user's criteria.
* The Gemini LLM analyzes the options and provides a personalized recommendation.

### 3. Strict User Verification (OTP Lock)
* The user selects a travel option and proceeds to book.
* The Streamlit UI prompts for Name, Email, and Phone number.
* The backend generates a 6-digit OTP and sends it via SMTP Email.
* **Security Lock:** The PostgreSQL database explicitly rejects the creation of a booking record unless the email session has been successfully verified via OTP.

### 4. Secure Payment (Razorpay & Demo Mode)
* Once verified, the booking is recorded in PostgreSQL as `PENDING`.
* The user is redirected to a custom HTML checkout page powered by the Razorpay gateway.
* **Demo Mode:** For live presentations, a "Skip Payment" bypass is available, which securely forces the transaction state to `CONFIRMED` without requiring actual card details.

### 5. Confirmation & E-Ticket Dispatch
* Upon successful payment (or Demo bypass), the backend verifies the Razorpay signature.
* The system automatically generates a responsive HTML E-Ticket and emails it to the verified user.
* The Streamlit UI transitions to the Success screen and updates the user's Booking History.

---

## 🧠 Where is LangGraph Used?

**LangGraph** is the core orchestrator of the conversational agent, located in the `app/graph/` directory. 

Unlike standard linear chatbots, LangGraph treats the conversation as a cyclical **State Machine** (`TravelState`). 
* **State Tracking:** It tracks missing fields in real-time across turns.
* **Nodes:** It routes traffic through specialized nodes (`TravelNode` for extraction and Gazetteer validation, `ProviderNode` for fetching APIs, and `AiNode` for generating natural responses).
* **Conditional Edges:** It uses conditional routing to loop back to the user if locations are invalid or missing, and only advances to the recommendation phase when the exact schema requirements are met.
* **Memory:** It utilizes a `RedisCheckpointer` to persist conversational memory so the user can pause and resume their planning seamlessly.

---

## 🚀 Step-by-Step Setup & Installation Guide

Follow these instructions to clone, setup, and run the project on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:
* **Python 3.10+**
* **PostgreSQL** (Running on default port 5432/5433)
* **Redis Server** (Running on default port 6379)
* **Git**

### Step 1: Clone the Repository
```bash
git clone [https://github.com/Chetan973/AI-Smart-Travel-Planner.git](https://github.com/Chetan973/AI-Smart-Travel-Planner/.git)
cd AI-Smart-Travel-Planner

Step 2: Create a Virtual Environment
It is highly recommended to isolate your dependencies using a virtual environment.
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

Step 3: Install Dependencies
    Install the required Python packages for both the backend and the Streamlit frontend.

Bash
    # Install backend requirements
    pip install -r requirements.txt

    # Install frontend requirements
    pip install -r streamlit-ui/requirements.txt
    Step 4: Configure Environment Variables
    Create a .env file in the root directory (AI-Smart-Travel-Planner/.env) and add your specific credentials:

    Code snippet
    # Application
    APP_NAME="AI Smart Travel Planner"
    ENVIRONMENT=development

    # PostgreSQL Database (Update with your username/password/port)
    DATABASE_URL=postgresql+psycopg://postgres:YourPassword@localhost:5432/travel_planner_db

    # Redis Memory
    REDIS_URL=redis://localhost:6379/0

    # Google Gemini API
    GOOGLE_API_KEY=your_gemini_api_key_here

    # SMTP Configuration (For OTP and E-Tickets)
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_google_app_password

    # Razorpay Sandbox Credentials
    RAZORPAY_KEY_ID=rzp_test_your_key_here
    RAZORPAY_KEY_SECRET=your_razorpay_secret_here

    # Demo Presentation Mode (Set True to enable the Skip Payment button)
    DEMO_MODE_ENABLED=True
    Step 5: Initialize the Database
    Run the database initialization script to create the required tables (users, bookings, payments, email_otps) in PostgreSQL.

    Bash
    python -m app.database.init_db
    Step 6: Run the Application
    You will need two separate terminal windows/tabs to run the backend and frontend simultaneously.

    Terminal 1: Start the FastAPI Backend

    Bash
    # Ensure your virtual environment is active
    uvicorn app.main:app --reload
    The backend will be available at http://127.0.0.1:8000. You can view the API documentation at http://127.0.0.1:8000/docs.

Terminal 2: Start the Streamlit Frontend

Bash
# Ensure your virtual environment is active
    cd streamlit-ui
    streamlit run streamlit_app.py
