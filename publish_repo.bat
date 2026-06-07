@echo off
setlocal

set REPO_NAME=Supply-Chain-Digital-Twin
set DESCRIPTION=Industrial Supply Chain Digital Twin featuring Monte Carlo simulation, network science, intervention optimization, resilience analytics and executive decision support.

echo.
echo ============================================
echo Publishing %REPO_NAME% to GitHub
echo ============================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git is not installed or not in PATH.
  pause
  exit /b 1
)

where gh >nul 2>nul
if errorlevel 1 (
  echo ERROR: GitHub CLI is not installed or not in PATH.
  pause
  exit /b 1
)

gh auth status
if errorlevel 1 (
  echo ERROR: GitHub CLI is not authenticated. Run: gh auth login
  pause
  exit /b 1
)

if not exist ".git" (
  git init
)

git branch -M main
git add .
git commit -m "Initial release: Supply Chain Digital Twin platform"

gh repo view %REPO_NAME% >nul 2>nul
if errorlevel 1 (
  gh repo create %REPO_NAME% --public --description "%DESCRIPTION%" --source=. --remote=origin --push
) else (
  git remote remove origin >nul 2>nul
  git remote add origin https://github.com/net421/%REPO_NAME%.git
  git push -u origin main
)

gh repo edit %REPO_NAME% --description "%DESCRIPTION%" ^
  --add-topic supply-chain ^
  --add-topic digital-twin ^
  --add-topic monte-carlo ^
  --add-topic python ^
  --add-topic numba ^
  --add-topic analytics-engineering ^
  --add-topic data-science ^
  --add-topic operations-research ^
  --add-topic simulation ^
  --add-topic inventory-management ^
  --add-topic optimization ^
  --add-topic network-analysis ^
  --add-topic decision-intelligence ^
  --add-topic resilience-engineering

echo.
echo Done. Repository should be available at:
echo https://github.com/net421/%REPO_NAME%
echo.
pause
