from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from simple_history import register
from datetime import datetime
from django.db import models
# from django.db.models import Q, CheckConstraint


CONTENTTYPES_DIRS = {
    "video_file": "contenttypes/video/files/local/%Y/%m/%d/"
    ,
    "video_subtitles": "contenttypes/video_subtitles/files/local/%Y/%m/%d/"
    ,
    "audio_file": "contenttypes/audio/files/local/%Y/%m/%d/"
}


class ViewInfo(models.Model):  # Abstract
    """Абстрактная модель
    Информация о просмотрах

    Аргументы:
        view_counter (IntegerField): Кол-во просмотров
    """
    title = models.CharField(_("Title"), max_length=160)
    view_counter = models.PositiveIntegerField(_("Number of views"), default=0)

    class Meta:
        abstract = True


class ContenttypeSpecialOrder(models.Model):  # Abstract
    """Абстрактная модель для _ContentType - моделей
    для возможности назначения порядкового номера
    записи по умолчанию.

    Аргументы:
        serial_number (IntegerField): Порядковый номер
    """
    serial_number = models.PositiveIntegerField(_("Serial number"))

    class Meta:
        abstract = True


class Page(models.Model):
    """
    Модель Страница
    Аргументы:
        slug (SlugField(160)):  Слаг-поле
    """
    title = models.CharField(
        _("Title"),
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        unique_together = ('slug', 'title')

    def __str__(self):
        return "%s: %s" % (self.pk, self.title)


class ContentTypeVideo(ViewInfo, ContenttypeSpecialOrder):
    """
    Модель Контент типа видео

    Аргументы:
        ModelInfo ([type]): [description]
        ViewInfo ([type]): [description]
    """
    # video_id = models.AutoField(primary_key=True)
    video_file_path = models.FileField(
        _("Local video file"),
        upload_to=CONTENTTYPES_DIRS["video_file"],
        null=True,
        blank=True
    )
    video_file_link = models.URLField(
        _("Remote video file"),
        max_length=500,
        null=True,
        blank=True
    )
    subtitles_file_path = models.FileField(
        _("Local subtitles file"),
        upload_to=CONTENTTYPES_DIRS["video_subtitles"],
        null=True,
        blank=True
    )
    subtitles_file_link = models.URLField(
        _("Remote subtitles file"),
        max_length=500,
        null=True,
        blank=True
    )
    page = models.ForeignKey(
        Page,
        related_name="page_videos",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        # constraints = [
        #     CheckConstraint(
        #         check=Q(video_file_path__isnull=False) | \
        #         Q(video_file_link__isnull=False),
        #         name="not_both_null_video_links"
        #     ),
        #     CheckConstraint(
        #         check=Q(video_file_path__isnull=True) | \
        #         Q(video_file_link__isnull=True),
        #         name="not_both_video_links"
        #     ),
        #     CheckConstraint(
        #         check=Q(subtitles_file_path__isnull=True) | \
        #         Q(subtitles_file_link__isnull=True),
        #         name="not_both_subtitles_links"
        #     ),
        # ]
        verbose_name = _("Content type video")
        verbose_name_plural = _("Content types video")

    def __str__(self):
        return '%s: %s' % (self.pk, self.title)

    def clean(self):
        super().clean()
        if (
            self.video_file_path is None and
            self.video_file_link is None
        ):
            raise ValidationError(_("On of the video_file_ field must not be empty."))


class ContentTypeAudio(ViewInfo, ContenttypeSpecialOrder):
    """
    Модель Контент типа аудио

    Аргументы:
        file_local_path (FileField): ссылка на локальный файл
        file_link (URLField):        ссылка на удаленный файл
        bitrate (IntegerField):      битрейт кб/с
        page (ForeignKey):           ссылка на запись страницы
    """
    file_local_path = models.FileField(
        _("Local audio file"),
        upload_to=CONTENTTYPES_DIRS["audio_file"],
        null=True,
        blank=True
    )
    file_link = models.URLField(
        _("Remote audio file"),
        max_length=500,
        null=True,
        blank=True
    )
    bitrate = models.IntegerField(
        _("Bits in a second"),
        null=False,
        blank=False
    )
    page = models.ForeignKey(
        Page,
        related_name="page_audios",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        # constraints = [
        #     CheckConstraint(
        #         check=Q(file_local_path__isnull=False) | \
        #         Q(file_link__isnull=False),
        #         name="not_both_null_audio_links"
        #     ),
        #     CheckConstraint(
        #         check=Q(file_local_path__isnull=True) | \
        #         Q(file_link__isnull=True),
        #         name="not_both_audio_links"
        #     ),
        # ]
        verbose_name = _("Content type audio")
        verbose_name_plural = _("Content types audio")

    def __str__(self):
        return '%s: %s' % (self.pk, self.title)

    def clean(self):
        # super().clean()
        if self.file_link is None and self.file_local_path is None:
            raise ValidationError(_("One of the file link fields must be not empty."))


class ContentTypeText(ViewInfo, ContenttypeSpecialOrder):
    """
    Модель Контент типа текст

    Аргументы:
        text (TextField):   текстовое поле
        page (ForeignKey):  ссылка на запись страницы
    """
    text = models.TextField(_("Text field"))
    page = models.ForeignKey(
        Page,
        related_name="page_texts",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Content type text")
        verbose_name_plural = _("Content types text")

    def __str__(self):
        return '%s: %s' % (self.pk, self.title)

    def save(self, *args, **kwargs):
        super(ContentTypeText, self).save(*args, **kwargs)


for model in (
    Page, ContentTypeVideo,
    ContentTypeAudio, ContentTypeText
):
    register(model)
