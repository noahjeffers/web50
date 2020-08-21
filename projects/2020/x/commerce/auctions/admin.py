from django.contrib import admin


from .models import User, Listing, Bids, Comments, Category

class UserAdmin(admin.ModelAdmin):
    list_display=("id","username")

class BidAdmin(admin.ModelAdmin):
    list_display=("id", "get_listing", "userID", "amount")
    def get_listing(self,obj):
        return obj.listingID.title

class ListAdmin(admin.ModelAdmin):
    list_display=("id","title","listedBy")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id", "userID", "content","get_listing")
    def get_listing(self,obj):
        return obj.listingID.title

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id", "title")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListAdmin)
admin.site.register(Bids, BidAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(Category, CategoryAdmin)