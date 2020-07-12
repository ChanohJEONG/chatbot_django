import requests
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from chatbot.models import *
from django.utils import timezone
from chatbot.forms import *
from django.utils.datastructures import MultiValueDictKeyError
from datetime import date, time, datetime, timedelta
# from chatbot.wordcloud_meu import *


tmp = ""
cnt_tmp=0
usual_questions = [["안녕","하이","안녕하세요","미유안녕","미유 안녕","미유하이","미유 하이","안녕하소","안녀엉","안뇽","안뇽!","안뇽~","안뇨옹","안뇨오옹","안녀어엉"],
["뭐먹을까","뭐먹","뭐먹지","뭐먹을까?","뭐먹지?","뭐 먹지","뭐 먹을까","점심 뭐먹지","저녁 뭐먹지","아침 뭐먹지","아침 뭐먹을까","점심 뭐먹을까","저녁 뭐먹을까"],
['시발',"씨발","개새끼","개시","개자식","조까","좆까","좆","시발놈","시발년","씨발놈","씨발년","ㅅㅂ","ㄱㅅㄲ","병신","ㅄ","ㅂㅅ","병신새끼","ㅄ새끼","ㅂㅅ새끼","지랄","지랄하네","ㅈㄹ","ㅈㄹ하네"]]
usual_answer = [["안녕!","안녀엉~","안녕하세여!","안녕하소!","안!녕!","ㅎㅎㅎ안녕!","반가워!!"],
["맛있는거!!","참치어때! 나는 참치가 제일 좋아!","행복한 고민이다옹!","인생 최대의 고민..!"],
["너무해.. 우린 친구라고 생각했는데..","말넘심!!","욕은 정신건강에 해로워!","욕쟁이 할망구!!"]]
# Create your views here.


def index1(request):
    return HttpResponse('<h1>Hello</h1>')


def main(request):  # 메인 화면
    return render(
        request,
        'chatbot/index.html',
        {})


def signup(request):
    if request.method == "POST":
        # 비번 확인
        if request.POST["user_pw"] == request.POST["user_pw2"]:
            # POST 처리 코드
            user_id = request.POST.get('user_id')
            user_pw = request.POST.get('user_pw')
            nick_name = request.POST.get('nick_name')
            email = request.POST.get('email')

            # DB에 저장
            creat_user = Member(
                user_id=user_id,
                user_pw=user_pw,
                nick_name=nick_name,
                email=email,)
            creat_user.save()
            return redirect('/signin')

        else:
            return render(request, 'chatbot/sigup.html', {'error': 'username or password is incorrect'})

    return render(request, 'chatbot/signup.html')


def signin(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'chatbot/signin.html')
    else:
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        # member = Member.objects.get(real_id=user_id, pw=user_pw)
        try:
            member = Member.objects.get(user_id=user_id, user_pw=user_pw)
            request.session['user_id'] = member.user_id
            request.session['user_pw'] = member.user_pw

        except Member.DoesNotExist:
            return HttpResponse("<script>alert('ID 혹은 PWD가 틀립니다.');location = '/signin';</script>")
        else:
            return redirect('/')


def signout(request):
    auth.logout(request)
    return redirect('/')


def mypage(request):  # my pqge
    try:
        member_id = request.session['user_id']  # 로그인 정보
    except:
        return HttpResponse("<script>alert('로그인이 필요합니다.');location = '/signin';</script>")
    member = Member.objects.get(user_id=member_id)  # 로그인 된 user 정보 불러오기
    answers = Answer.objects.filter(m=member.member_id)  # 현재 로그인된 사용자의 answer만 불러오기
    diary_db = diary_answer.objects.filter(m=member.member_id)
    
    myList = []
    for i in range(0,len(diary_db)):
        myList.append(diary_db.values()[i]['useranswer'])
    
    # print(myList)

    # try:
    #     # 5005는 transformer, 5007은 Seq2SeqAttention, 5010은 word cloud
    #     api = requests.get('http://127.0.0.1:5010/'+myList+'&'+member_id, params=request.GET)#70.12.113.194
    # except MultiValueDictKeyError:
    #     api = "API 요청에 실패하였습니다."
    #     print("API 요청이 실패하였습니다.")

    context = {'answers': answers,  # 로그인한 사용자의 답변Data mypage.html에 전달
               'progress': "{0:.2f}".format(len(answers)/60*100), # 진행률 mypage.html에 전달
               'diarys':diary_db} #diary_db 전달
    return render(request, 'chatbot/mypage.html', context)


def chat(request):
    try:
        member_id = request.session['user_id']  # 로그인 정보
    except:
        return HttpResponse("<script>alert('로그인이 필요합니다.');location = '/signin';</script>")
    member = Member.objects.get(user_id=member_id)  # 로그인 된 user 정보 불러오기

    context = {
        'member': member,
    }

    return render(request, 'chatbot/chat.html', context)


def chat2(request):
    global tmp

    try:
        member_id = request.session['user_id']  # 로그인 정보
    except:
        return HttpResponse("<script>alert('로그인이 필요합니다.');location = '/signin';</script>")
    member = Member.objects.get(user_id=member_id)  # 로그인 된 user 정보 불러오기
    answer = Answer()  # DB에 있는 Answer 테이블 불러오기
    # ,answer,chatbot.member
    sql = '''select distinct question.question_id, question.keyword,question.content 
    from question where question.question_id not in
    (select question.question_id from question,answer where question.content = answer.choosequestion and answer.m_id = '''+str(member.member_id)+');'
    questions = Question.objects.raw(sql)  # 질문 DB 에서 사용자가 대답했던 내용 제외하고 가져오기
    
    context = {
        'questions': questions,
        'member': member,
    }

    try:
        useranswer = request.GET['answerObject']  # WEB상에서 사용자가 질문에 대답한 Answer값
    except MultiValueDictKeyError:
        useranswer = False

    try:
        # WEB상에서 사용자가 선택한 질문의 Keyword 값
        userquestion = request.GET['question_ch']
    except MultiValueDictKeyError:
        userquestion = False

    if userquestion != False:
        try:
            tmp = Question.objects.get(keyword=userquestion)
        except Question.DoesNotExist:
            print("DB 내용에 없는 keyword 값입니당")

    print("$"*80)

    if useranswer != False:
        # DB 테이블(Member)에서 user_id 가 member_id와 동일한 내용 조회하여 저장
        answer.m = member
        answer.day = timezone.now()  # 테이블의 day 속성 값에 현재시간 입력
        answer.choosequestion = tmp.content  # 사용자 선택 question 내용 저장
        answer.useranswer = useranswer  # 사용자 답변 content에 저장
        answer.save()

    return render(request, 'chatbot/chat2.html',context)

def chat2_2(request):
    global cnt_tmp
    diary = diary_answer()
    try:
        member_id = request.session['user_id']  # 로그인 정보
    except:
        return HttpResponse("<script>alert('로그인이 필요합니다.');location = '/signin';</script>")
    member = Member.objects.get(user_id=member_id)  # 로그인 된 user 정보 불러오기

    try:
        tmp = diary_answer.objects.filter(day=datetime.now().strftime('%Y-%m-%d'),m=member.member_id)
    except:
        print("DB 입력 오류")
        
    if tmp.exists() and len(tmp)==3:
        print(datetime.now().strftime('%Y-%m-%d'))
        return HttpResponse("<script>alert('오늘 일기는 이미 작성하셨어요! Mypage에서 확인해주세요!');location = '/mypage';</script>") 
    
    try:
        useranswer = request.GET['answerObject']  # WEB상에서 사용자가 질문에 대답한 Answer값
    except MultiValueDictKeyError:
        useranswer = False

    print("="*50)
    print(useranswer)

    context = {
        'member': member,
    }

    if useranswer != False:
        diary.m = member
        diary.day = datetime.now().strftime('%Y-%m-%d')  # 테이블의 day 속성 값에 현재시간 입력
        diary.question =  cnt_tmp # 사용자 선택 question 내용 저장
        diary.useranswer = useranswer  # 사용자 답변 content에 저장
        diary.save()
        if cnt_tmp == 2:
            cnt_tmp =0
        else:
            cnt_tmp = cnt_tmp +1

    return render(request, 'chatbot/chat2_2.html',context)


def chat3(request):

    # try:
    #     useranswer = request.GET['answer']  # WEB상에서 사용자가 질문에 대답한 Answer값 Form 태그
    # except MultiValueDictKeyError:
    #     useranswer = False

    # print('==========================================')
    # print(useranswer)

    return render(request, 'chatbot/chat3.html', {})


def conversation(request):
    global usual_answer
    global usual_questions
    try:
        member_id = request.session['user_id']  # 로그인 정보
    except:
        return HttpResponse("<script>alert('로그인이 필요합니다.');location = '/signin';</script>")

    ChatDB = Chat_data()  # chat DB 다불러옴
    member = Member.objects.get(user_id=member_id)  # 로그인 된 user 정보 불러오기

    try:
        text = request.GET['answerObject']  # WEB상에서 사용자가 질문에 대답한 Answer값
    except MultiValueDictKeyError:
        text = False

    for i in range(len(usual_questions)):
        if text in usual_questions[i]:
            answer = random.choice(usual_answer[i])
            return HttpResponse(answer)
    
    try:
        # 5005는 transformer, 5007은 Seq2SeqAttention
        api = requests.get('http://127.0.0.1:5005/'+text, params=request.GET)#70.12.113.194
    except MultiValueDictKeyError:
        api = "API 요청에 실패하였습니다."
        print("API 요청이 실패하였습니다.")

    print('=========================================')
    print(text)
    answer = api.text  # trans_answer(text)#transformer 대답

    print('==================API 응답==================')
    print(answer)

    ChatDB.m = member  # DB 테이블(Member)에서 user_id 가 member_id와 동일한 내용 조회하여 저장
    ChatDB.day = timezone.now()  # 테이블의 day 속성 값에 현재시간 입력
    ChatDB.User = text  # user input DB 저장
    ChatDB.Chat = answer  # chat ouput DB저장
    ChatDB.save()  # DB 저장

    return HttpResponse(answer)


def conversation_2(request):
    try:
        text = request.GET['answerObject']  # WEB상에서 사용자가 질문에 대답한 Answer값
        r = requests.get('http://70.12.113.194:5006/'+text, #70.12.113.194
                         params=request.GET)  # BERT API 요청
    except MultiValueDictKeyError:
        text = False

    answer = r.text
    print('-----------------Bert API 응답-----------------')
    print(answer)

    return HttpResponse(answer)

def delete(request, diary_id):
    diary = diary_answer.objects.get(id = diary_id)
    diary.delete()
    return redirect('/mypage/',{})

def edit(request, diary_id):
    diary = diary_answer.objects.get(id = diary_id)
    if request.method == "POST":
        form = Diary_Post(request.POST,request.FILES)
        if form.is_valid(): 
            
            print(form.cleaned_data)
            diary.useranswer = form.cleaned_data['useranswer']
            diary.save()
            return redirect('/mypage/')
    else:
        form = Diary_Post()
        return render(request, 'chatbot/edit_post.html',{'form':form})


def explain_model(request):  # 메인 화면
    return render(
        request,
        'chatbot/explain_model.html',
        {})

def explain_web(request):  # 메인 화면
    return render(
        request,
        'chatbot/explain_web.html',
        {})

def about_us(request):  # 메인 화면
    return render(
        request,
        'chatbot/about_us.html',
        {})