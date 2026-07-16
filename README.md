# Local Hub 개발 환경 가이드

이 문서는 팀원이 프로젝트를 처음 클론했을 때 같은 개발 환경을 빠르게 맞추기 위한 안내입니다.

이 프로젝트는 Python 코드를 `backend/` 아래에서 관리하고, Python 가상환경은 프로젝트 루트의 `.venv` 하나만 사용합니다. 하위 폴더마다 `.venv`를 따로 만들지 않습니다.

## 프로젝트 구조

```text
local_hub/
├── .venv/                 # 루트 공용 Python 가상환경, Git에 올리지 않음
├── backend/AI/            # AI 챗봇 FastAPI/그래프 코드
├── backend/               # 메인 FastAPI 백엔드 코드
├── backend/data/          # 로컬 데이터 파일 및 스키마 문서
├── frontend/              # Vue/Vite 프론트엔드
├── backend/requirements.txt  # Python 의존성 단일 관리 파일
├── setup.ps1              # Windows PowerShell용 Python 환경 설정 스크립트
└── setup.sh               # Git Bash/Linux/macOS용 Python 환경 설정 스크립트
```

## 사전 준비

Python과 Node.js가 필요합니다.

- Python: 3.11 이상 권장
- Node.js: `frontend/package.json` 기준 `^22.18.0` 또는 `>=24.12.0`
- Windows 사용자는 PowerShell에서 실행하는 것을 기준으로 합니다.

설치 확인:

```powershell
python --version
node --version
npm --version
```


## Python 가상환경 정책

Python 가상환경은 반드시 루트 폴더의 `.venv` 하나만 사용합니다.

좋은 예:

```text
local_hub/.venv
```

피해야 할 예:

```text
local_hub/backend/.venv
local_hub/backend/AI/.venv
local_hub/venv
```

이렇게 정한 이유는 다음과 같습니다.

- `backend`와 `AI`가 같은 Python 패키지들을 함께 사용합니다.
- 팀원마다 다른 위치에 가상환경을 만들면 import, 실행 경로, 패키지 버전이 쉽게 꼬입니다.
- `backend/requirements.txt` 하나만 관리하면 의존성 변경 사항을 리뷰하기 쉽습니다.

## Windows PowerShell 설정 방법

프로젝트 루트에서 실행합니다.

```powershell
.\setup.ps1
```

이 스크립트가 하는 일:

1. 루트에 `.venv`가 없으면 새로 생성합니다.
2. `.venv` 안의 Python으로 `pip`, `setuptools`, `wheel`을 업데이트합니다.
3. `backend/requirements.txt`에 적힌 Python 패키지를 설치합니다.

설치가 끝나면 현재 터미널에서 가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

활성화되면 프롬프트 앞에 `(.venv)`가 보입니다.

```text
(.venv) PS C:\Users\...\local_hub>
```

## Git Bash/Linux/macOS 설정 방법

프로젝트 루트에서 실행합니다.

```bash
bash setup.sh
```

설치가 끝나면 현재 터미널에서 가상환경을 활성화합니다.

```bash
source .venv/bin/activate
```

## 의존성 추가 방법

Python 패키지를 새로 추가할 때는 `backend/requirements.txt`만 수정합니다.

예:

```text
fastapi==0.111.1
sqlalchemy==2.0.22
```

수정 후 다시 설치합니다.

```powershell
.\setup.ps1
```

또는 Bash 환경에서는:

```bash
bash setup.sh
```

Python 의존성은 `backend/requirements.txt` 하나로만 관리합니다. 백엔드와 AI 의존성을 추가할 때도 이 파일만 수정하면 됩니다.

## 백엔드 실행

먼저 루트에서 가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

메인 백엔드 실행:

```powershell
npm run dev:backend
```

직접 실행할 때는 다음 명령을 사용합니다.

```powershell
python -m uvicorn backend.app.main:app --reload
```

기본 주소:

```text
http://127.0.0.1:8000
```

상태 확인:

```text
http://127.0.0.1:8000/api/health
```

## AI 서버

AI 챗봇 API는 메인 백엔드 실행에 함께 포함됩니다. 백엔드 하나만 실행하면 `/api/chat`도 같이 사용할 수 있습니다.

```powershell
.\.venv\Scripts\Activate.ps1
npm run dev:backend
```

기본 주소:

```text
http://127.0.0.1:8000
```

상태 확인:

```text
http://127.0.0.1:8000/api/health
```

AI 챗봇 CLI를 실행할 때도 루트 가상환경을 활성화한 뒤 실행합니다.

```powershell
python -m backend.AI.app.chatbot.cli
```

## 프론트엔드 실행

프론트엔드는 Python 가상환경과 별개로 `frontend/`에서 npm 의존성을 관리합니다.

```powershell
cd frontend
npm install
npm run dev
```

루트에서 실행할 때는 다음 명령을 사용할 수 있습니다.

```powershell
npm run dev:frontend
```

Vite 개발 서버 주소는 터미널에 출력됩니다. 일반적으로 다음 주소를 사용합니다.

```text
http://localhost:5173
```

## 자주 겪는 문제

### PowerShell에서 스크립트 실행이 막힐 때

아래 명령으로 현재 실행만 허용할 수 있습니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

### `python` 명령을 찾을 수 없을 때

Python이 설치되어 있지 않거나 PATH에 등록되지 않은 상태입니다.

1. Python 3.11 이상을 설치합니다.
2. 설치할 때 `Add python.exe to PATH` 옵션을 켭니다.
3. 새 터미널을 열고 다시 확인합니다.

```powershell
python --version
```

### 패키지 설치가 실패할 때

네트워크, 사내 보안 정책, 프록시, 백신 설정 때문에 PyPI 접속이 막힐 수 있습니다.

다시 시도:

```powershell
.\setup.ps1
```

계속 실패하면 에러 메시지에서 `Failed to establish a new connection`, `Access denied`, `proxy`, `SSL` 관련 문구가 있는지 확인하고 팀에 공유합니다.

### 가상환경이 꼬였을 때

루트 `.venv`를 삭제한 뒤 다시 생성합니다.

```powershell
Remove-Item -Recurse -Force .\.venv
.\setup.ps1
```

단, `backend/AI/.venv`, `backend/.venv` 같은 하위 가상환경은 만들지 않습니다.

### 다른 가상환경이 남아 있는지 확인하기

PowerShell:

```powershell
Get-ChildItem -Recurse -Force -Directory -Include .venv,venv,env | Select-Object -ExpandProperty FullName
```

정상이라면 루트 `.venv`만 보여야 합니다.

## 커밋 전 체크

Python 의존성 충돌 확인:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

프론트엔드 타입 체크 및 빌드:

```powershell
cd frontend
npm run build
```

루트에서 실행할 때는 다음 명령을 사용할 수 있습니다.

```powershell
npm run build:frontend
```

## Git에 올리지 않는 파일

다음 파일과 폴더는 개인 개발 환경에만 필요하므로 Git에 올리지 않습니다.

```text
.venv/
venv/
__pycache__/
.pytest_cache/
```

팀 공용으로 관리해야 하는 파일은 다음입니다.

```text
backend/requirements.txt
setup.ps1
setup.sh
README.md
.env.example
```
