from django.db import models

from rttcore.models.models import BaseTimeStampedModel
from rttorganization.models.models import Organization
from rttproduct.models.core_models import Industry
from rttsubstance.models import Substance, SubstanceUsesAndApplication


class ProductCategory(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='media/product_category_image', blank=True, null=True)
    online = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    industry = models.ManyToManyField(Industry, blank=True, related_name='product_category_industries')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class MaterialCategory(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='media/material_category_image', blank=True, null=True)
    online = models.BooleanField(default=False)
    short_name = models.CharField(max_length=20, blank=True, null=True)

    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING, related_name='material_category_industry')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Material Categories'
        constraints = [
            models.UniqueConstraint(fields=['name', 'industry'], name='unique_material_category')
        ]

    def __str__(self):
        return self.name


class Product(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='media/product_image', blank=True, null=True)

    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='product_organization')

    material_categories = models.ManyToManyField(MaterialCategory, related_name='product_material_categories',
                                                 blank=True)
    product_categories = models.ManyToManyField(ProductCategory, related_name='product_product_categories', blank=True)
    substances = models.ManyToManyField(Substance, related_name='substances_product', blank=True)
    substance_use_and_apps = models.ManyToManyField(SubstanceUsesAndApplication, blank=True,
                                                    related_name='product_substance_use_and_apps')

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'organization'], name='unique_product_name_organization')
        ]

    def __str__(self):
        return self.name
