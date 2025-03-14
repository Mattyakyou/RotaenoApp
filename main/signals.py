from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Diff, Score

@receiver(post_save, sender=CustomUser)
def create_user_scores(sender, instance, created, **kwargs):
    if created:  # ユーザーが新規作成されたときのみ実行
        # Diffモデルの各titleを取得
        diff_titles = Diff.objects.all()

        # 各Diffのtitleに対してScoreを作成
        for diff in diff_titles:
            Score.objects.create(
                user=instance,
                title=diff.title,
                I_score=None,
                II_score=None,
                III_score=None,
                IV_score=None,
                IV_a_score=None,
            )


@receiver(post_save, sender=Diff)
def create_score_for_all_users(sender, instance, created, **kwargs):
    if created:  # Diffが新規作成されたときのみ実行
        # 全てのユーザーを取得
        users = CustomUser.objects.all()

        # 各ユーザーに新しいDiffタイトルに対するScoreを作成
        for user in users:
            Score.objects.create(
                user=user,
                title=instance.title,  # Diffの新しいtitleを使用
                I_score=None,
                II_score=None,
                III_score=None,
                IV_score=None,
                IV_a_score=None,
            )

def delete_scores_for_diff(sender, instance, **kwargs):
    # Diffのtitleに対応するScoreを削除
    Score.objects.filter(title=instance.title).delete()