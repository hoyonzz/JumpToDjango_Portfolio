# **Pybo: Full-Stack Q&A 게시판 (Django)**

### Django 학습의 A to Z: 기획부터 설계, 개발, 배포까지 1인 Full-Cycle 개발 프로젝트

**`단순히 따라 치는 코딩을 넘어, 모든 개념을 손으로 직접 기록하고 파고들며 Django의 동작 원리를 체화했습니다.`**


본 프로젝트는 '점프 투 장고' 교재를 기반으로, 백엔드 개발의 기초부터 실무적인 배포 프로세스까지 **웹 개발의 전체 사이클(Full-Cycle)을 1인 개발**로 완수한 포트폴리오입니다. 백엔드 기초부터 실무 배포까지 3개월간의 모든 학습 내용을 **손코딩 노트로 기록(`02_Study_Materials`)**하고, 각 단계를 **처음부터 다시 코드를 작성하며 체화(`01_Learning_Archive`)**하는 과정을 통해 완성했습니다.

 - **역할:** 풀스택 개발자 (프론트엔드 · 백엔드 · DB · 배포)
 - **기술 스택**
   - **Backend:** Python3 · Django5
   - **Frontend:** HTML5 · CSS3 · Bootstrap5 · JavaScript
   - **Database:** PostgreSQL (prod)
   - **Deployment:** AWS Lightsail · Gunicorn · Nginx
   - **CI/CD & Logging:** RotatingFileHandler (로깅)



**🚀 실제 운영 중인 웹사이트:** [http://13.209.106.188](http://13.209.106.188)  
**(⬆️ 위 링크를 클릭하여 모든 기능을 직접 테스트해보실 수 있습니다.)**

***

## 📁 폴더 구조

```
JumpToDjango_Portfolio/
├─ 01_Learning_Archive/      # 단계별 실습 코드
├─ 02_Study_Materials/       # 손코딩 학습 노트 PDF
├─ 03_Final_Project/         # 배포된 최종 코드
├─ 04_Portfolio_Materials/   # README 및 포트폴리오 자료
└─ 05_Deployment_Config/     # AWS/Gunicorn/Nginx 설정
```

***


## 📂 프로젝트 구조 (03_Final_Project)

```
config/             # 전체 프로젝트 설정
  ├ settings/       # base, local, prod 설정 분리
  ├ urls.py
  ├ wsgi.py
common/             # 인증 · 회원 관리
  ├ models.py      # Profile 모델 + signals
  ├ forms.py       # UserForm, ProfileForm, UserUpdateForm
  ├ views.py       # signup, profile, edit_profile, 404 handler
  ├ urls.py
pybo/               # Q&A 게시판 핵심 로직
  ├ models.py      # Category, Question, Answer, Comment, QuestionView
  ├ forms.py       # QuestionForm, AnswerForm, CommentForm
  ├ views/         # base_views, question_views, answer_views, comment_views, vote_views
  ├ urls.py
templates/          # 공통 · 인증 · 게시판 템플릿
static/             # CSS · JS · Bootstrap · 이미지
logs/               # mysite.log (RotatingFileHandler)
manage.py  
.env  
requirements.txt  
```

***

## ⚙️ 주요 기능 · 시연 GIF

| 기능                     | 설명                                              | GIF                            |
|-------------------------|---------------------------------------------------|--------------------------------------|
| 회원가입 & 로그인      | Django Auth + django-allauth 연동                  | ![Image](https://github.com/user-attachments/assets/91fdf3d9-3014-453b-b485-29eb938d3c70)    |
| 게시글 CRUD            | 질문 작성 · 수정 · 삭제 · 목록 조회                | ![Image](https://github.com/user-attachments/assets/ab1632b9-fbb1-46fc-9112-2486c1e14965)        |
| 답변 기능               | 답변 등록 · 수정 · 삭제 · 답변 링크 이동          | ![Image](https://github.com/user-attachments/assets/0fcedf7f-5fc1-42b4-ae1a-3858283a9430)        |
| 댓글 & 추천 기능        | 질문·답변 댓글, 좋아요(추천)                      | ![Image](https://github.com/user-attachments/assets/8b4cd974-3f78-48d4-b1b4-b930ffecf4a7)
| 검색 & 정렬 기능        | 질문·답변·글쓴이 검색, 추천·인기·최근순으로 정렬   | ![Image](https://github.com/user-attachments/assets/ecb841c7-e96b-4dcc-a0eb-af7611b32731)  
| 오류 페이지            | 404 커스텀 템플릿                                  | <img alt="Image" src="https://github.com/user-attachments/assets/a4248f30-8cbc-4b0f-86b4-8948514104c1" />          |

***

## 🏛️ 시스템 아키텍처

<img alt="Image" src="https://github.com/user-attachments/assets/cb1790df-e969-4ca1-ab49-85325efd5e58" />

### 핵심 설계 원칙
1. **성능 최적화**: Nginx가 정적 파일을 직접 서빙하여 Django 서버 부하 최소화
2. **환경 분리**: 개발(SQLite)과 운영(PostgreSQL) 환경 독립 운영
3. **확장성**: Gunicorn 멀티 프로세싱으로 동시 요청 처리 능력 향상
4. **모니터링**: RotatingFileHandler로 체계적인 로그 관리

***

## 🔍 핵심 코드 하이라이트

### 1. Django Signals를 활용한 프로필 자동 생성
`User` 모델 생성 시 `post_save` 시그널을 받아, 연결된 `Profile` 객체를 자동으로 생성하여 데이터의 정합성을 보장합니다.
```python
# common/models.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### 2. IP 기반 중복 방지 조회수 로직
별도의 `QuestionView` 모델을 두어, 동일 IP의 중복 조회를 방지하고 순수한 조회수(Unique Visitor)를 집계합니다.  
```python
# pybo/views/base_views.py
if not QuestionView.objects.filter(question=question, ip_address=ip).exists():
    question.views += 1
    question.save(update_fields=['views'])
    QuestionView.objects.create(question=question, ip_address=ip)
```

### 3. `annotate`를 활용한 동적 정렬 쿼리  
`annotate`와 `Count`를 사용하여 추천 수를 동적으로 계산하고, 이를 기준으로 질문 목록을 정렬합니다.
```python
# pybo/views/base_views.py
if so == 'recommend':
    question_list = Question.objects.annotate(
        num_voter=Count('voter')).order_by('-num_voter', '-create_date')
```


### 4. 설정 분리 · 배포  
- `settings/base.py`, `local.py`, `prod.py`로 환경별 설정 분리  
- Gunicorn∙Nginx 서비스 파일 커스터마이징  
- AWS Lightsail 배포 스크립트 (`mysite.sh`) 작성  

***

## 💡 저의 성장과 기술적 강점

### 1. "왜?"를 놓치지 않는 집요한 학습 과정
저는 모든 기술을 '그냥' 사용하지 않았습니다. `view` 함수가 복잡해졌을 때 왜 모듈화가 필요한지, `User` 모델을 왜 직접 상속하지 않고 `Profile` 모델로 확장해야 하는지, `Nginx`와 `Gunicorn`은 어떤 역할을 주고받는지 등 **모든 기술적 선택의 이유를 파고들어 30여 개의 `학습 노트(PDF)`로 기록**했습니다. 이 과정을 통해 단순히 지식을 쌓는 것을 넘어, 문제 해결을 위한 최적의 기술을 선택하고 적용하는 능력을 길렀습니다.

**➡️ [저의 3개월간의 학습 기록 전체 보기 (GitHub 폴더 링크)](./02_Study_Materials/)**

### 2. Full-Stack & DevOps: 웹 개발 전체 사이클 경험
백엔드 개발자를 지망하지만, 서비스 전체의 흐름을 이해하기 위해 **프론트엔드(HTML/CSS/JS), 백엔드(Django), 데이터베이스(PostgreSQL), 인프라(AWS) 및 배포(Nginx/Gunicorn)** 까지 모든 과정을 직접 설계하고 구축했습니다. 이 경험을 통해 각 기술 스택의 역할을 명확히 이해하고, 다른 직무의 동료들과 원활하게 협업할 수 있는 기반을 다졌습니다.

### 3. 실무를 고려한 확장 가능성 있는 설계
미래의 유지보수와 기능 확장을 고려하여 실무적인 설계 원칙을 적용했습니다.
*   **환경 분리:** `settings.py`를 `base`, `local`, `prod`로 분리하고 `.env`를 활용하여 민감 정보를 안전하게 관리합니다.
*   **관심사 분리:** 사용자(`common`)와 게시판(`pybo`) 앱을 분리하고, `views.py`를 기능 단위로 모듈화하여 코드의 응집도를 높였습니다.
*   **자동화:** Django `Signals`를 활용하여 `User` 생성 시 `Profile`이 자동으로 생성되도록 구현, 모델 간의 결합도를 낮추고 반복적인 로직을 자동화했습니다.

### 4. IP 기반의 정교한 조회수 기능 구현
단순히 카운트를 증가시키는 방식을 넘어, 별도의 `QuestionView` 모델을 설계하여 사용자의 `IP` 주소를 기록함으로써 **동일한 사용자에 의한 중복 조회수 증가를 방지**하는 정교한 로직을 직접 설계하고 구현했습니다.

***

## 🔧 설치 및 실행

```bash
# 1. 최종 프로젝트 코드 디렉토리로 이동
cd 03_Final_Project

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/Scripts/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. .env 파일 설정 (03_Final_Project 루트에 생성)
# SECRET_KEY='your_secret_key'
# ... (기타 필요한 환경 변수)

# 5. 데이터베이스 마이그레이션
python manage.py migrate

# 6. 개발 서버 실행
python manage.py runserver --settings=config.settings.local
```

***
