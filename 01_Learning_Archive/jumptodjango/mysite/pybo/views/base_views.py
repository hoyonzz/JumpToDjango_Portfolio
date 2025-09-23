from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question, Answer, Category, QuestionView



def index(request, category_id=None):
    # pybo 목록 출력

    # 입력 인자
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준

    # 전체 카테고리 목록 조회
    categories = Category.objects.all()

    # 선택된 카테고리 객체 가져오기(없다면 None)
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
    else:
        category = None

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    # 카테고리별 필터링(category_id 있으면 해당 카테고리만)
    if category:
        question_list = question_list.filter(category=category)

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(author__username__icontains=kw) | # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list':page_obj,'categories':categories, 'category':category, 'page': page, 'kw':kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # pybo 내용 출력

    # 입력 인자
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')

    # 조회
    question = get_object_or_404(Question, pk=question_id)
    ip = get_client_ip(request)

    # 이미 조회한 적이 있는지 확인하기
    if not QuestionView.objects.filter(question=question, ip_address=ip).exists():
        # 처음 조회하는 경우에만 죄후 증가
        question.views += 1
        question.save(update_fields = ['views'])

        # 조회 기록 저장
        QuestionView.objects.create(question=question, ip_address=ip)

    # 정렬
    if so == 'recommend':
        answer_list = Answer.objects.filter(question=question).annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = Answer.objects.filter(question=question).annotate(
            num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else: # recent
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')
        
    # 페이징 처리
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list':page_obj, 'so':so}
    return render(request, 'pybo/question_detail.html', context)

def get_client_ip(request):
    # 클라이언트 IP주소를 가져오는 함수
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

