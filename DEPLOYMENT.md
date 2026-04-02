# Deployment Guide

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run counter_party_explorer/app.py
```

## Data Setup

Place your CSV files in the `data/` folder:
- `data/Trade_Lead_Gen_from_Payment.csv`
- `data/Trade_Lead_Gen_from_Remitter.csv`

The app will auto-load these files on startup. Reps won't need to upload anything.

## Password Protection

1. Copy the example secrets file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml` and set your password:
   ```toml
   [auth]
   password = "your-secure-password"
   ```

**Note:** Never commit `secrets.toml` to git (it's in .gitignore).

---

## Deploy to Streamlit Cloud (Recommended)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add files
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/counter-party-explorer.git
git push -u origin main
```

### Step 2: Add Data Files

**Option A: Include in repo** (if data isn't sensitive)
```bash
git add data/*.csv
git commit -m "Add data files"
git push
```

**Option B: Upload separately** (for sensitive data)
- Reps will need to upload via the UI
- Or use Streamlit Cloud's secrets to store a URL to data

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repo
4. Set main file path: `counter_party_explorer/app.py`
5. Click "Deploy"

### Step 4: Configure Secrets

In Streamlit Cloud dashboard:
1. Go to your app's settings
2. Click "Secrets"
3. Add:
   ```toml
   [auth]
   password = "your-secure-password"
   ```
4. Save

Your app will be live at: `https://your-app-name.streamlit.app`

---

## Deploy to Internal Server

### Using Docker (Recommended)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "counter_party_explorer/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t counter-party-explorer .
docker run -p 8501:8501 -v ./data:/app/data counter-party-explorer
```

### Direct Run

```bash
# On your server
streamlit run counter_party_explorer/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

Access at: `http://your-server-ip:8501`

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Port to run on | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Bind address | localhost |

---

## Updating Data

To refresh data:
1. Replace CSV files in `data/` folder
2. Click "↻ Refresh Data" in the app sidebar
3. Or restart the app

---

## Troubleshooting

**App shows "No data loaded"**
- Ensure CSV files are in `data/` folder with correct names
- Check file permissions

**Password not working**
- Verify `.streamlit/secrets.toml` exists and has correct format
- On Streamlit Cloud, check Secrets in app settings

**Slow loading**
- Large CSV files take time to process on first load
- Consider pre-processing data or using caching
