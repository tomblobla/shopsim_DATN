from django.db import models
from ckeditor.fields import RichTextField


class Topic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tên chủ đề')
    slug = models.SlugField(unique=True, verbose_name='Đường dẫn đẹp')
    desc = models.TextField(verbose_name='Mô tả', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Chủ đề'
        verbose_name_plural = 'Danh sách chủ đề'

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    short_desc = models.CharField(max_length=500, verbose_name='Mô tả ngắn')
    thumbnail = models.ImageField(upload_to='images/', verbose_name='Hình ảnh minh họa')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts', verbose_name='Chủ đề')
    slug = models.SlugField(unique=True, verbose_name='Đường dẫn đẹp')
    content = RichTextField(verbose_name='Nội dung')
    is_pinned = models.BooleanField(default=False, verbose_name='Ghim')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Danh sách bài viết'
