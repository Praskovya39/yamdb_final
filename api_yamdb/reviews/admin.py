from django.contrib import admin

from reviews.models import Title, Category, Genre, Review, Comment


class TitleAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('genre', 'category',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):

    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
