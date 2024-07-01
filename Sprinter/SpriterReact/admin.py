from django.contrib import admin
from .models import *
admin.site.register([AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, AuthUserGroups, AuthUserUserPermissions,
                     Commentary, DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession, Post,
                     PostTag, SpUser, Tag])
