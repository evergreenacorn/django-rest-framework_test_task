from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.functional import empty
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    _, Page, ContentTypeVideo,
    ContentTypeAudio, ContentTypeText
)


# Register your models here.
admin.site.site_header = _("TEST TASK Admin")
admin.site.site_title = _("TEST TASK Admin Portal")
admin.site.index_title = _("Welcome to the admin panel of the TEST TASK project!")


class AbstractInline(admin.TabularInline):
    model = None
    ordering = ("pk", "serial_number")
    readonly_fields = ("view_counter",)
    extra = 1


class VideoInline(AbstractInline):
    model = ContentTypeVideo


class AudioInline(AbstractInline):
    model = ContentTypeAudio


class TextInline(AbstractInline):
    model = ContentTypeText


class PageAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (_("Common page options"),  {
            "fields": ("title", "slug")
        }),
    )
    inlines = (
        VideoInline,
        AudioInline,
        TextInline
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    empty_value_display = "???"
    list_per_page = 20


class AbstractContentAdmin(SimpleHistoryAdmin):
    search_fields = ("title",)
    readonly_fields = ("view_counter",)
    list_per_page = 20


class VideoContentAdmin(AbstractContentAdmin):
    pass


class AudioContentAdmin(AbstractContentAdmin):
    pass


class TextContentAdmin(AbstractContentAdmin):
    search_fields = ("title", "^text")


zipped_tuples = zip(
    (
        Page,
        ContentTypeVideo,
        ContentTypeAudio,
        ContentTypeText
    ),
    (
        PageAdmin,
        VideoContentAdmin,
        AudioContentAdmin,
        TextContentAdmin
    )
)
for model, admin_model in zipped_tuples:
    admin.site.register(model, admin_class=admin_model)

admin.site.unregister(User)
admin.site.unregister(Group)
