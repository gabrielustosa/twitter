from django.db import models


class Action(models.IntegerChoices):
    RETWEET = 1
    LIKE = 2
    COMMENT = 3
