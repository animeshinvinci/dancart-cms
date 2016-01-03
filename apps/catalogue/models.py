from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from treebeard.mp_tree import MP_Node
from sorl.thumbnail import ImageField
from adminsortable.models import SortableMixin
import os


def get_brand_logo_path(instance, filename):
    return os.path.join("uploads/brands/%d" % instance.id, filename)


def get_product_photo_path(instance, filename):
    return os.path.join("uploads/products/%d" % instance.product.id, filename)


# Category class
class Category(MP_Node):

    class Meta:
        verbose_name_plural = _("categories")

    name = models.CharField(max_length=45)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])

    def __str__(self):
        return self.name


# Brand class
class Brand(models.Model):

    name = models.CharField(
        _('Brand name'),
        max_length=80,
        null=False,
        blank=False
    )

    logo = ImageField(
        _('Logo'),
        upload_to=get_brand_logo_path,
        null=False,
        help_text=_('Logo of this brand')
    )


# Product manager
class ProductManager(models.Manager):

    def most_popular(self):
        return self.order_by('-visits')

    def added_recently(self):
        return self.order_by('-publication_date')


# Product class
class Product(models.Model):

    objects = ProductManager()

    category = models.ForeignKey(
        Category,
        help_text=_('Category of this product')
    )
    
    name = models.CharField(
        _('Product name'),
        max_length=140,
        null=False,
        blank=False
    )

    description = models.TextField(
        _('Product description'),
        null=False,
        blank=False
    )

    publication_date = models.DateField(
        _('Publication date'),
        null=False,
        blank=False,
        auto_now_add=True,
        help_text=_('Date when this product was published.')
    )

    visits = models.PositiveIntegerField(
        _('Number of visit'),
        default=0,
        null=False,
        blank=False,
        help_text=_('Number of times this product has been visited')
    )

    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=2
    )

    slug = models.SlugField(
        _('Slug'),
        max_length=140,
        null=False,
        blank=False,
        help_text=_('A unique name to identify this product.')
    )

    related_products = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('List of related products'),
        help_text=_('Products that are related to this product.')
    )

    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse("product_details", args=[self.category.slug, self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date < now
#
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'


class Photo(SortableMixin):

    class Meta:
        ordering = ['item_order']

    product = models.ForeignKey(Product)

    description = models.CharField(
        _('Description'),
        max_length=60
    )

    item_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False
    )

    file = ImageField(
        upload_to=get_product_photo_path,
        null=False
    )