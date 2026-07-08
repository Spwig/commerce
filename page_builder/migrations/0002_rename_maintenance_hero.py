"""
Data migration to rename the maintenance page hero element from name='' to
name='Maintenance Hero', and fix the zh_hans translation key to zh-hans.
"""
from django.db import migrations


def rename_maintenance_hero(apps, schema_editor):
    Page = apps.get_model('page_builder', 'Page')
    Element = apps.get_model('page_builder', 'Element')

    try:
        page = Page.objects.get(slug='maintenance')
    except Page.DoesNotExist:
        return

    updated = Element.objects.filter(
        page=page, element_type='hero', name=''
    ).update(name='Maintenance Hero')

    if updated:
        # Fix zh_hans -> zh-hans key in translations if present
        for element in Element.objects.filter(
            page=page, element_type='hero', name='Maintenance Hero'
        ):
            if element.translations and 'zh_hans' in element.translations:
                element.translations['zh-hans'] = element.translations.pop('zh_hans')
                element.save(update_fields=['translations'])


def reverse_rename(apps, schema_editor):
    Page = apps.get_model('page_builder', 'Page')
    Element = apps.get_model('page_builder', 'Element')

    try:
        page = Page.objects.get(slug='maintenance')
    except Page.DoesNotExist:
        return

    Element.objects.filter(
        page=page, element_type='hero', name='Maintenance Hero'
    ).update(name='')


class Migration(migrations.Migration):

    dependencies = [
        ('page_builder', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(rename_maintenance_hero, reverse_rename),
    ]
