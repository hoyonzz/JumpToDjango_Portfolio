from django import forms
from .models import Question, Answer, Comment, Category



class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='게시판'
    )
    class Meta:
        model = Question
        fields = ['category', 'subject', 'content']
        labels = {
            'category': '카테고리',
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변 내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }