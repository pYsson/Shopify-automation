# Shopify-automation
## Description
- requests 라이브러리를 통해 쇼피파이 결제 자동화 (In progress)
  - 원하는 제품의 링크를 통해 해당 제품 리스탁 모니터링 
  - 원하는 사이즈 모니터링 후 리스탁 시 오토 카팅 및 결제
  - 프록시 로테이션 기능
  - 원하는 사이즈 범위 설정 기능
  - 웹훅 설정 및 테스트 기능

## Installation
1. 레포지토리 클론  
```git clone https://github.com/pYsson/Shopify-automation.git```
2. 필요한 라이브러리 설치  
```pip install -r requirements.txt```

## How to run your Bot
1. profile 폴더 내 profile_us.json 파일에 프로필 정보 작성  
2. proxies.txt 파일에 프록시 추가  
  - ip : port : id :pw 형식  
3. setting.json 파일에 디스코드 웹훅 URL 추가  
  - 추가를 하지 않더라도 파일 실행시 추가 가능  
4. main.py 파일 실행  
```python3 main.py``` or ```python main.py```  
<img width="776" alt="스크린샷 2022-01-16 오전 1 00 09" src="https://user-images.githubusercontent.com/97378861/149628607-b3e3e36c-88aa-4dc4-844e-59d84e4d4173.png">

## How to start your Restock Task
![무제](https://user-images.githubusercontent.com/97378861/149628918-cd9a8269-f70c-41ee-b77c-286d41cd96e3.jpg)  
![image](https://user-images.githubusercontent.com/97378861/149630612-08c8ceb9-9d7f-4469-92d0-49b348561bef.png)
