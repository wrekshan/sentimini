from django.contrib import admin

from .models import FAQ
# Register your models here.
class FAQAdmin(admin.ModelAdmin):
	list_display = ["question","answer","category","date_created","date_updated","active"]
	list_display_links = ["question"]
	list_filter = ["category"]
	search_fields = ["question","category"]
	class Meta:
		model = FAQ

admin.site.register(FAQ,FAQAdmin)

