# PrickledHerald-Instabot

This is an Instagram bot for posting images with captions, automatically generating content from articles, and handling image processing.

## Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/prickledherald-instabot.git
cd prickledherald-instabot
```

### **2. Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### **3. Install Required Dependencies**
```bash
pip install -r requirements.txt
```

---

## Configuration (.env Setup)
To securely store API keys and credentials, create a `.env` file in the project directory.

### **1. Create a `.env` File**
Create a new file named `.env` in the project root directory and add the following:

```
ACCESS_TOKEN="your_instagram_access_token_here"
INSTAGRAM_ACCOUNT_ID="your_instagram_account_id_here"
IMGUR_CLIENT_ID="your_imgur_client_id_here"
```

### **2. Ensure `.env` is Not Committed**
Check that `.env` is in `.gitignore` to prevent accidentally pushing sensitive credentials:
```bash
git check-ignore -v .env
```
If `.env` is tracked, remove it from Git history:
```bash
git rm --cached .env
```

---

## Running the Bot
Once everything is set up, you can run the bot:
```bash
python main.py
```

---

## Updating the Bot
To pull the latest updates from GitHub:
```bash
git pull origin main
pip install -r requirements.txt  # Reinstall dependencies if needed
```

---

## Troubleshooting
### **1. `ModuleNotFoundError`**
If you get a missing module error, ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

### **2. `.env` Not Loading**
Make sure you installed `python-dotenv` and your `.env` file is in the correct location.

### **3. `git push` Issues**
If `.env` was committed by mistake:
```bash
git rm --cached .env
git commit -m "Removed .env from tracking"
git push origin main
```

---

## Contributing
If you'd like to contribute, fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License.

