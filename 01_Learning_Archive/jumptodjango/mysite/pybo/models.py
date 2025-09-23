from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')
    class Meta:
        ordering = ['-create_date']
        indexes = [
            models.Index(fields=['category', 'views']),
            models.Index(fields=['-create_date']),
            models.Index(fields=['-views']),
        ]
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

# 조회 기록 모델 추가
class QuestionView(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('question', 'ip_address')

        indexes = [
            models.Index(fields=['question', 'ip_address']),
            models.Index(fields=['created_at'])
        ]
        verbose_name = '질문 조회 기록'
        verbose_name_plural = '질문 조회 기록들'