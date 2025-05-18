# 🎧 CS235 Pod Library - Podcast Web Application (Flask)

## 📖 Overview

This project is a **web-based digital podcast library**. It allows users to:

- 🔍 **Browse** and **search** podcasts by title, category, author, or language.
- 📝 **Post comments and ratings** on podcasts when logged in.
- ❤️ **Create personal playlists** by adding or removing episodes.
- 🔐 **Register, log in, and manage their accounts securely**.

---

## ✅ Key Features
- 🔎 Search podcasts by title, category, author, and language.
- 🔐 User authentication (registration, login, logout).
- ⭐ Podcast reviews and ratings.
- 📃 Playlist management.

---

## 🛠️ Technologies

- Python
- Flask
- SQLAlchemy ORM
- Jinja2 Templates
- WTForms / Flask-WTF
- Pytest

---

## ⚙️ Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

---

## 🚀 Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
````

---

## 📦 Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/code/switkowski/building-a-podcast-recommendation-engine/input

---

## 🚩 About This Project

This project was originally developed as part of an academic assignment from **COMPSCI 235 - Software Development for the Web** at the **University of Auckland** in **2024 Semester 2**.

It was completed by a team of **three members**.  

While the initial project structure was provided by the course teaching team, all feature implementation, interface development, and functionality were fully developed by our team.

---

## 🧑‍💻 Personal Contribution

In this team project, I was responsible for:

- 🧩 **Designing and implementing parts of the domain model**
- ⚙️ **Developing Flask routes and blueprints** for podcasts, playlists, reviews, and search features
- 🧪 **Writing unit tests** to validate key functionalities, including:
  - Domain model behavior (e.g., Podcast, Episode, Playlist, Review)
  - CSV data loading and repository integration
- ✅ **Ensuring the application passed all functional and non-functional requirements**

---

## 📝 License
This project is provided for educational and portfolio demonstration purposes only.
Redistribution without proper attribution is not allowed.

---

