# 作成者：岩崎・古越
import os
from django import forms
from django.core.mail import EmailMessage
from .models import Skillseat, Language, Course, Favorite, Request, Chat, Evaluation, Inquiry, News, Block
import datetime


# 一番初めのプロフィール作成
class SkillseatCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_img', 'user_name', 'gender', 'birthday', 'profile_text', )

    # 入力時プルダウンリストになるよう変更
    gender = forms.fields.ChoiceField(choices=(('男', '男'), ('女', '女'), ('その他', 'その他')), label='性別', required=True,)
    # 入力時カレンダーになるよう変更
    birthday = forms.fields.DateField(label="生年月日", widget=forms.DateInput(attrs={"type": "date", "min": "1500-04-01", "max": datetime.date.today(), "value": datetime.date.today()}))

    # プロフィール文章をテキストエリアに変更
    widgets = {
        'profile_text': forms.Textarea(
            attrs={'rows': 10, 'cols': 30}
        ),
    }

    # CSSを利用できるようにする
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# プロフィールの更新
class SkillseatUpdateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('user_img', 'user_name', 'gender', 'birthday', )

    # 入力時プルダウンリストになるよう変更
    gender = forms.fields.ChoiceField(choices=(('男', '男'), ('女', '女'), ('その他', 'その他')), label='性別', required=True,)
    # 入力時カレンダーになるよう変更
    birthday = forms.fields.DateField(label="生年月日", widget=forms.DateInput(attrs={"type": "date", "min": "1500-04-01", "max": datetime.date.today(), "value": datetime.date.today()}))

    # CSSを利用できるようにする
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# プロフィールの文章の更新
class ProfileTextCreateForm(forms.ModelForm):
    class Meta:
        model = Skillseat
        fields = ('profile_text',)

        # プロフィールの文章をテキストエリアに変更
        widgets = {
            'profile_text': forms.Textarea(
                attrs={'rows': 10, 'cols': 30}
            ),
        }


# name属性を適用
FIELD_NAME_MAPPING = {
        # 'Modelクラスのフィールド名' : 'name属性の値'
        'genre_1': 'genres_1_0',
        'genre_2': 'genres_2_0',
        'career': 'career_0',
        'language_detail': 'language_detail_0',
        'evaluation_num': 'evaluation_num',
        'evaluation_text': 'evaluation_text',
    }


# 言語作成
class LanguageCreateForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('genre_1', 'genre_2', 'career', 'language_detail')

        # テキストエリアの高さ、幅を指定
        widgets = {
            'genre_1': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）OS", 'id': "genres_1_0", }
            ),
            'genre_2': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）Linux", 'id': "genres_2_0", }
            ),
            'career': forms.TextInput(
                attrs={'rows': 1, 'cols': 15, 'placeholder': "例）x年xか月", 'id': "career_0", }
            ),
            'language_detail': forms.Textarea(
                attrs={'rows': 1, 'cols': 30, 'placeholder': "例）環境設計・構築が可能",
                       'id': "language_detail_0",
                       }),
        }

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(LanguageCreateForm, self).add_prefix(field_name)


# マイ講座作成
class MyCourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'detail', 'course_img',)

        # テキストエリアの高さ、幅を指定
        widgets = {
            'detail': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


# 依頼申請文作成
class RequestApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('message',)

        # テキストエリアの高さ、幅を指定
        widgets = {
            'message': forms.Textarea(attrs={'rows': 15, 'cols': 40}),
        }


# 評価作成
class EvaluationCreateForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ('evaluation_num', 'evaluation_text',)

        # テキストエリアの高さ、幅を指定
        widgets = {
            'evaluation_text': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }

    # 入力時プルダウンリストになるよう変更
    evaluation_num = forms.fields.ChoiceField(choices=((1, '★☆☆☆☆ 星1'), (2, '★★☆☆☆ 星2'), (3, '★★★☆☆ 星3'),
                                                       (4, '★★★★☆ 星4'), (5, '★★★★★ 星5')), label='評価', required=True, )


# お問い合わせ作成
class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('user_name', 'email', 'inquiry_content',)

        # テキストエリアの高さ、幅を指定
        widgets = {
            'user_name': forms.TextInput(attrs={'rows': 1, 'cols': 40}),
            'email': forms.TextInput(attrs={'rows': 1, 'cols': 40}),
            'inquiry_content': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }


# 管理者側からお知らせの作成
class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('news_detail',)

        # テキストエリアの高さ、幅を指定
        widgets = {
            'news_detail': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }

