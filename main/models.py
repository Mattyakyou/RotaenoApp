from django.db import models

from django.core.validators import MaxValueValidator

from django.contrib.auth.models import User

# Create your models here.

class Diff(models.Model):
    title = models.CharField(
        max_length=100
    )
    I_diff = models.DecimalField(
        max_digits=3, decimal_places=1
    )
    II_diff = models.DecimalField(
        max_digits=3, decimal_places=1
    )
    III_diff = models.DecimalField(
        max_digits=3, decimal_places=1
    )
    IV_diff = models.DecimalField(
        max_digits=3, decimal_places=1
    )
    IV_a_diff = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        s = "<diff " + \
        "ID=" + str(self.id) + " " + \
        "title=" + str(self.title) + " " + \
        "I_diff=" + str(self.I_diff) + " " + \
        "II_diff=" + str(self.II_diff) + " " + \
        "III_diff=" + str(self.III_diff) + " " + \
        "IV_diff=" + str(self.IV_diff) + " " + \
        "IV_a_diff=" + str(self.IV_a_diff) + " " + \
        ">"
        return s

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(
        max_length=100
    )

    I_score = models.PositiveIntegerField(
        default = None, null=True, blank=True, validators=[MaxValueValidator(1010000)]
    )
    II_score = models.PositiveIntegerField(
        default = None, null=True, blank=True, validators=[MaxValueValidator(1010000)]
    )
    III_score = models.PositiveIntegerField(
        default = None, null=True, blank=True, validators=[MaxValueValidator(1010000)]
    )
    IV_score = models.PositiveIntegerField(
        default = None, null=True, blank=True, validators=[MaxValueValidator(1010000)]
    )
    IV_a_score = models.PositiveIntegerField(
        default = None, null=True, blank=True, validators=[MaxValueValidator(1010000)]
    )

    I_clear = models.BooleanField(
        default=False
    )
    II_clear = models.BooleanField(
        default=False
    )
    III_clear = models.BooleanField(
        default=False
    )
    IV_clear = models.BooleanField(
        default=False
    )
    IV_a_clear = models.BooleanField(
        default=False
    )

    I_fc = models.BooleanField(
        default=False
    )
    II_fc = models.BooleanField(
        default=False
    )
    III_fc = models.BooleanField(
        default=False
    )
    IV_fc = models.BooleanField(
        default=False
    )
    IV_a_fc = models.BooleanField(
        default=False
    )

    I_ap = models.BooleanField(
        default=False
    )
    II_ap = models.BooleanField(
        default=False
    )
    III_ap = models.BooleanField(
        default=False
    )
    IV_ap = models.BooleanField(
        default=False
    )
    IV_a_ap = models.BooleanField(
        default=False
    )

    def __str__(self):
        s = f"<score user={self.user.username} ID={self.id} title={self.title} " + \
            f"I_score={self.I_score} II_score={self.II_score} " + \
            f"III_score={self.III_score} IV_score={self.IV_score} IV_a_score={self.IV_a_score} " + \
            f"I_clear={'Active' if self.I_clear else 'Inactive'} " + \
            f"II_clear={'Active' if self.II_clear else 'Inactive'} " + \
            f"III_clear={'Active' if self.III_clear else 'Inactive'} " + \
            f"IV_clear={'Active' if self.IV_clear else 'Inactive'} " + \
            f"IV_a_clear={'Active' if self.IV_a_clear else 'Inactive'} " + \
            f"I_fc={'Active' if self.I_fc else 'Inactive'} " + \
            f"II_fc={'Active' if self.II_fc else 'Inactive'} " + \
            f"III_fc={'Active' if self.III_fc else 'Inactive'} " + \
            f"IV_fc={'Active' if self.IV_fc else 'Inactive'} " + \
            f"IV_a_fc={'Active' if self.IV_a_fc else 'Inactive'} " + \
            f"I_ap={'Active' if self.I_ap else 'Inactive'} " + \
            f"II_ap={'Active' if self.II_ap else 'Inactive'} " + \
            f"III_ap={'Active' if self.III_ap else 'Inactive'} " + \
            f"IV_ap={'Active' if self.IV_ap else 'Inactive'} " + \
            f"IV_a_ap={'Active' if self.IV_a_ap else 'Inactive'} >"
        return s

class User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(
        default="aaa",
        max_length=255
    )

    def __str__(self):
        s = f"<User user={self.user.username} " + \
            f"text={self.text} >"
        return s
