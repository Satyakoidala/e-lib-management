from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Library_Users),

admin.site.register(Issued_Books),

admin.site.register(Submitted_Books),

admin.site.register(History),

admin.site.register(Payment_View),

admin.site.register(Payment_History),

admin.site.register(Books),
