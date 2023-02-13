# 作成者：岩崎・古越・大和
from django.db import models
# アカウントテーブルを参照するためにインポートCustomUserかAccount
from accounts.models import CustomUser
# 禁止ワードのチェック
from django.core.exceptions import ValidationError

# 禁止ワード
bad_words = [
    "死ね", "タヒね", "ﾀﾋね",
]


def validate_bad_word(value):
    for word in bad_words:
        if word in value:
            #TIPS:forループ中でもraise命令で後続の処理は実行されなくなるため、breakは不要
            raise ValidationError("不適切な単語が含まれています。", params={'value': value}, )


# スキルシートテーブル
class Skillseat(models.Model):

    user_id = models.OneToOneField(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    user_name = models.CharField(verbose_name='名前', max_length=30, validators=[validate_bad_word])
    gender = models.CharField(verbose_name='性別', max_length=5)
    birthday = models.DateField(verbose_name="生年月日", blank=True, null=True)
    user_img = models.ImageField(verbose_name='プロフィール画像', max_length=30, blank=True, null=True)
    profile_text = models.CharField(verbose_name='プロフィール文章', max_length=10000, default="よろしくお願いします", validators=[validate_bad_word])
    user_evaluation = models.FloatField(verbose_name='評価', max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Skillseat'


# 言語テーブル
class Language(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    genre_1 = models.CharField(verbose_name="ジャンル大", max_length=100, validators=[validate_bad_word])
    genre_2 = models.CharField(verbose_name="ジャンル小", max_length=100, validators=[validate_bad_word])
    career = models.CharField(verbose_name="経歴", max_length=100, blank=True, null=True, validators=[validate_bad_word])
    language_detail = models.CharField(verbose_name="詳細", max_length=500, blank=True, null=True, validators=[validate_bad_word])
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Language'


# 講座テーブル
class Course(models.Model):

    user_id = models.OneToOneField(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    title = models.CharField(verbose_name="講座タイトル", max_length=100, validators=[validate_bad_word])
    detail = models.CharField(verbose_name="講座詳細", max_length=500, validators=[validate_bad_word])
    course_img = models.ImageField(verbose_name='イメージ画像', max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Course'


# お気に入りテーブル
class Favorite(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10)
    course_id = models.ForeignKey(Course, verbose_name="講座ID", on_delete=models.PROTECT, max_length=10)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Favorite'


# 依頼テーブル
class Request(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザー送信者ID", on_delete=models.PROTECT, max_length=10, related_name="user_id")
    receiver_id = models.ForeignKey(CustomUser, verbose_name="ユーザー受信者ID", on_delete=models.PROTECT, max_length=10, related_name="receiver_id")
    course_id = models.ForeignKey(Course, verbose_name="講座ID", on_delete=models.PROTECT, max_length=10)
    message = models.CharField(verbose_name="メッセージ", max_length=500, validators=[validate_bad_word])
    request_completed = models.BooleanField(verbose_name="依頼成立", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Request'


# チャットテーブル
class Chat(models.Model):

    request_id = models.ForeignKey(Request, verbose_name="依頼ID", on_delete=models.PROTECT, max_length=10)
    user_id = models.ForeignKey(CustomUser, verbose_name="送信者ID", on_delete=models.PROTECT, max_length=10)
    message = models.CharField(verbose_name="メッセージ", max_length=500, validators=[validate_bad_word])
    file = models.FileField(verbose_name="ファイル", max_length=500, upload_to='static/files/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Chat'

    def __str__(self):
        return self.request_id


# 評価テーブル
class Evaluation(models.Model):

    user1_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー1ID", on_delete=models.PROTECT, max_length=10, related_name="user1_eva"
    )
    user2_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー2ID", on_delete=models.PROTECT, max_length=10, related_name="user2_eva"
    )
    # max_length=5
    evaluation_num = models.IntegerField(verbose_name="評価",)
    evaluation_text = models.CharField(verbose_name="レビュー文", max_length=500, blank=True, null=True, validators=[validate_bad_word])
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Evaluation'


# お問い合わせテーブル
class Inquiry(models.Model):

    email = models.CharField(verbose_name="メールアドレス", max_length=256)
    user_name = models.CharField(verbose_name="名前", max_length=500)
    inquiry_content = models.CharField(verbose_name="お問い合わせ内容", max_length=500, validators=[validate_bad_word])
    replied = models.BooleanField(verbose_name="返信の有無", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiry'


# お知らせテーブル
class News(models.Model):

    user_id = models.ForeignKey(CustomUser, verbose_name="ユーザーID", on_delete=models.PROTECT, max_length=10, blank=True, null=True)
    news_detail = models.CharField(verbose_name="お知らせ内容", max_length=500, validators=[validate_bad_word])
    reply_all = models.BooleanField(verbose_name="全員へ返信", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'News'


# ブロックテーブル
class Block(models.Model):

    user1_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー1ID", on_delete=models.PROTECT, max_length=10, related_name="user1_block"
    )
    user2_id = models.ForeignKey(
        CustomUser, verbose_name="ユーザー2ID", on_delete=models.PROTECT, max_length=10, related_name="user2_block"
    )

    class Meta:
        verbose_name_plural = 'Block'


# フレンドテーブル
class Friends(models.Model):
    class Meta:
        verbose_name = '友達リスト'
        verbose_name_plural = '友達リスト'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_friends")
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="友達", related_name="friend_friends")
    review_completed = models.BooleanField(verbose_name="レビュー完了", blank=True, null=True)

    def __str__(self):
        return f"{self.friend}"


# チャットのメッセージテーブル
class Messages(models.Model):
    description = models.TextField(validators=[validate_bad_word])
    sender_name = models.ForeignKey(CustomUser, verbose_name="送信者", on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(CustomUser, verbose_name="受信者", on_delete=models.CASCADE,
                                      related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)
        verbose_name = 'メッセージリスト'
        verbose_name_plural = 'メッセージリスト'

