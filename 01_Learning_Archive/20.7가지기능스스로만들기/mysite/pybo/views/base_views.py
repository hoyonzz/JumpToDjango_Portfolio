from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question, Category



def category_question_list(request, category_id):
    # 카테고리별 질문리스트
    category = get_object_or_404(Category, pk=category_id)

    # 입력 인자
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    question_list = Question.objects.filter(category=category)

    if so == 'recommend':
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    category_list = Category.objects.all()

    context = {'category': category, 'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category_list':category_list}

    return render(request, 'pybo/category_question_list.html', context)




def index(request):
    # pybo 목록 출력

    
    # 입력 인자
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') #정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    category_list = Category.objects.all()
    context = {'question_list': page_obj, 'page':page, 'kw':kw, 'so':so, 'category_list': category_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # pybo 내용 출력
    question = get_object_or_404(Question, pk=question_id)
    
    # 입력 인자
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'recommend':
        answer_list = question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = question.answer_set.order_by('-view_count', '-create_date')
    else:
        answer_list = question.answer_set.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'question':question, 'answer_list': page_obj, 'so':so}
    return render(request, 'pybo/question_detail.html', context)
