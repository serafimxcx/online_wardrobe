from django.contrib import admin
from .models import UserAccount, ItemColor, ItemStyle, ItemCategory, ItemSubcategory, BodyShape, UserProfile, FashionItem, UserItem, UserOutfit, OutfitPlan, Wishlist

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(ItemColor)
admin.site.register(ItemStyle)
admin.site.register(ItemCategory)
admin.site.register(ItemSubcategory)
admin.site.register(BodyShape)
admin.site.register(UserProfile)
admin.site.register(FashionItem)
admin.site.register(UserItem)
admin.site.register(UserOutfit)
admin.site.register(OutfitPlan)
admin.site.register(Wishlist)