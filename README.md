# 💰 Personal Finance Management Application (CLI + GUI)

![Core Implementation](https://img.shields.io/badge/Core-CLI-success)
![Extension](https://img.shields.io/badge/GUI-Optional-blue)
![Language](https://img.shields.io/badge/Python-3.9+-yellow)

A Python-based personal finance management application designed to help users
track income, expenses, budgets, and generate financial reports.

This project was implemented **CLI-first**, strictly following the given task
requirements. A graphical desktop interface (GUI) was later added as an
**optional extension** to improve usability and visualization.

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

## 📁 Project Structure Overview

```text
personal-finance-manager/
│
├── auth/                # User registration & authentication (CLI)
├── transactions/        # Income & expense handling + reports logic
├── budgets/             # Budget management and alerts
├── database/            # SQLite database connection & schema
├── data/                # Backups and persistent data
├── exports/             # CSV export utilities
├── tests/               # Unit tests (Pytest)
│
├── gui/                 # Optional GUI (Desktop Application)
│   ├── pages/           # GUI pages (Dashboard, Transactions, etc.)
│   ├── widgets/         # Reusable UI components
│   ├── dialogs/         # Modal dialogs
│   ├── styles/          # Qt stylesheets (QSS)
│   └── main.py          # GUI entry point
│
├── assets/              # Icons and UI assets
├── main.py              # CLI entry point
└── README.md

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
- Categorize transactions (e.g., Food, Rent, Salary)

**Location:** `transactions/`

---

### 3️⃣ Financial Reports
- Monthly and yearly reports
- Automatic calculation of total income, expenses, and savings

**Location:** `transactions/`, `exports/`

---

### 4️⃣ Budget Management
- Monthly budgets by category
- Budget exceed detection and alerts

**Location:** `budgets/`

---

### 5️⃣ Data Persistence
- SQLite database storage
- Automatic database creation on first run

**Location:** `database/`

---

### 6️⃣ Backup & Restore
- Backup financial data
- Restore data from previous backups

**Location:** `data/backups/`

---

### 7️⃣ Testing
- Unit tests using Pytest
- Core functionality coverage

**Location:** `tests/`

---

## ▶️ How to Run the Application (Step-by-Step)

### 🔧 Prerequisites
Ensure the following are installed:
- Python 3.9 or higher
- Git

Verify installation:
```bash
python --version
git --version

---

## 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/shrashtimittal/personal-finance-manager-cli.git
cd personal-finance-manager-cli

## ▶️ Step 2: Run the CLI Application

Start the command-line application using:

```bash
python main.py

---

## 🧭 Using the Application

Once the application starts, you can perform the following actions through the
interactive CLI prompts:

- Register a new user or log in with existing credentials
- Add income and expense entries
- Categorize transactions (e.g., Food, Rent, Salary)
- View monthly and yearly financial summaries
- Set and monitor category-wise budgets
- Automatically persist all data using SQLite

All interactions are handled through **clear, guided command-line prompts**,
making the application easy to use without prior setup.

---

## 🧪 Running Tests (Optional)

Unit tests are written using **Pytest** to validate core functionality.

Install Pytest (if not already installed):
```bash
pip install pytest

Run the test 
```bash
pytest

---

## 🖥️ GUI EXTENSIONS (OPTIONAL)

> ⚠️ The graphical user interface (GUI) is an **optional enhancement**.
> The core requirement of a command-line application is fully met
> and remains the primary implementation.

### Why a GUI was added
After completing the CLI-based application, a desktop GUI was developed
to:
- improve usability 
- and Provide better data visualization
- Demonstrate integration of a GUI with an existing backend
The GUI **reuses the same backend
logic** as the CLI.

No backend functionality was changed or duplicated for the GUI.

---

### GUI Features
- Login and registration screens
- Dashboard with income, expense, savings overview
- Transaction management (add, edit, delete, filter, paginate)
- Budget visualization with status indicators
- Financial reports with charts
- Insights and recommendations
- CSV export functionality
- Desktop packaging as a standalone executable

---

### GUI Technology
- **Framework:** PySide6 (Qt)
- **Architecture:** Shared backend (CLI + GUI)
- **Packaging:** PyInstaller (Windows EXE)

---

### Running the GUI Application (Optional)

---

The GUI provides a desktop-based interface built on top of the same backend logic
used by the CLI.

---

### 🔧 Prerequisites for GUI

Ensure the following are installed:
- Python 3.9 or higher
- PySide6 (Qt for Python)

---

### 📦 Step 1: Install GUI Dependency

Install PySide6 using pip:
```bash
pip install PySide6

## ▶️ Step 2: Run the GUI Application

Launch the GUI using:
```bash
python -m gui.main

## 🧭 Using the GUI Application

Once launched, the GUI allows you to:

- Register and log in using the same user system as the CLI
- View a dashboard with income, expenses, savings, and budget status
- Add, edit, delete, and filter transactions
- Visualize budgets with progress indicators
- Generate financial reports with charts
- View insights and recommendations
- Export reports to CSV

All data used by the GUI is **shared with the CLI** and stored in the same
SQLite database.

---

## 🪟 Optional: Windows Executable

The GUI can also be packaged as a standalone Windows executable using PyInstaller.
Refer to the packaging section for build instructions.

