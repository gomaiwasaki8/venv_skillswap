# 作成者：岩崎・古越・大和
from django.urls import path
from . import views

app_name = 'skillswap'

urlpatterns = [

    # ホーム画面
    path('', views.IndexView.as_view(), name="index"),

    # お問い合わせ
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    # お問い合わせ完了
    path('inquiry/completed', views.InquiryCompletedView.as_view(), name="inquiry-completed"),

    # ログイン後
    path('after-login/', views.AfterLoginView.as_view(), name="after-login"),

    # スキルシートの作成
    path('skillseat-create/', views.SkillseatCreateView.as_view(), name="skillseat-create"),
    # スキルシートの更新
    path('skillseat-update/<int:pk>/', views.SkillseatUpdateView.as_view(), name="skillseat-update"),

    # 言語の作成
    path('language-create/', views.LanguageCreateView.as_view(), name="language-create"),
    # 言語の更新
    path('language-update/<int:pk>/', views.LanguageUpdateView.as_view(), name="language-update"),
    # 言語の削除
    path('language-delete/<int:pk>/', views.LanguageDeleteView.as_view(), name="language-delete"),

    # マイページのプロフィール文章閲覧
    path('my-page/profile-text/', views.ProfileTextView.as_view(), name="profile-text"),
    # マイページのプロフィール文章更新
    path('my-page/profile-text-update/<int:pk>/', views.ProfileTextUpdateView.as_view(), name="profile-text-update"),

    # マイページのスキルシート閲覧
    path('my-page/skillseat-browse/', views.SkillseatBrowseView.as_view(), name="skillseat-browse"),

    # マイページのマイ講座閲覧
    path('my-page/my-course/', views.MyCourseView.as_view(), name="my-course"),
    # マイページのマイ講座作成
    path('my-page/my-course-create/', views.MyCourseCreateView.as_view(), name="my-course-create"),
    # マイページのマイ講座更新
    path('my-page/my-course-update/<int:pk>/', views.MyCourseUpdateView.as_view(), name="my-course-update"),

    # マイページでお気に入り解除
    path('mypage/favorite/<int:pk>/', views.FavoriteMypageView.as_view(), name="my-favorite"),

    # マイページの自分に来たレビュー一覧(リンク貼ってないけど使える)
    path('my-page/my-review/', views.MyReviewView.as_view(), name="my-review"),

    # 講座選択
    path('course-selection/', views.CourseSelectionView.as_view(), name="course-selection"),

    # お気に入り登録・解除
    path('favorite/<int:pk>/', views.FavoriteView.as_view(), name="favorite"),

    # 講座詳細
    path('course-detail/<int:user_id_id>/', views.CourseDetailView.as_view(), name="course-detail"),
    # 講座詳細からお気に入り
    path('course-detail/favorite-detail/<int:pk>/', views.FavoriteDetailView.as_view(), name="favorite-detail"),

    # 相手のプロフィール（プロフィール文章）閲覧
    path('others-profile/text/<int:pk>/', views.OthersProfileTextView.as_view(), name="others-profile-text"),
    # 相手のプロフィール（講座）閲覧
    path('others-profile/course/<int:user_id_id>/', views.OthersProfileCourseView.as_view(),
         name="others-profile-course"),
    # 相手のプロフィール(講座)からお気に入り
    path('others-profile/course/favorite/<int:pk>/', views.FavoriteProfileView.as_view(),
         name="favorite-profile"),
    # 相手のプロフィール（スキルシート）閲覧
    path('others-profile/skillseat/<int:user_id_id>/', views.OthersProfileSkillseatView.as_view(),
         name="others-profile-skillseat"),
    # 相手のプロフィール（レビュー）閲覧
    path('others-profile/review/<int:user_id_id>/', views.OthersProfileReviewView.as_view(), name="others-profile-review"),

    # 依頼申請
    path('request-application/<int:pk>/', views.RequestApplicationView.as_view(), name="request-application"),
    # 依頼申請済みの講座
    path('my-page/requested-course/', views.RequestedCourseView.as_view(), name="requested-course"),
    # 依頼のキャンセル
    path('my-page/requested-course-cancel/<int:pk>/', views.RequestedCourseCancelView.as_view(), name="requested-course-cancel"),

    # 受講済みの講座
    path('my-page/attendance-history/', views.AttendanceHistoryView.as_view(), name="attendance-history"),

    # お気に入りの講座一覧
    path('my-page/favorite-list/', views.FavoriteListView.as_view(), name="favorite-list"),

    # 自分で退会する
    path("my-page/my-suspension/<int:user_id_id>", views.MySuspensionView.as_view(), name="my-suspension"),

    # お知らせ（依頼）
    path('news/request-received/', views.RequestReceivedView.as_view(), name="request-received"),

    # 依頼の拒否
    path('news/request-received/rejection/<int:pk>/', views.RequestRejectionView.as_view(), name="request-rejection"),

    # お知らせ（運営から）
    path('news/management-list/', views.ManagementListView.as_view(), name="management-list"),

    # チャット
    path("chat/", views.SearchUser.as_view(), name="search_user"),
    # 依頼の許可の後チャットへ遷移（フレンド登録）
    path("addfriend/<int:user_id_id>", views.addFriend, name="addfriend"),
    # 相手とのチャット
    path("chat/<str:username>", views.get_message, name="get_message"),
    # メッセージ送信
    path('api/messages', views.UpdateMessage.as_view()),
    # メッセージの送信
    path('api/messages/<int:sender>/<int:receiver>', views.UpdateMessage.as_view()),

    # 1回目のレビュー
    path("review/<int:pk>/", views.ReviewView.as_view(), name="review"),
    # 2回目以降のレビュー更新
    path("review-update/<int:pk>/", views.ReviewUpdateView.as_view(), name="review-update"),
    # レビュー更新後の遷移
    path("reviewcompleted/", views.ReviewCompletedView.as_view(), name="review_completed"),

    # 管理者側のログイン後
    path("administrator/", views.AdministratorView.as_view(), name="administrator"),
    # 管理者側のユーザ一覧
    path("administrator/user-list/", views.UserListView.as_view(), name="user-list"),
    # 管理者側のユーザ停止
    path("administrator/user-list/suspension/<int:user_id_id>", views.SuspensionView.as_view(), name="suspension"),
    # 管理者側のユーザ復帰
    path("administrator/user-list/restoration/<int:user_id_id>", views.RestorationView.as_view(), name="restoration"),
    # 管理者側の受け取ったお問い合わせ一覧
    path("administrator/inquiry-list/", views.InquiryListView.as_view(), name="inquiry-list"),
    # 管理者側の受け取ったお問い合わせ返信済みにする
    path("administrator/inquiry-replied/<int:pk>/", views.InquiryRepiedView.as_view(), name="inquiry-replied"),
    # 管理者側の受け取ったお問い合わせ未返信にする
    path("administrator/inquiry-unreplied/<int:pk>/", views.InquiryUnrepliedView.as_view(), name="inquiry-unreplied"),
    # 管理者側のお知らせ一覧
    path("administrator/news-list/", views.NewsListView.as_view(), name="news-list"),
    # 管理者側のお知らせ作成
    path("administrator/news-create/", views.NewsCreateView.as_view(), name="news-create"),
    # 管理者側のお知らせ更新
    path("administrator/news-update/<int:pk>/", views.NewsUpdateView.as_view(), name="news-update"),
]