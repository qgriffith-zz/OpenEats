# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.frontpage'
        db.add_column('news_entry', 'frontpage', self.gf('django.db.models.fields.BooleanField')(default=False, unique=True), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'Entry.frontpage'
        db.delete_column('news_entry', 'frontpage')

    models = {
        'news.entry': {
            'Meta': {'object_name': 'Entry'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['news']
