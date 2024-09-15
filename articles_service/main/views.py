from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Article, Comment
from django.http import JsonResponse
from .forms import CommentForm
import pytz
from django.contrib import messages
from django.utils.html import escape



# Create your views here.

def home(request):
    articles = Article.objects.filter(published=True).order_by('-date')
    return render(request, 'home.html', {'articles': articles})


@require_POST
def save_text(request):
    text = request.POST.get('text')
    request.session['text'] = text
    print(text)
    return JsonResponse({}, status=200)


def create_article_page(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Для того, чтобы написать статью, вам необходимо авторизироваться')
        return redirect(reverse('login'))
    text = request.session.get('text')
    return render(request, 'create_article.html', {'text': text})


@login_required
@require_POST
def create_article(request):
    title = request.POST.get('article_title')
    text = request.POST.get('article_text')
    if len(title) < 3 or len(text) < 10:
        return JsonResponse({"message": "Слишком короткое название или текст"}, status=400)
    else:
        image = request.FILES.get('article_image')
        print(request.FILES)
        print('hui')
        print(image)
        new_article = Article(title=title, text=text, author=request.user)
        if image:
            new_article.image = image
        new_article.save()
        return JsonResponse({}, status=200)


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.published == False and not request.user.groups.filter(name='admin').exists():
        messages.error(request, 'У вас нету прав доступа к данной странице')
        return render(request, 'control_panel.html')
    else:
        comments = Comment.objects.filter(article=article).order_by('-date')
        form = CommentForm()
        return render(request, 'article.html', {'article': article, 'form': form,
                                                'comments': comments})


@require_POST
def send_comment(request, article_id):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            text = escape(form.cleaned_data.get('text'))
            get_article = get_object_or_404(Article, id=article_id)
            new_comment = Comment(text=text, author=request.user, article=get_article)
            new_comment.save()
            local_timezone = pytz.timezone('Europe/Moscow')
            localized_time = new_comment.date.astimezone(local_timezone)
            response_data = {
                'author': new_comment.author.username,
                'text': new_comment.text,
                'created_at': localized_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            return JsonResponse(response_data)
    else:
        return JsonResponse({'user_is_not_auth': 'Для того, чтобы оставлять комментарии, вам необходимо авторизироваться'})


def control_panel(request):
    if request.user.groups.filter(name='admin').exists():
        articles = Article.objects.filter(published=False)
        return render(request, 'control_panel.html', {'articles': articles})
    else:
        messages.error(request, 'У вас нету прав доступа к данной странице')
        return render(request, 'control_panel.html')


@require_POST
def publish_article(request, article_id):
    if request.user.groups.filter(name='admin').exists():
        article = get_object_or_404(Article, id=article_id)
        article.published = True
        article.save()
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)


@login_required
@require_POST
def del_article(request, article_id):
    if request.user.groups.filter(name='admin').exists():
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)


@login_required
@require_POST
def edit_article(request, article_id):
    if request.user.groups.filter(name='admin').exists():
        article = get_object_or_404(Article, id=article_id)
        text = request.POST.get('text')
        article.text = text
        article.save()
        article_new_text = article.text
        return JsonResponse({'article_new_text': article_new_text}, status=200)
    else:
        return JsonResponse({}, status=400)