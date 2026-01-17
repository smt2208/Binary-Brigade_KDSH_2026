# Complete Setup Guide for Windows

**Team:** Binary Brigade  
**Project:** Character Backstory Verification System

---

## Prerequisites

- **Windows 10/11** (64-bit)
- **At least 8GB RAM** (16GB recommended)
- **10GB free disk space**
- **Internet connection**

---

## Step 1: Install Docker Desktop

### 1.1 Download Docker Desktop

1. Go to [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Click **"Download for Windows"**
3. Save the installer (`Docker Desktop Installer.exe`)

### 1.2 Install Docker Desktop

1. **Run the installer** - Double-click `Docker Desktop Installer.exe`
2. **Follow the installation wizard:**
   - Check "Use WSL 2 instead of Hyper-V" (recommended)
   - Click "Ok"
3. **Wait for installation** (takes 5-10 minutes)
4. **Restart your computer** when prompted

### 1.3 Start Docker Desktop

1. Launch **Docker Desktop** from Start Menu
2. Wait for Docker engine to start (whale icon in system tray will stop animating)
3. You should see "Docker Desktop is running" notification

### 1.4 Verify Docker Installation

Open PowerShell and run:
```powershell
docker --version
docker-compose --version
```

Expected output:
```
Docker version 24.x.x, build xxxxxxx
Docker Compose version v2.x.x
```

---

## Step 2: Install Python

### 2.1 Check if Python is Installed

Open PowerShell and run:
```powershell
python --version
```

If you see `Python 3.10.x` or higher, skip to Step 3.

### 2.2 Download Python

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download **Python 3.10** or higher
3. Run the installer

### 2.3 Install Python

⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation!

1. Run the installer
2. ✅ Check **"Add python.exe to PATH"**
3. Click **"Install Now"**
4. Click "Yes" when prompted by Windows

### 2.4 Verify Python Installation

Open a **NEW** PowerShell window and run:
```powershell
python --version
pip --version
```

---

## Step 3: Setup the Project

1. Extract the project ZIP file to your desired location (e.g., `E:\Projects\Novel_RAG\Code\`)
2. Open PowerShell and navigate to the Code folder:
```powershell
cd E:\Projects\Novel_RAG\Code
```

---

## Step 4: Install Python Dependencies

### 4.1 Create Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### 4.2 Install Required Packages

```powershell
pip install -r requirements.txt
```

This will install:
- langchain, langgraph
- openai
- pandas
- pathway
- And all other dependencies

Wait 2-5 minutes for installation to complete.

---

## Step 5: Configure OpenAI API Key

### 5.1 Get Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Log in to your account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)

### 5.2 Create .env File

Create a file named `.env` in the `Code` folder:

```powershell
notepad .env
```

Add this line (replace with your actual key):
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Save and close Notepad.

### 5.3 Verify .env File

```powershell
cat .env
```

Should display:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## Step 6: Prepare Data Files

Ensure your project structure looks like this:

```
E:\Projects\Novel_RAG\Code\
├── main.py
├── run.py
├── .env
├── docker-compose.yml
├── requirements.txt
├── data/
│   ├── test.csv
│   └── Books/
│       ├── In search of the castaways.txt
│       └── The Count of Monte Cristo.txt
├── config/
├── src/
└── servers/
```

**Important:** Make sure `test.csv` and both book files are in the correct locations!

---

## Step 7: Run the Complete Pipeline

### 7.1 Single Command Execution (Recommended)

This command does everything automatically:
- Starts Docker containers
- Waits for vector stores to be ready
- Processes all test data
- Generates results.csv

```powershell
python run.py
```

### 7.2 What to Expect

You'll see output like:
```
🔍 Checking if Docker is installed...
✅ Docker is installed!

🚀 Starting Docker containers...
✅ Containers started successfully!

⏳ Waiting for servers to be ready...
   Waiting for server on port 8765... (1/30)
   Waiting for server on port 8766... (1/30)
✅ Both servers are ready!

🚀 Starting Novel RAG Verification System
================================================================================
📊 Loaded 60 test cases

################################################################################
Processing 1/60 - ID: 95
################################################################################
...
```

### 7.3 Processing Time

- **Per row:** 10-20 seconds
- **60 rows:** ~15-30 minutes
- The system will retry failed rows automatically

### 7.4 Output

When complete, you'll find:
- `results.csv` - Your predictions in submission format

---

## Step 8: Manual Docker Control (Optional)

### Start Servers Manually
```powershell
docker-compose up -d --build
```

### Check Server Status
```powershell
docker-compose ps
```

### View Server Logs
```powershell
docker-compose logs -f pathway-castaways
docker-compose logs -f pathway-monte-cristo
```

### Stop Servers
```powershell
docker-compose down
```

### Run Main Script (After Servers Are Running)
```powershell
python main.py
```

---

## Troubleshooting

### ❌ "Docker is not running"

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (whale icon stops animating)
3. Try again

### ❌ "Read timed out" errors

**Solution:**
- These are handled automatically with retry logic
- System will retry up to 5 times per row
- All rows guaranteed to be processed

### ❌ "OPENAI_API_KEY not found"

**Solution:**
1. Make sure `.env` file exists in `Code` folder
2. Open `.env` and verify the key is correct
3. No spaces around the `=` sign

### ❌ "Port 8765 already in use"

**Solution:**
```powershell
docker-compose down
docker-compose up -d --build
```

### ❌ "No module named 'langchain'"

**Solution:**
```powershell
pip install -r requirements.txt
```

### ❌ PowerShell execution policy error

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Docker containers won't start

**Solution:**
1. Open Docker Desktop
2. Click Settings → Resources
3. Increase Memory to at least 4GB
4. Click "Apply & Restart"

---

## Verification Steps

### Check Everything is Working

1. **Docker running:**
   ```powershell
   docker ps
   ```
   Should show 2 containers running

2. **Python imports:**
   ```powershell
   python -c "from src.graph_agent import graph; print('✅ OK')"
   ```

3. **API key configured:**
   ```powershell
   python -c "from config.config import OPENAI_API_KEY; print('✅ API Key loaded')"
   ```

4. **Servers responding:**
   ```powershell
   curl http://localhost:8765/health
   curl http://localhost:8766/health
   ```

---

## Quick Reference Commands

| Action | Command |
|--------|---------|
| Start everything | `python run.py` |
| Check Docker status | `docker ps` |
| View server logs | `docker-compose logs -f` |
| Stop Docker | `docker-compose down` |
| Restart Docker | `docker-compose restart` |
| Check results | `cat results.csv` |
| Activate venv | `.\venv\Scripts\Activate.ps1` |
| Deactivate venv | `deactivate` |

---

## Expected Results Format

Your `results.csv` should look like:
```csv
story_id,prediction,rationale
95,0,Evidence 5 shows the opposite dynamic: during the Hundred Days...
136,0,Faria says he was Cardinal Spada's secretary for twenty years...
59,1,The novel presents Thalcave as a highly capable outdoorsman...
```

- **story_id:** Test case ID
- **prediction:** 1 (consistent) or 0 (contradict)
- **rationale:** Brief explanation (max 150 chars)

---

## System Requirements Summary

✅ **Minimum:**
- Windows 10/11 64-bit
- 8GB RAM
- 4-core CPU
- 10GB free disk space

✅ **Recommended:**
- Windows 11 64-bit
- 16GB RAM
- 8-core CPU
- 20GB free disk space
- SSD storage

---

## Support

If you encounter issues:

1. Check Docker Desktop is running
2. Verify `.env` file has correct API key
3. Ensure all files are in correct folders
4. Check PowerShell is running as Administrator (if permission errors)
5. Review the Troubleshooting section above

For persistent issues, check:
- Docker Desktop logs (Settings → Troubleshoot → Get Logs)
- Terminal output for error messages
- `results.csv` for any rows with fallback predictions

---

## Success Checklist

Before running the pipeline, verify:

- [ ] Docker Desktop installed and running
- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with OpenAI API key
- [ ] `test.csv` exists in `data/` folder
- [ ] Both book files exist in `data/Books/` folder
- [ ] Terminal is in `Code` folder

Then run: `python run.py`

---

**Good luck! 🚀**
