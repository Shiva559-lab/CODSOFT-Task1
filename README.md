# CODSOFT-Task1
# ✦ Task 1 — To-Do List Application

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

A feature-rich **GUI-based To-Do List application** built with Python and Tkinter. Manage your daily tasks with priorities, due dates, search, and filtering — all in a sleek dark-themed interface with zero external dependencies.

---

## 📸 Preview

```
╔══════════════════════════════════════╗
║         ✦ TASK FORGE                 ║
║   your work, forged in order         ║
╠══════════════════════════════════════╣
║  12 total   8 active   4 done  33%  ║
╠══════════════════════════════════════╣
║  ⌕ Search tasks…    [All][Active][Done]  [+ ADD TASK] ║
╠══════════════════════════════════════╣
║ ▐ ○  Buy groceries        ▲ High  ⏰ 2025-12-01  ✎ ✕ ║
║ ▐ ✓  Submit assignment    ▲ Low   added Dec 01   ✎ ✕ ║
╚══════════════════════════════════════╝
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ **Add Task** | Create tasks with title, note, due date & priority |
| ✎ **Edit Task** | Update any field via a clean pop-up dialog |
| ✓ **Toggle Complete** | Mark tasks done/undone with one click |
| ✕ **Delete Task** | Remove tasks with a confirmation prompt |
| 🔍 **Live Search** | Filter tasks by title or note in real-time |
| 🗂 **Filter Tabs** | Switch between All / Active / Done views |
| ⌫ **Clear Done** | Bulk-remove all completed tasks at once |
| 📊 **Progress Bar** | Visual completion percentage tracker |
| 💾 **Auto-Save** | Tasks persist to `tasks.json` across sessions |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external packages required — uses Python's standard library only

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/python-projects.git
cd python-projects/task1-todo

# Run the application
python todo_app.py
```

---

## 🎯 How to Use

| Action | How |
|---|---|
| Add a task | Click **+ ADD TASK** button |
| Complete a task | Click the **○** circle on any task card |
| Edit a task | Click the **✎** pencil icon |
| Delete a task | Click the **✕** icon and confirm |
| Search | Type in the search bar (live filter) |
| Filter by status | Click **All**, **Active**, or **Done** tabs |
| Clear completed | Click **⌫ CLEAR DONE** at the bottom |

---

## 🗂 Priority System

| Level | Color | Use Case |
|---|---|---|
| 🔴 **High** | Coral Red | Urgent, time-sensitive tasks |
| 🟡 **Medium** | Warm Gold | Standard priority tasks |
| 🟢 **Low** | Green | Nice-to-do, no deadline |

---

## 📁 Project Structure

```
task1-todo/
│
├── todo_app.py       # Main application (single file)
└── tasks.json        # Auto-generated data file (created on first run)
```

---

## 💾 Data Storage

Tasks are saved automatically to `tasks.json` in the same directory. Each task stores:

```json
{
  "title": "Buy groceries",
  "note": "Don't forget milk",
  "due": "2025-12-01",
  "priority": "High",
  "done": false,
  "created": "Nov 28"
}
```

---

## 🛠 Built With

- **Python 3** — Core language
- **Tkinter** — GUI framework (built into Python)
- **JSON** — Lightweight data persistence

---

