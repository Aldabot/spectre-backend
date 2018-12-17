# Spectre API & PostgreSQL
### Setup
1. Clone repository  
```bash
git clone  git@github.com:Aldabot/spectre-backend.git`
```
2. Create Virtual Environment
```bash
cd spectre-backend  
virtualenv venv
source venv/bin/activate
```  
3. Install requirements
```bash
pip install -r requirements.txt
```  
4. Create Environment variables in `.env`
```bash
touch .env
# fill .env with credentials from postman
```  

5. If needing a kernel in order to debug:
```bash
python3 -m pip install ipykernel  
python3 -m ipykernel install --user
```
