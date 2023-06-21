# HACK-EDUTECH-Back

## 1. miniconda 설치
> https://docs.conda.io/en/latest/miniconda.html 참조  
Window의 경우는 exe 파일로 설치가능하면 MacOS 와 Linux 의 경우 쉘 스크립트를 이용하여 설치

## 2. 가상환경 설치
> conda env create -f requirements.yml
- p.s 가상환경이 존재하는데 가상환경을 업데이트 해야 할 경우  
```conda env update -n hack-edutech-back -f requirements.yml --prune```

## 3. 가상환경 실행
> conda activate hack-edutech-back

## 4. DJANGO_SECRET 환경변수 값 설정  
둘 중 하나를 선택
1. ```.env``` 파일을 통한 설정  
    ```echo DJANGO_SECRET=your-secret-key > .env```
2. 환경변수 값 설정  
    windows : ```set DJANGO_SECRET=your-secret-key```  
    linux : ```export DJANGO_SECRET=your-secret-key```  

## 5. 개발모드로 서버 실행
```python manage.py runserver (포트번호)```  
ex) ```python manage.py runserver``` 또는 ```python manage.py runserver 8000```