from django.contrib import admin
from .models import Listing, User, Bids, Comments

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comments)
