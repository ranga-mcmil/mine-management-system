from django.contrib import admin
from .models import Claim, Proof, Payment, AnnualInspection, User
from django.contrib.auth.admin import UserAdmin



# # Register your models here.
# @admin.register(Mine)
# class MineAdmin(admin.ModelAdmin):
#    list_display = ('user', 'name', 'created')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
   list_display = ('applicant', 'address', 'size_approximation', 'date_applied', 'status', 'created')


@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_by', 'is_processeed', 'created')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'reason', 'user', 'proof', 'is_processeed', 'created')


@admin.register(AnnualInspection)
class AnnualInspectionAdmin(admin.ModelAdmin):
    list_display = ('claim', 'condition', 'desicion', )


