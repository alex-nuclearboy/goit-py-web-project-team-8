# Personal Assistant App

The code for the personal assistant application, developed by Team 8 as part of the Python web course at GoIT

## Getting Started

### Prerequisites

- **Docker and Docker Compose:** Ensure you have Docker and Docker Compose installed on your system to handle the application and database containers.
- **Python:** Ensure Python 3.10 or higher is installed on your system.
- **Poetry:** This project uses Poetry for dependency management.

### Installation

- **Fork the repository:**
Click the "Fork" button in the upper right corner to create a copy of the repository under your GitHub account.

- **Clone the repository:**
```bash
git clone https://github.com/<your-github-username>/goit-py-web-project-team-8.git
```

**NOTE:** Replace `<your-github-username>` with your actual GitHub username. 

- **Navigate to the project directory:**
```bash
cd goit-py-web-project-team-8
```

- **Create your own branch:**
```bash
git branch <new-branch>
git checkout <new-branch>
```

- **To set up the environment** use the following commands depending on your operating system:
   - Unix/Linux/macOS:
   ```bash
   cp .env.example .env
   ```
   - Windows:
   ```powershell
   copy .env.example .env
   ```

**NOTE:** Adjust `.env` file with your settings

- **Activate the Poetry environment and install dependencies:**
```bash
poetry shell
poetry install --no-root
```

- **Start the PostgreSQL server:**
```bash
docker compose up -d
```

- **Navigate further into the Django project directory:**
```bash
cd personal_assistant/
```

- **Perform database migrations and data transfers:**
```bash
python manage.py migrate
```

- **Create a superuser to manage the app as an administrator:**
```bash
python manage.py createsuperuser
```

- **Start the Django development server**:
```bash
python manage.py runserver
```

### Accessing the Application

After starting the server, open a web browser and visit the following URL to access the application:

[http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

### Making Changes

- **Regularly pull the latest changes from the main repository to keep your branch up to date:**
```bash
git pull origin main
```

- **Make your changes in the code.**

- **Add your changes to the staging area and commit them:**
```bash
git add .
git commit -m "Descriptive commit message"
```

- **Push your changes to the remote repository:**
```bash
git push origin <your-branch>
```
