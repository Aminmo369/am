from django.contrib import admin

# Register your models here.
from .models import Topic , Entry ,Author, Book ,  GSMModule, SMS, OutgoingSMS,Car
from .models import Category, Article

admin.site.register(Topic)
admin.site.register(Entry)


####################

admin.site.register(GSMModule)
admin.site.register(SMS)
admin.site.register(OutgoingSMS)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Car)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "published_date", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}



from .models import Question, Answer, Comment, Vote

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "created_at")
    search_fields = ("question__title", "author__username")
    list_filter = ("created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at")
    search_fields = ("user__username", "content")
    list_filter = ("created_at",)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "answer", "value")
    list_filter = ("value",)
    search_fields = ("user__username", "question__title", "answer__content")
