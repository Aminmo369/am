from django.db import models
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    #A topic the user
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "موضوع"
        verbose_name_plural = "موضوعات"

class Entry(models.Model):
    #something specific about  topic
    topic = models.ForeignKey(Topic, null=True, blank=True,on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/',null=True, blank=True)
    text = models.TextField(
        verbose_name="محتوای مقاله",
        help_text="متن کامل مقاله را اینجا بنویسید",
        default="محتوا هنوز اضافه نشده است",
        blank=True,
        null=True,
    )
    date_added = models.DateTimeField(auto_now_add=True)    
    #created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    #updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.text[:50] + ''
#############################################
class Category(models.Model):
    """دسته‌بندی اخبار"""
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class Article(models.Model):
    """مدل اخبار علمی"""
    title = models.CharField(max_length=255, verbose_name="عنوان خبر")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles", verbose_name="دسته‌بندی")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="نویسنده")
    content = models.TextField(verbose_name="متن خبر")
    image = models.ImageField(upload_to="news_images/", null=True, blank=True, verbose_name="تصویر خبر")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده؟")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "خبرنامه"
        ordering = ["-published_date"]

##################################################################

class GSMModule(models.Model):
    imei = models.CharField(
        max_length=15, 
        unique=True, 
        verbose_name="IMEI دستگاه",
        help_text="IMEI منحصر‌به‌فرد ماژول را وارد کنید."
    )
    operator = models.CharField(
        max_length=50, 
        verbose_name="نام اپراتور",
        help_text="نام اپراتور سیم‌کارت در ماژول."
    )
    signal_strength = models.IntegerField(
        verbose_name="قدرت سیگنال (dBm)",
        help_text="قدرت سیگنال بر اساس dBm."
    )
    status = models.BooleanField(
        default=True, 
        verbose_name="وضعیت فعال بودن",
        help_text="فعال/غیرفعال بودن ماژول GSM."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "ماژول GSM"
        verbose_name_plural = "ماژول‌های GSM"

    def __str__(self):
        return f"{self.imei} - {self.operator}"

class SMS(models.Model):
    gsm_module = models.ForeignKey(
        GSMModule, 
        on_delete=models.CASCADE, 
        related_name="messages",
        verbose_name="ماژول GSM مرتبط"
    )
    sender = models.CharField(
        max_length=20, 
        verbose_name="شماره فرستنده",
        help_text="شماره تلفنی که پیامک ارسال کرده است."
    )
    message = models.TextField(
        verbose_name="متن پیامک",
        help_text="محتوای پیامک دریافتی یا ارسالی."
    )
    received_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="زمان دریافت"
    )

    class Meta:
        verbose_name = "پیامک"
        verbose_name_plural = "پیامک‌ها"

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}..."

class OutgoingSMS(models.Model):
    gsm_module = models.ForeignKey(
        GSMModule, 
        on_delete=models.CASCADE, 
        related_name="sent_messages",
        verbose_name="ماژول GSM مرتبط"
        
    )
    receiver = models.CharField(
        max_length=20, 
        verbose_name="شماره گیرنده",
        help_text="شماره تلفنی که پیامک به آن ارسال شده است."
    )
    message = models.TextField(
        verbose_name="متن پیامک",
        help_text="محتوای پیامک ارسالی."
    )
    sent_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="زمان ارسال"
    )

    class Meta:
        verbose_name = "پیامک ارسالی"
        verbose_name_plural = "پیامک‌های ارسالی"

    def __str__(self):
        return f"To {self.receiver}: {self.message[:30]}..."
#################################################

from datetime import date

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField( blank=True,null=True)

    def __str__(self):
        return self.name  # نمایش نام نویسنده در پنل ادمین

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.CASCADE, related_name="books")
    published_date = models.DateField(default=date.today)  # مقدار پیش‌فرض برای جلوگیری از خطا
    price = models.DecimalField(max_digits=8, decimal_places=2)  # افزایش مقدار max_digits
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # اختیاری کردن تصویر

    def __str__(self):
        return self.title  # نمایش عنوان کتاب در پنل ادمین

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"

   
#################################################

# مدیر سفارشی برای ماشین‌های سبز
class GreenCarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(color='green')

# مدیر سفارشی برای ماشین‌های قرمز
class RedCarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(color='red')

# مدل ماشین
class Car(models.Model):
    COLOR_CHOICES = [
        ('red', 'قرمز'),
        ('green', 'سبز'),
        ('blue', 'آبی'),
        ('black', 'مشکی'),
        ('white', 'سفید'),
    ]

    name = models.CharField(max_length=100, help_text="نام ماشین را وارد کنید")
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, help_text="رنگ ماشین را انتخاب کنید")
    model_year = models.IntegerField(help_text="سال ساخت ماشین را وارد کنید")

    # مدیر پیش‌فرض
    objects = models.Manager()
    
    # مدیران سفارشی
    green_cars = GreenCarManager()
    red_cars = RedCarManager()

    def __str__(self):
        return f"{self.name} - {self.color} ({self.model_year})"
    
###########################################

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان سوال")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="توضیح سوال")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions", verbose_name="نویسنده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="سوال مربوطه")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", verbose_name="نویسنده")
    content = models.TextField(verbose_name="متن پاسخ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    def __str__(self):
        return f"پاسخ {self.author.username} به {self.question.title}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ‌ها"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name="comments", verbose_name="سوال مربوطه")
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name="comments", verbose_name="پاسخ مربوطه")
    content = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        return f"نظر {self.user.username}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, "Like"),
        (-1, "Dislike"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name="votes", verbose_name="سوال مربوطه")
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name="votes", verbose_name="پاسخ مربوطه")
    value = models.IntegerField(choices=VOTE_CHOICES, verbose_name="رأی")

    class Meta:
        unique_together = ("user", "question", "answer")  # یک کاربر نمی‌تواند دو بار رأی دهد
        verbose_name = "رأی"
        verbose_name_plural = "رأی‌ها"

    def __str__(self):
        return f"{self.user.username} رأی {self.get_value_display()} داد"

                                                     