# CSV User Upload API

## 📌 Project Overview

This project provides a Django REST Framework (DRF) API endpoint that allows users to upload a CSV file containing user data.  

The API validates the data, stores valid records in the database, and returns a structured JSON response summarizing the results.

---

## 🚀 Features

- Upload CSV file via POST API
- Validates:
  - `name` → must be non-empty string
  - `email` → must be valid email format
  - `age` → integer between 0 and 120
- Skips duplicate email addresses gracefully
- Bulk inserts valid records for performance
- Returns detailed validation errors
- Includes unit tests
- Handles large CSV files efficiently

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite (default database)

---

## 📂 Project Structure

```

csv_user_api/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│
├── manage.py
├── requirements.txt
├── README.md
├── sample_input.csv
├── large_sample_input.csv
└── .gitignore

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd csv_user_api
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Start Development Server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## 📡 API Endpoint

### Upload CSV

```
POST /api/upload/
```
<img width="1858" height="964" alt="Screenshot 2026-03-05 004832" src="https://github.com/user-attachments/assets/6c610564-f1ed-45c0-8221-450175652adc" />


### Request Type

`multipart/form-data`

### Form Field

| Key  | Type | Required |
| ---- | ---- | -------- |
| file | File | Yes      |

---

## 📥 Sample Input CSV Format

```
name,email,age
Rahul,rahul@example.com,25
Anu,anu@example.com,30
```
<img width="1848" height="964" alt="Screenshot 2026-03-05 004856" src="https://github.com/user-attachments/assets/4fd11e9e-0350-4aa3-90f1-a8d313ea4f56" />

---

## 📤 Sample Response

```json
{
  "total_saved": 2,
  "total_rejected": 1,
  "errors": [
    {
      "row": 3,
      "error": {
        "age": ["Age must be between 0 and 120."]
      }
    }
  ]
}
```
<img width="1158" height="904" alt="Screenshot 2026-03-05 005908" src="https://github.com/user-attachments/assets/f47704ca-b51a-4da0-8e2a-6d9f33432afe" />


---

## 🧪 Running Unit Tests

```bash
python manage.py test
```
<img width="757" height="237" alt="unit_test_execution png" src="https://github.com/user-attachments/assets/13c7b74e-575a-4de9-b29d-f5209ba89a00" />


---

## ⚡ Performance Considerations

* Uses `bulk_create()` for efficient database inserts.
* Fetches existing emails once to avoid repetitive database queries.
* Wrapped in `transaction.atomic()` for data integrity.

---

## ❗ Error Handling

* Rejects non-CSV files.
* Handles invalid encoding.
* Provides detailed validation errors.
* Skips duplicate emails gracefully.

---

## 👨‍💻 Author

Rahul K Milan
