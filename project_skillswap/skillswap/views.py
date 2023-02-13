# 作成者：岩崎・古越・大和
import requests
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import *
from .models import *
from django import forms
from django.db.models import Q
import re
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
# チャット機能で利用する
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from skillswap.serializers import MessageSerializer
# ソート時
from django.db.models import F

# ログインユーザのみスキルシートを閲覧出来る
class OnlyYouSkillseat(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        skillseat = get_object_or_404(Skillseat, pk=self.kwargs['pk'])
        return self.request.user.id == skillseat.user_id_id


# ログインユーザのみ講座を閲覧出来る
class OnlyYouCourse(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return self.request.user.id == course.user_id_id


# ログインしているユーザが友達の人だけに評価できる
class OnlyYouFriends(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        friends = get_object_or_404(Friends, pk=self.kwargs['pk'])
        return self.request.user.id == friends.user_id


# ログイン前のホーム画面
class IndexView(generic.TemplateView):
    template_name = "index.html"


# ログイン後の遷移先指定
class AfterLoginView(LoginRequiredMixin, generic.View):
    def get(self, request):
        # スーパーユーザの場合管理者画面へ遷移
        if self.request.user.is_superuser:
            return redirect('skillswap:administrator')
        # プロフィールと言語を作成していた場合トップの講座選択画面へ遷移
        elif Language.objects.filter(user_id_id=self.request.user).exists() and Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:course-selection')
        # プロフィールを作成していた場合言語作成画面へ遷移
        elif Skillseat.objects.filter(user_id_id=self.request.user).exists():
            return redirect('skillswap:language-create')
        # それ以外（プロフィールも言語も作成していなかった場合）プロフィール作成画面へ遷移
        else:
            return redirect('skillswap:skillseat-create')


# アカウント情報（プロフィール）新規作成
class SkillseatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Skillseat
    template_name = "skillseat_create.html"
    form_class = SkillseatCreateForm
    success_url = reverse_lazy('skillswap:language-create')

    def form_valid(self, form):
        skillseat = form.save(commit=False)
        skillseat.user_id = self.request.user
        skillseat.save()
        return super().form_valid(form)


# 言語スキルシート作成（入力フォーム増減可能）
class LanguageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Language
    template_name = "language_create.html"
    form_class = LanguageCreateForm
    success_url = reverse_lazy('skillswap:course-selection')

    def post(self, request, *args, **kwrgs):
        # 空の配列を作ります
        genre_1List = []
        genre_2List = []
        careerList = []
        language_detailList = []

        # request.POST.items()でPOSTで送られてきた全てを取得。
        for i in request.POST.items():
            # name属性のtitle_から始まるものをtitleListに追加
            if re.match(r'genres_1_*', i[0]):
                genre_1List.append(i[1])
            if re.match(r'genres_2_*', i[0]):
                genre_2List.append(i[1])
            if re.match(r'career_*', i[0]):
                careerList.append(i[1])
            if re.match(r'language_detail_*', i[0]):
                language_detailList.append(i[1])

        # titleListの要素数分を回す
        for i in range(len(genre_1List)):
            language = Language.objects.create(
                user_id_id=self.request.user.id,
                genre_1=genre_1List[i],
                genre_2=genre_2List[i],
                career=careerList[i],
                language_detail=language_detailList[i],
            )
            language.save()
        return redirect("skillswap:course-selection")


# アカウント情報（プロフィール）の更新
class SkillseatUpdateView(LoginRequiredMixin, OnlyYouSkillseat, generic.UpdateView):
    model = Skillseat
    template_name = "skillseat_update.html"
    form_class = SkillseatUpdateForm
    success_url = reverse_lazy('skillswap:skillseat-browse')


# 言語の更新
class LanguageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Language
    template_name = "language_update.html"
    form_class = LanguageCreateForm
    success_url = reverse_lazy('skillswap:skillseat-browse')


# マイページの言語削除
class LanguageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Language
    template_name = "language_delete.html"

    def get_queryset(self):
        language = Language.objects.filter(id=self.kwargs['pk'])
        return language

    success_url = reverse_lazy('skillswap:skillseat-browse')


# マイページの言語閲覧
class SkillseatBrowseView(LoginRequiredMixin, generic.ListView):
    template_name = "skillseat_browse.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(SkillseatBrowseView, self).get_context_data(**kwargs)
        context.update({
            'language_list': Language.objects.filter(user_id_id=self.request.user).order_by('created_at'),
            'course_list': Course.objects.filter(user_id_id=self.request.user),
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 自分のプロフィール文章閲覧
class ProfileTextView(LoginRequiredMixin, generic.ListView):
    model = Skillseat
    template_name = "profile_text.html"

    def get_queryset(self):
        profile_text = Skillseat.objects.filter(user_id_id=self.request.user)
        return profile_text


# 自分のプロフィール文章の更新
class ProfileTextUpdateView(LoginRequiredMixin, OnlyYouSkillseat, generic.UpdateView):
    model = Skillseat
    template_name = "profile_text_update.html"
    form_class = ProfileTextCreateForm
    success_url = reverse_lazy('skillswap:profile-text')


# 講座選択画面と検索機能
class CourseSelectionView(generic.ListView):
    model = Course
    template_name = "course_selection.html"

    def get_context_data(self, **kwargs):
        context = super(CourseSelectionView, self).get_context_data(**kwargs)
        courses = Course.objects.select_related('user_id').filter(~Q(user_id_id=self.request.user.id))
        favorite = Favorite.objects.prefetch_related('user_id', 'course_id').values('course_id').filter(user_id_id=self.request.user.id)
        context.update({
            'course_request_list': courses, # 使ってない
            'favorite_list': favorite, # 使ってない
            'q': self.request.GET.get('q'),
        })
        return context

    def get_queryset(self, **kwargs):
        course = super().get_queryset(**kwargs)
        query = self.request.GET
        course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id))
        active = CustomUser.objects.filter(is_active=True)

        # 検索バーから抽出
        if query.get('q') == "None":
            course = course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id), user_id_id__in=active).order_by('created_at')
        elif q := query.get('q'):
            course = course.select_related('user_id').filter(Q(user_id_id__in=active), ~Q(user_id_id=self.request.user.id), Q(title__icontains=q) | Q(detail__icontains=q), )
        # 新着順
        if query.get('new'):
            return course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id), user_id_id__in=active).order_by('-created_at')
        # 投稿順
        elif query.get('old'):
            return course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id), user_id_id__in=active).order_by('created_at')
        # 人気順
        elif query.get('popular'):
            return course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id),
                                                           user_id_id__in=active).order_by(F('user_id_id__skillseat__user_evaluation').desc(nulls_last=True))
        # それ以外
        else:
            return course.select_related('user_id').filter(~Q(user_id_id=self.request.user.id), user_id_id__in=active).order_by('created_at')


# お気に入り登録(講座一覧から)
class FavoriteView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        if Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).exists():
            # お気に入りの解除
            favorite = Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).delete()
        else:
            # お気に入りの登録
            favorite = Favorite.objects.create(
                user_id_id=self.request.user.id,
                course_id_id=self.kwargs['pk'],
            )
            favorite.save()
        return redirect('skillswap:course-selection')


# お気に入り登録(マイページから)
class FavoriteMypageView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        if Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).exists():
            # お気に入りの解除
            favorite = Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).delete()
        else:
            # お気に入りの登録
            favorite = Favorite.objects.create(
                user_id_id=self.request.user.id,
                course_id_id=self.kwargs['pk'],
            )
            favorite.save()
        return redirect('skillswap:favorite-list')


# お気に入り登録(講座詳細から)
class FavoriteDetailView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        if Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).exists():
            # お気に入りの解除
            favorite = Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).delete()
        else:
            # お気に入りの登録
            favorite = Favorite.objects.create(
                user_id_id=self.request.user.id,
                course_id_id=self.kwargs['pk'],
            )
            favorite.save()
        user_id_id = Course.objects.values('user_id_id').get(pk=self.kwargs['pk'])
        return redirect('skillswap:course-detail', user_id_id=user_id_id['user_id_id'])


# お気に入り登録(相手のプロフィール講座から)
class FavoriteProfileView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        if Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).exists():
            # お気に入りの解除
            favorite = Favorite.objects.filter(user_id_id=self.request.user.id, course_id_id=self.kwargs['pk']).delete()
        else:
            # お気に入りの登録
            favorite = Favorite.objects.create(
                user_id_id=self.request.user.id,
                course_id_id=self.kwargs['pk'],
            )
            favorite.save()
        user_id_id=Course.objects.values('user_id_id').get(pk=self.kwargs['pk'])
        return redirect('skillswap:others-profile-course', user_id_id=user_id_id['user_id_id'])


# お気に入り一覧
class FavoriteListView(LoginRequiredMixin, generic.ListView):
    models = Favorite
    template_name = "favorite_list.html"

    def get_context_data(self, **kwargs):
        context = super(FavoriteListView, self).get_context_data(**kwargs)
        favorite = Favorite.objects.select_related('course_id').filter(user_id_id=self.request.user)
        skillseat = Skillseat.objects.filter(user_id_id=self.request.user)
        context.update({
            'favorite_list': favorite,
            'skillseat_list': skillseat,
        })
        return context

    def get_queryset(self):
        favorite = Favorite.objects.filter(user_id_id=self.request.user)
        return favorite


# 自分の講座の閲覧
class MyCourseView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = "my_course.html"

    def get_context_data(self, **kwargs):
        context = super(MyCourseView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.request.user),
            'course_list': Course.objects.filter(user_id_id=self.request.user).order_by('-created_at')
        })
        return context


# 自分の講座作成
class MyCourseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Course
    template_name = "my_course_create.html"
    form_class = MyCourseCreateForm
    success_url = reverse_lazy('skillswap:skillseat-browse')

    def form_valid(self, form):
        course = form.save(commit=False)
        course.user_id = self.request.user
        course.save()
        return super().form_valid(form)


# 自分の講座の更新
class MyCourseUpdateView(LoginRequiredMixin, OnlyYouCourse, generic.UpdateView):
    model = Course
    template_name = "my_course_update.html"
    form_class = MyCourseCreateForm
    success_url = reverse_lazy('skillswap:my-course')


# 自分の講座詳細画面
class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
    template_name = "course_detail.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 自分に来たレビューの閲覧
class MyReviewView(LoginRequiredMixin, generic.ListView):
    template_name = "my_review_list.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(MyReviewView, self).get_context_data(**kwargs)
        context.update({
            'review_list': Evaluation.objects.filter(user2_id_id=self.request.user)
            })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 自分で退会する
class MySuspensionView(LoginRequiredMixin, generic.TemplateView):
    template_name = "my_suspension_update.html"

    def post(self, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.kwargs['user_id_id'])
        user.is_active = False
        user.save()
        return redirect('skillswap:index')


# 他の人のプロフィール文章閲覧
class OthersProfileTextView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_text.html"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileTextView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(id=self.kwargs['pk']),
        })
        return context


# 他の人の講座閲覧
class OthersProfileCourseView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_course.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileCourseView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
            'course_list': Course.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 他の人のアカウント情報閲覧
class OthersProfileSkillseatView(generic.DetailView):
    model = Skillseat
    template_name = "others_profile_skillseat.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileSkillseatView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
            'language_list': Language.objects.filter(user_id_id=self.kwargs['user_id_id']),
        })
        return context


# 相手のプロフィール閲覧
class OthersProfileReviewView(generic.ListView):
    model = Skillseat
    template_name = "others_profile_evaluation.html"
    slug_field = "user_id_id"
    slug_url_kwarg = "user_id_id"

    def get_context_data(self, **kwargs):
        context = super(OthersProfileReviewView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.filter(user_id_id=self.kwargs['user_id_id']),
            'evaluation_list': Evaluation.objects.select_related('user1_id').filter(user2_id_id=self.kwargs['user_id_id'])
        })
        return context

    def get_queryset(self, **kwargs):
        skillseat = Skillseat.objects.select_related('user2_id').filter(user_id_id=self.kwargs['user_id_id'])
        return skillseat


# 依頼申請の作成
class RequestApplicationView(LoginRequiredMixin, generic.FormView):
    model = Request
    template_name = "request_application.html"
    form_class = RequestApplicationCreateForm
    success_url = reverse_lazy('skillswap:course-selection')

    def form_valid(self, form):

        form = RequestApplicationCreateForm(self.request.POST or None)
        if self.request.method == 'POST':
            if form.is_valid():
                receiver = Course.objects.get(pk=self.kwargs['pk'])
                Request.objects.update_or_create(user_id=self.request.user, course_id_id=self.kwargs['pk'],
                                                 receiver_id_id=receiver.user_id_id, request_completed__isnull=True,
                                                 defaults={'user_id': self.request.user,
                                                           'course_id_id': self.kwargs['pk'],
                                                           'receiver_id_id': receiver.user_id_id,
                                                           'message': self.request.POST['message']})
        return super().form_valid(form)


# 依頼申請済みの講座閲覧
class RequestedCourseView(LoginRequiredMixin, generic.ListView):
    template_name = "requested_course.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):

        context = super(RequestedCourseView, self).get_context_data(**kwargs)
        request = Request.objects.select_related('course_id').filter(user_id_id=self.request.user, request_completed__isnull=True).order_by('created_at')

        context.update({
            'request_list': request,
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 依頼のキャンセル
class RequestedCourseCancelView(LoginRequiredMixin, generic.DeleteView):
    model = Request
    template_name = "requested_course_cancel.html"
    success_url = reverse_lazy('skillswap:requested-course')


# 講座受講履歴
class AttendanceHistoryView(LoginRequiredMixin, generic.ListView):
    template_name = "attendance_history.html"
    model = Skillseat
    context_object_name = 'skillseat_list'

    def get_context_data(self, **kwargs):
        context = super(AttendanceHistoryView, self).get_context_data(**kwargs)
        request = Request.objects.select_related('course_id').filter(user_id_id=self.request.user,
                                                                     request_completed=True).order_by('created_at')
        context.update({
            'request_list': request,
        })
        return context

    def get_queryset(self):
        return Skillseat.objects.filter(user_id_id=self.request.user)


# 自分に来た依頼の閲覧
class RequestReceivedView(LoginRequiredMixin, generic.ListView):
    model = Request
    template_name = "request_received.html"

    def get_context_data(self, **kwargs):
        context = super(RequestReceivedView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.select_related('user_id').filter(
                receiver_id_id=self.request.user, request_completed__isnull=True).order_by('created_at'),
        })
        return context


# 依頼の拒否
class RequestRejectionView(LoginRequiredMixin, generic.UpdateView):
    model = Request
    template_name = "request_rejection.html"

    def get(self, request, *args, **kwargs):
        result = Request.objects.get(pk=self.kwargs['pk'])
        result.request_completed = False
        result.save()
        return redirect('skillswap:request-received')


# お問い合わせ入力画面
class InquiryView(generic.CreateView):
    model = Inquiry
    template_name = "inquiry.html"
    form_class = InquiryCreateForm
    success_url = reverse_lazy('skillswap:inquiry-completed')

    def form_valid(self, form):
        inquiry = form.save()
        inquiry.save()
        return super().form_valid(form)


# お問い合わせ完了画面
class InquiryCompletedView(generic.TemplateView):
    template_name="inquiry_completed.html"


# フレンドの取得
def getFriendsList(username):
    # 指定したユーザの友達リストを取得
    # :param: ユーザ名
    # :return: ユーザ名の友達リスト
    try:
        user = CustomUser.objects.get(username=username)
        friends = list(user.user_friends.all())
        return friends
    except:
        return []


# フレンド一覧の表示
class SearchUser(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        # 検索機能はつけていない。
        if 'search' in self.request.GET:
            query = request.GET.get("search")
            users = list(CustomUser.objects.filter(is_active=True))
            user_list = []
            for user in users:
                # 検索文字列を含むユーザ情報を取得(自分は除外)
                if query in user.username and user.username != request.user.username:
                    user_list.append(user)
        else:
            user_list = list(CustomUser.objects.filter(is_active=True))  # 全ユーザ一覧を取得
            for user in user_list:
                if user.username == request.user.username:
                    user_list.remove(user)  # 自分のユーザだけ除外
                    break

        friends = getFriendsList(request.user.username)  # 自分のフレンド一覧を取得
        return render(request, "chat/search.html", {'users': user_list, 'friends': friends})


# 許可を押した際にフレンド登録を行う
def addFriend(request, user_id_id):
    # 引数で受け取ったユーザ名(username)を Friendsテーブルに友達として登録する。
    login_user = request.user.username
    user_name = CustomUser.objects.get(pk=user_id_id)
    friend = CustomUser.objects.get(username=user_name)
    current_user = CustomUser.objects.get(username=login_user)
    friend_lists = current_user.user_friends.all()

    # 許可した場合Requestテーブルに許可した事を追加する（request_completedをTrueにする）
    result = Request.objects.get(Q(user_id=current_user, receiver_id=friend)| Q(user_id=friend, receiver_id=current_user), request_completed__isnull=True)
    result.request_completed = True
    result.save()

    #既に友達登録済みの場合flag=1にセット
    flag = 0
    for friend_list in friend_lists:
        if friend_list.friend.pk == friend.pk:
            flag = 1
            break
    #フレンド未登録の場合
    if flag == 0:
        #お互いにフレンド登録を行う。
        current_user.user_friends.create(friend=friend)  #ログオンユーザ視点でフレンドを登録
        friend.user_friends.create(friend=current_user)   #フレンド視点でログオンユーザをフレンドに登録
        # フレンドになったら取引が許可されたことをrequestテーブルに保存
        object = Request.objects.get(user_id_id=friend, receiver_id_id=current_user)
        context = {'object': object}
        object.request_completed = True
        object.save()
    return redirect("skillswap:search_user")


# チャット情報を取得
def get_message(request, username):
    # 特定ユーザ間のチャット情報を取得する
    # usernameがis_activeでなければこの処理を抜ける
    friend = CustomUser.objects.get(username=username)
    current_user = CustomUser.objects.get(username=request.user.username)
    messages = Messages.objects.filter(sender_name=current_user.id, receiver_name=friend.id) | \
               Messages.objects.filter(sender_name=friend.id, receiver_name=current_user.id)
    friends = getFriendsList(request.user.username)
    return render(request, "chat/messages.html",
                  {'messages': messages,
                   'friends': friends,
                   'current_user': current_user, 'friend': friend})


# チャットを送る
class UpdateMessage(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        sender = self.kwargs.get('sender')
        receiver = self.kwargs.get('receiver')
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        for message in messages:
            message.seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)


# 1回目のレビュー(作成)
class ReviewView(LoginRequiredMixin, OnlyYouFriends, generic.CreateView):
    model = Evaluation
    template_name = "review.html"
    form_class = EvaluationCreateForm
    success_url = reverse_lazy('skillswap:review_completed')

    def get_context_data(self, **kwargs):
        friend = Friends.objects.values('friend_id').get(pk=self.kwargs['pk'])
        context = super(ReviewView, self).get_context_data(**kwargs)
        context.update({
            'course_list': Course.objects.filter(user_id_id=friend['friend_id']),
        })
        return context

    def form_valid(self, form):
        friend = Friends.objects.values('friend_id').get(pk=self.kwargs['pk'])
        evaluation = form.save(commit=False)
        evaluation.user1_id_id = self.request.user.id
        evaluation.user2_id_id = friend['friend_id']
        evaluation.save()
        # レビューを計算して対象のユーザの平均評価を保存
        evaluation_list = Evaluation.objects.filter(user2_id_id=friend['friend_id'])
        evaluation_num = 0
        for eva in evaluation_list:
            evaluation_num += eva.evaluation_num
        # 平均の計算
        evaluation_ave = round(evaluation_num / evaluation_list.count(), 1)
        skillseat = Skillseat.objects.get(user_id_id=friend['friend_id'])
        skillseat.user_evaluation = evaluation_ave
        skillseat.save()
        # friendsテーブルにレビュー完了したかを保存
        friends = Friends.objects.get(pk=self.kwargs['pk'])
        friends.review_completed = True
        friends.save()
        return super().form_valid(form)


#2回目以降のレビュー(更新)
class ReviewUpdateView(LoginRequiredMixin, OnlyYouFriends, generic.FormView):
    model = Evaluation
    template_name = "review.html"
    form_class = EvaluationCreateForm
    success_url = reverse_lazy('skillswap:review_completed')

    def get_context_data(self, **kwargs):
        friend = Friends.objects.values('friend_id').get(pk=self.kwargs['pk'])
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        context.update({
            'course_list': Course.objects.filter(user_id_id=friend['friend_id']),
        })
        return context

    def form_valid(self, form):
        friend = Friends.objects.values('friend_id').get(pk=self.kwargs['pk'])
        evaluation = Evaluation.objects.get(user1_id_id=self.request.user.id, user2_id_id=friend['friend_id'])
        evaluation.user1_id_id = self.request.user.id
        evaluation.user2_id_id = friend['friend_id']
        evaluation.evaluation_num = self.request.POST['evaluation_num']
        evaluation.evaluation_text = self.request.POST['evaluation_text']
        evaluation.save()

        # レビューを計算して対象のユーザの平均評価を保存
        evaluation_list = Evaluation.objects.filter(user2_id_id=friend['friend_id'])
        evaluation_num = 0
        for eva in evaluation_list:
            evaluation_num += eva.evaluation_num
        # 平均の計算
        evaluation_ave = round(evaluation_num / evaluation_list.count(), 1)
        skillseat = Skillseat.objects.get(user_id_id=friend['friend_id'])
        skillseat.user_evaluation = evaluation_ave
        skillseat.save()
        # friendsテーブルにレビュー完了したかを保存
        friends = Friends.objects.get(pk=self.kwargs['pk'])
        friends.review_completed = True
        friends.save()
        return super().form_valid(form)


# レビュー完了画面
class ReviewCompletedView(LoginRequiredMixin, generic.TemplateView):
    template_name = "review_completed.html"


# 管理者ログイン後トップページ
class AdministratorView(LoginRequiredMixin, generic.TemplateView):
    template_name = "Administrator.html"


# 管理者側からユーザの一覧閲覧
class UserListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = "user_list.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update({
            'skillseat_list': Skillseat.objects.all()
        })
        return context


# 管理者側からユーザのアカウント停止処理
class SuspensionView(LoginRequiredMixin, generic.TemplateView):
    template_name = "suspension_update.html"

    def post(self, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.kwargs['user_id_id'])
        user.is_active = False
        user.save()
        return redirect('skillswap:user-list')


# 管理者側からユーザのアカウント復旧処理
class RestorationView(LoginRequiredMixin, generic.TemplateView):
    template_name = "restoration_update.html"

    def post(self, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.kwargs['user_id_id'])
        user.is_active = True
        user.save()
        return redirect('skillswap:user-list')


# 管理者側からお問い合わせ一覧
class InquiryListView(LoginRequiredMixin, generic.ListView):
    model = Inquiry
    template_name = "inquiry_list.html"

    def get_queryset(self, **kwargs):
        inquiry = super().get_queryset(**kwargs)
        query = self.request.GET

        # 返信済み
        if query.get('replied'):
            return inquiry.filter(replied=True)
        # 未返信
        elif query.get('no-reply'):
            return inquiry.filter(replied__isnull=True)
        # それ以外
        else:
            return inquiry.order_by('created_at')


# お問い合わせを返信済みにする
class InquiryRepiedView(LoginRequiredMixin, generic.UpdateView):
    model = Inquiry
    template_name = "inquiry_list.html"

    def get(self, request, *args, **kwargs):
        result = Inquiry.objects.get(pk=self.kwargs['pk'])
        result.replied = True
        result.save()
        return redirect('skillswap:inquiry-list')


# お問い合わせを未返信にする
class InquiryUnrepliedView(LoginRequiredMixin, generic.UpdateView):
    model = Inquiry
    template_name = "inquiry_list.html"

    def get(self, request, *args, **kwargs):
        result = Inquiry.objects.get(pk=self.kwargs['pk'])
        result.replied = True
        result.save()
        return redirect('skillswap:inquiry-list')


# 管理者側からお知らせ一覧
class NewsListView(LoginRequiredMixin, generic.ListView):
    model = News
    template_name = "news_list.html"


# 管理者側からお知らせを作成
class NewsCreateView(LoginRequiredMixin, generic.CreateView):
    model = News
    template_name = "news_create.html"
    form_class = NewsCreateForm
    success_url = reverse_lazy('skillswap:news-list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.reply_all = True
        news.save()
        return super().form_valid(form)


# 管理者側からお知らせの更新
class NewsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = News
    template_name = "news_update.html"
    form_class = NewsCreateForm
    success_url = reverse_lazy('skillswap:news-list')


# 運営からのお知らせ表示
class ManagementListView(LoginRequiredMixin, ListView):
    model = News
    template_name = "management_list.html"

    def get_queryset(self):
        news = News.objects.filter(Q(reply_all=True) | Q(user_id_id=self.request.user.id))
        return news

