# Skill Swap Platform

A web-based platform that enables users to exchange skills through a friendly, interactive interface. Built with Flask, Python, and standard web technologies.

## 🚀 Features

- User registration and login
- Profile management
- List skills you can offer and skills you want to learn
- Search for users by skills and availability
- Send and manage skill swap requests
- Dashboard to view your swaps and history

## 🏗️ Tech Stack

- Python 3.x
- Flask
- Jinja2 Templates
- SQLite/MySQL/PostgreSQL (configurable)
- HTML/CSS/Bootstrap

## 📁 Project Structure

```
Skill_Swap_Platform/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/
│   ├── css/
│   └── js/
├── models.py
├── forms.py
└── README.md
```

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HARRY5D/Skill_Swap_Platform.git
   cd Skill_Swap_Platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**  
   Create a `.env` file and add your configuration (e.g., SECRET_KEY).

5. **Initialize the database**
   ```bash
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   flask run
   ```
   The app will be available at `http://localhost:5000/`

## 👤 User Guide

- Register for an account and log in.
- Edit your profile to add your skills (offered and wanted).
- Browse other users and send swap requests.
- Accept, reject, or manage incoming swap requests from your dashboard.

## 🛠️ Configuration

- Edit `config.py` (or set environment variables) for database URI, secret key, etc.

## 🧪 Testing

You can run tests (if available) with:
```bash
python -m unittest discover
```

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push and open a pull request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues, please open an issue on the GitHub repo.
