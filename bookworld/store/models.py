from django.db import models
from django.forms import IntegerField
from category . models import Category
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator
# from django_extensions.db.fields import AutoSlugField
# Create your models here.

class Product(models.Model):
    book_name = models.CharField(max_length=200,unique = True)
    # slug      = models.SlugField(unique = True,blank=True)
    author = models.CharField(max_length=50)
    description =  models.TextField(max_length=500,blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to = 'photos/book',validators=[FileExtensionValidator(allowed_extensions=["jpg","jpeg","webp"])])
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_count = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    is_active = models.BooleanField(default=False)
    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.book_name