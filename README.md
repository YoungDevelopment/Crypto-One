# Crypto-One Webhook Receiver

A FastAPI webhook receiver that forwards messages to Discord.

## Features

- Receives POST requests at the root endpoint
- Forwards webhook payloads to Discord
- Async notification handling

## Local Development

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - Windows PowerShell: `.\venv\Scripts\Activate.ps1`
   - Windows CMD: `.\venv\Scripts\activate.bat`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:

   ```bash
   uvicorn main:app --reload
   ```

5. Access the API:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Deployment to Vercel

### Option 1: Using Vercel CLI

1. Install Vercel CLI:

   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:

   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

### Option 2: Using GitHub Integration

1. Push your code to a GitHub repository

2. Go to [Vercel Dashboard](https://vercel.com/dashboard)

3. Click "Add New Project"

4. Import your GitHub repository

5. Vercel will automatically detect the Python configuration

6. Click "Deploy"

## Environment Variables

If you need to keep the Discord webhook URL as an environment variable:

1. In Vercel Dashboard, go to your project settings
2. Add environment variable:
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Your Discord webhook URL

Then update `main.py` to use:

```python
import os
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
```

## Configuration

- **vercel.json**: Deployment configuration
- **requirements.txt**: Python dependencies
- **runtime.txt**: Python version specification

## API Endpoints

- `POST /` - Webhook receiver endpoint

## License

MIT
