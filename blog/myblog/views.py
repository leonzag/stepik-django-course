from django.contrib.auth import authenticate, login
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from taggit.models import Tag

from blog.settings import EMAIL_HOST_USER

from .forms import CommentForm, FeedBackForm, SignInForm, SignUpForm
from .models import Comment, Post


class MainView(View):
    """
    Главная страница
    """

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-id")  # по убыванию (от новых к старым)
        paginator = Paginator(posts, 6)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "home.html", context={"page_obj": page_obj})


class PostDetailView(View):
    """
    Страница поста
    """

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tags.most_common()
        last_posts = Post.objects.all().order_by("-id")[:5]
        return render(
            request,
            "post_detail.html",
            context={
                "post": post,
                "common_tags": common_tags,
                "last_posts": last_posts,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        if (comment_form := CommentForm(request.POST)).is_valid():
            text = request.POST["text"]
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(post=post, username=username, text=text)
            return redirect(request.META.get("HTTP_REFERER", "/"))
        return render(
            request, "post_detail.html", context={"comment_form": comment_form}
        )


class TagView(View):
    """
    Страница постов по тегу
    """

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tags=tag)
        common_tags = Post.tags.most_common()
        return render(
            request,
            "tag.html",
            context={
                "title": f"#Тег: {tag}",
                "posts": posts,
                "common_tags": common_tags,
            },
        )


class SearchResaultsView(View):
    """
    Страница поиска и его результатов
    """

    def get(self, request, *args, **kwargs):
        results = []
        if query := request.GET.get("q"):
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "search.html",
            context={"title": "Поиск", "results": page_obj, "count": page_obj.count},
        )


class SignUpView(View):
    """
    Страница решистрации
    """

    def get(self, request, *args, **kwargs):
        return render(request, "signup.html", context={"form": SignUpForm()})

    def post(self, request, *args, **kwargs):
        if (form := SignUpForm(request.POST)).is_valid() and (user := form.save()):
            login(request, user)
            return redirect("index", permanent=True)
        return render(request, "signup.html", context={"form": form})


class SignInView(View):
    """
    Страница входы
    """

    def get(self, request, *args, **kwargs):
        return render(request, "signin.html", context={"form": SignInForm()})

    def post(self, request, *args, **kwargs):
        if (form := SignInForm(request.POST)).is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                return redirect("index")

        return render(request, "signin.html", context={"form": form})


class FeedBackView(View):
    """
    Страница Обратной Связи
    """

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "contact.html",
            context={"form": FeedBackForm(), "title": "Обратная связь"},
        )

    def post(self, request, *args, **kwargs):
        if (form := FeedBackForm(request.POST)).is_valid():
            name = form.cleaned_data["name"]
            from_email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    f"От {name} | {subject}",
                    message,
                    from_email,
                    [f"{EMAIL_HOST_USER}"],
                )
            except BadHeaderError:
                return HttpResponse("Невалидный заголовок")
            return redirect("success", permanent=True)

        return render(request, "contact.html", context={"form": form})


class SuccessView(View):
    """
    Страница, показывающая успех некоторого действия
    """

    def get(self, request, *args, **kwargs):
        return render(request, "success.html", context={"title": "Спасибо"})
