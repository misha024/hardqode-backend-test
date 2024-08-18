from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    """
    на счет author логичнее было бы сделать ForeignKey (имхо)
    """
    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    cost = models.PositiveIntegerField(
        verbose_name="Стоимость"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE,
        verbose_name="Курс")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(max_length=255, verbose_name='Название')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    users = models.ManyToManyField(to="users.CustomUser", through="UserToGroup")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)


class UserToGroup(models.Model):
    """Модель пользователей"""
    user = models.ForeignKey(to="users.CustomUser", on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'group')
