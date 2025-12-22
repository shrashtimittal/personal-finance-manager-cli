# 💰 Personal Finance Management Application (CLI + GUI)

A Python-based personal finance management application designed to help users
track income, expenses, budgets, and generate financial reports.

This project was implemented CLI-first, strictly following the given task
requirements. A graphical desktop interface (GUI) was later added as an
optional extension to improve usability.

---

## 🎯 Project Objective

To develop a command-line application that allows users to:

- Register and authenticate securely
- Track income and expenses
- Categorize transactions
- Generate financial reports
- Manage monthly budgets
- Persist data using a database
- Back up and restore financial data

---

## 🖥️ CLI FEATURES (CORE IMPLEMENTATION)

### 1️⃣ User Registration & Authentication
- Unique username registration
- Secure login system
- User-specific data isolation

**Location:** `auth/`

---

### 2️⃣ Income & Expense Tracking
- Add income and expense transactions
- Update existing transactions
- Delete transactions
- Categorize transactions

**Location:** `transactions/`

---

### 3️⃣ Financial Reports
- Monthly and yearly reports
- Total income, expenses, and savings

**Location:** `transactions/`, `exports/`

---

### 4️⃣ Budget Management
- Monthly budgets by category
- Budget exceed detection

**Location:** `budgets/`

---

### 5️⃣ Data Persistence
- SQLite database storage

**Location:** `database/`

---

### 6️⃣ Backup & Restore
- Backup and restore financial data

**Location:** `data/backups/`

---

### 7️⃣ Testing
- Unit tests using Pytest

**Location:** `tests/`

---

## ▶️ Running the CLI Application

---

## 🖥️ GUI EXTENSIONS (OPTIONAL)

> ⚠️ The graphical user interface (GUI) is an **optional enhancement**.
>  
> The core requirement of a command-line application is fully met
> and remains the primary implementation.

### Why a GUI was added
After completing the CLI-based application, a desktop GUI was developed
to improve usability and visualization, while **reusing the same backend
logic**.

No backend functionality was changed or duplicated for the GUI.

---

### GUI Features
- Login and registration screens
- Dashboard with income, expense, savings overview
- Transaction management (add, edit, delete, filter, paginate)
- Budget visualization with status indicators
- Financial reports with charts
- Insights and recommendations
- CSV export
- Desktop packaging as a standalone executable

---

### GUI Technology
- **Framework:** PySide6 (Qt)
- **Architecture:** Shared backend (CLI + GUI)
- **Packaging:** PyInstaller (Windows EXE)

---

### Running the GUI Application (Optional)


