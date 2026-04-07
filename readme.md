# Writing Advisor

## 1. Problem: improving one’s writing

Good writing is hard. Many people:

- Struggle to **identify weaknesses** in their own text (clarity, structure, tone).
- Don’t have instant access to a **teacher, editor, or writing coach**.
- Want **quick, concrete suggestions** instead of vague advice like “be clearer” or “write more concisely”.

Without feedback, it’s easy to repeat the same mistakes—overly long sentences, unclear word choices, weak structure—and never see how to improve.

## 2. How this application helps

This application provides a simple way to get **immediate, targeted feedback** on your writing:

- You paste a paragraph or short text into the web interface.
- The app sends your text to a **writing-advice API** (or a local analysis function).
- It returns **specific suggestions** on how to improve clarity, structure, and style.
- Each analysis is **stored in a database**, so you can review your progress over time.

In other words, it turns your browser into a lightweight writing coach: quick, repeatable, and always available.

## 3. How it works (architecture)

The app is built with **Python**, **Flask**, and **SQLite**:

- **User interface (UI)**  
  - Implemented with HTML templates (`templates/` folder).  
  - `index.html` provides a text area where you paste your writing and a button to request advice.  
  - `history.html` shows previous analyses stored in the database.

- **Application logic**  
  - `app.py` defines the Flask application.  
  - The `/` route:
    - Handles `GET` requests to show the form.
    - Handles `POST` requests when you submit text.
    - Calls a function that contacts the writing-advice API (or a mock function) and returns suggestions.
    - Saves the original text and the advice to the database.
  - The `/history` route:
    - Queries the database for past analyses.
    - Renders them in a simple list.

- **Database**  
  - `models.py` defines a `WritingSample` model with:
    - `text`: the original user text.
    - `advice`: the feedback returned by the API.
    - `created_at`: timestamp of the analysis.
  - Uses **SQLite** via `Flask_SQLAlchemy`.  
  - The database file (`writing.db`) is created automatically in the `instance/` folder.

- **API integration**  
  - The function `get_writing_advice(text)` in `app.py` is responsible for calling an external API.  
  - In this sample, it’s mocked with simple rules, but you can:
    - Add a real endpoint URL.
    - Use an API key stored in an environment variable.
    - Parse the JSON response and return the advice string.