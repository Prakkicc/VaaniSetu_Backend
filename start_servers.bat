@echo off
echo Starting all VaaniSetu Backends...

:: 1. Start Python NER Backend (Port 5000)
start "NER Service (Port 5000)" cmd /k "cd Named_Entity_Recognition && call venv\Scripts\activate && python app.py"

:: 2. Start Django Scheme Engine (Port 8001)
start "Scheme Engine (Port 8001)" cmd /k "cd Govt_Scheme\backend && call venv\Scripts\activate && python manage.py runserver 8001"

:: 3. Start Django Intent Engine (Port 8000)
start "Intent Engine (Port 8000)" cmd /k "cd VaaniSetu_NlpIntent_Backend && python manage.py runserver 8000"

:: 4. Start FastAPI OCR Engine (Port 8002)
start "OCR Engine (Port 8002)" cmd /k "cd OCR_Backend && call venv\Scripts\activate && uvicorn api:app --host 127.0.0.1 --port 8002 --reload"

:: 5. Start Main Node.js Gateway (Port 3000)
:: We add a 3-second timeout to give the Python servers time to boot up first
timeout /t 3 /nobreak >nul
start "Main Node Gateway (Port 3000)" cmd /k "cd MainBackend && node index.js"

echo All 5 servers are launching in separate windows! You can close this window.