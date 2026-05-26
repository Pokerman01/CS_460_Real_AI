# CS460 AI Smart Tax (prototype)

AI Smart Tax is a Streamlit web application that helps users organize receipts, extract expense details, verify tax-related information, and view tax analytics.

## Features

- Receipt upload for images and PDFs
- AI-style receipt analysis demo
- Manual verification and correction form
- SQLite database storage
- Receipt history with search and category filters
- Tax analytics dashboard with expense, VAT, and deductible summaries
- Dark themed landing page and dashboard

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## How to Run

1. Clone this repository.

``` 
  git clone <your-repository-url>
  cd CS_460_Real_AI 
```

2. Install the required packages.

```
  pip install streamlit pandas plotly
```

3. Run the application.

```
  streamlit run app.py
```

or try if it not working properly 

```
  python -m streamlit run app.py      
```
this command runs Streamlit through the active Python interpreter. When your system cannot find the standalone.
    

** Before running the command, make sure your terminal is in the correct project folder where app.py is located. If you run the command from the wrong path, Streamlit may not find app.py.



4. Project Structure

CS_460_Real_AI/
├── app.py          # Main router for landing page and dashboard
├── landing.py      # Landing page UI
├── dashboard.py    # Receipt scanner, verification, history, and analytics
├── database.py     # SQLite database functions
└── README.md


** Notes
This project is a course prototype for smart receipt and tax organization. The current receipt analysis uses mock extracted data for demonstration purposes.

If you want to use real receipt analysis, you can connect the app to your own AI/OCR API.
