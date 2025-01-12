# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class InventoryTable(models.Model):
    material_code = models.TextField(db_column='Material Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    material_description = models.TextField(db_column='Material Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unit = models.TextField(db_column='Unit', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    open_stock = models.TextField(db_column='Open Stock', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    material_issued = models.TextField(db_column='Material Issued', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    material_received = models.TextField(db_column='Material Received', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    closing_stock = models.TextField(db_column='Closing Stock', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prefix = models.TextField(db_column='Prefix', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    pdt = models.TextField(db_column='PDT', blank=True, null=True)  # Field name made lowercase.
    bfp = models.TextField(db_column='BFP', blank=True, null=True)  # Field name made lowercase.
    price = models.TextField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'INVENTORY_TABLE'
