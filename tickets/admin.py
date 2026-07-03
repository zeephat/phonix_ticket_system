from django.contrib import admin
# Hakikisha ume-import meza zote hapa, pamoja na Companies na SeatLocks
from .models import AmenityItems, Bookings, Routes, Schedules, Buses, Users, Payments, Companies, SeatLocks

admin.site.register(AmenityItems)
admin.site.register(Bookings)
admin.site.register(Routes)
admin.site.register(Schedules)
admin.site.register(Buses)
admin.site.register(Users)
admin.site.register(Payments)
admin.site.register(Companies)   # <<< Hapa sasa itaonekana Admin!
admin.site.register(SeatLocks)   # <<< Hapa na hii ya kiti kufungwa itaonekana