from .models import Page
from django.shortcuts import get_object_or_404
from django.db.models import F
from test_task.celery import app


@app.task
def update_views_count(page_id):
    page = get_object_or_404(Page, pk=page_id)
    page_content = (page.page_videos, page.page_audios, page.page_texts)
    for content in page_content:
        if content is not None:
            content.update(F("view_counter") + 1)
