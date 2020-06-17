from django.db import models

# Create your models here.
class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=40)
    user_pw = models.CharField(max_length=40, blank=True, null=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'member'

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100)
    content = models.CharField(max_length=200)

    class Meta:
        db_table = 'question'

class Answer(models.Model):
    m = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    choosequestion = models.CharField(max_length=200)
    useranswer = models.CharField(max_length=200)

    class Meta:
        db_table = 'answer'

class diary_answer(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField(blank=True, null=True)
    m = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    question = models.CharField(max_length=200)
    useranswer = models.CharField(max_length=200)

    class Meta:
        db_table = 'diary_answer'

class Chat_data(models.Model):
    id = models.AutoField(primary_key=True)
    m = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    User = models.CharField(max_length=200)
    Chat = models.CharField(max_length=200)

    class Meta:
        db_table = 'chat_data'
