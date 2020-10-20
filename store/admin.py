from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from store.models import *


class LotAdmin(admin.ModelAdmin):
	list_display = ('id', 'tech_name', 'status', "date_created", "premium", "price")
	list_display_links = ("tech_name", )
	list_select_related = True
	list_editable = ('status', 'premium', "price")
	list_filter = ('status', 'premium', 'date_created')
	ordering = ('-date_created',)
	search_fields = ("tech_name", )
	filter_horizontal = ('character', 'weapons', 'stock', 'barrel', 'muzzle', 'mag', 'scope', 'grip')
	fieldsets = (
		(None, {'fields': ('tech_name', 'status', ('premium', 'price'), 'date_created')}),
		(_("Collection"), {'fields': ('character', 'weapons', 'stock', 'barrel', 'muzzle', 'mag', 'scope', 'grip')})
	)


class UserLotAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'lot', 'date_purchased')
	list_display_links = ('id', )
	list_filter = ('lot', )
	search_fields = ('user', 'lot')
	readonly_fields = ('date_purchased', 'user', 'lot')
	ordering = ('-date_purchased',)


admin.site.register(Lot, LotAdmin)
admin.site.register(UserLots, UserLotAdmin)
