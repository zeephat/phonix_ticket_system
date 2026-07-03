from django.db import models

class Users(models.Model):
    class UserRoles(models.TextChoices):
        ADMIN = 'ADMIN', 'Msimamizi Mkuu (Admin)'
        OPERATOR = 'OPERATOR', 'Wakala wa Basi (Operator)'
        CUSTOMER = 'CUSTOMER', 'Abiria (Customer)'

    user_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(unique=True, max_length=20)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True  # Badili kuwa True kama unataka Django isimamie mabadiliko
        db_table = 'users'
        verbose_name_plural = "Watumiaji (Users)"

    def __str__(self):
        return f"{self.fullname} ({self.role})"


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(unique=True, max_length=100)
    license_number = models.CharField(unique=True, max_length=50)
    contact_email = models.CharField(max_length=100)
    is_verified = models.IntegerField(choices=[(1, 'Ndiyo'), (0, 'Hapana')], default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'companies'
        verbose_name_plural = "Makampuni ya Mabasi (Companies)"

    def __str__(self):
        return self.company_name


class Buses(models.Model):
    class BusTypes(models.TextChoices):
        LUXURY = 'LUXURY', 'Premium Luxury'
        SEMI_LUXURY = 'SEMI_LUXURY', 'Semi Luxury'
        ORDINARY = 'ORDINARY', 'Ordinary Class'

    bus_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    plate_number = models.CharField(unique=True, max_length=20)
    total_capacity = models.IntegerField()
    bus_type = models.CharField(max_length=11, choices=BusTypes.choices, default=BusTypes.ORDINARY)

    class Meta:
        managed = True
        db_table = 'buses'
        verbose_name_plural = "Mabasi (Buses)"

    def __str__(self):
        return f"{self.plate_number} - {self.company.company_name}"


class Routes(models.Model):
    route_id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_duration_hours = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'routes'
        verbose_name_plural = "Ruti za Safari (Routes)"

    def __str__(self):
        return f"{self.origin} ➔ {self.destination}"


class Schedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Routes, models.DO_NOTHING)
    bus = models.ForeignKey(Buses, models.DO_NOTHING)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='created_by', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'schedules'
        verbose_name_plural = "Ratiba za Safari (Schedules)"

    def __str__(self):
        return f"{self.bus.plate_number} ({self.route}) - {self.departure_time.strftime('%d/%m %H:%M')}"


class SeatLocks(models.Model):
    class LockStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active Lock'
        EXPIRED = 'EXPIRED', 'Expired Lock'
        RELEASED = 'RELEASED', 'Released'

    lock_id = models.BigAutoField(primary_key=True)
    schedule = models.ForeignKey(Schedules, models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    seat_number = models.IntegerField()
    locked_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expires_at = models.DateTimeField()
    lock_status = models.CharField(max_length=20, choices=LockStatus.choices, default=LockStatus.ACTIVE)

    class Meta:
        managed = True
        db_table = 'seat_locks'
        unique_together = (('schedule', 'seat_number', 'lock_status'),)
        verbose_name_plural = "Viti Vilivyofungwa (Seat Locks)"


class Bookings(models.Model):
    class BookingStatus(models.TextChoices):
        CONFIRMED = 'CONFIRMED', 'Imethibitishwa (Confirmed)'
        PENDING = 'PENDING', 'Inasubiri Malipo (Pending)'
        CANCELLED = 'CANCELLED', 'Imeghairishwa (Cancelled)'

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    schedule = models.ForeignKey(Schedules, models.DO_NOTHING)
    lock = models.ForeignKey(SeatLocks, models.DO_NOTHING)
    seat_number = models.IntegerField()
    final_fare = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_hash = models.CharField(unique=True, max_length=64)
    cancellation_reason = models.TextField(blank=True, null=True)
    refunded_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='refunded_by', related_name='bookings_refunded_by_set', blank=True, null=True)
    booking_status = models.CharField(max_length=9, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bookings'
        unique_together = (('schedule', 'seat_number', 'booking_status'),)
        verbose_name_plural = "Tiketi Zilizokatiwa (Bookings)"


class Payments(models.Model):
    class PaymentStatus(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Imekamilika (Completed)'
        FAILED = 'FAILED', 'Imefeli (Failed)'
        PENDING = 'PENDING', 'Inasubiri (Pending)'

    class PaymentMethods(models.TextChoices):
        MPESA = 'M-PESA', 'Vodacom M-Pesa'
        TIGOPESA = 'TIGO PESA', 'Tigo Pesa'
        AIRTELMONEY = 'AIRTEL MONEY', 'Airtel Money'
        CRDB = 'CRDB BANK', 'CRDB Bank Card'

    payment_id = models.BigAutoField(primary_key=True)
    booking = models.OneToOneField(Bookings, models.DO_NOTHING)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PaymentMethods.choices)
    transaction_reference = models.CharField(unique=True, max_length=100)
    idempotency_key = models.CharField(unique=True, max_length=255)
    raw_api_payload = models.JSONField(blank=True, null=True)
    payment_status = models.CharField(max_length=9, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'payments'
        verbose_name_plural = "Malipo (Payments)"


class AmenityItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=5, choices=[('DRINK', 'Kinywaji'), ('SNACK', 'Chakula Chepesi')])
    dietary_type = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.IntegerField(choices=[(1, 'Wazi/Active'), (0, 'Zimwa/Inactive')], default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'amenity_items'
        verbose_name_plural = "Huduma za Ndani (Amenity Items)"