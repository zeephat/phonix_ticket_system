import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Schedules, Routes, SeatLocks, Bookings, Payments, Users

def simu_ya_sms_gateway(phone, message):
    """
    Hapa ndipo utakapo weka kodi yako ya kuunganisha na NextSMS, Beem, au Twilio.
    Kwa sasa inaishia kwenye terminal (print) kama kumbukumbu.
    """
    print(s_msg := f"--- SMS IMETUMWA KWENDA {phone} ---")
    print(message)
    print("-" * 40)
    return True

def tafuta_mabasi_view(request):
    """
    View inayoshughulikia kuonyesha ukurasa wa nyumbani na fomu ya kutafuta mabasi.
    Inachukua data za maeneo ya kutoka na kwenda ili kuzionyesha kwenye dropdowns.
    """
    # Hapa tunavuta maeneo yote yaliyopo kwenye database kwa ajili ya fomu ya utafutaji
    maeneo_kutoka = Routes.objects.values_list('origin', flat=True).distinct()
    maeneo_kwenda = Routes.objects.values_list('destination', flat=True).distinct()
    
    # Kupokea vigezo vya utafutaji kutoka kwenye GET request (kama vipo)
    chaguzi_kutoka = request.GET.get('kutoka', '')
    chaguzi_kwenda = request.GET.get('kwenda', '')
    chaguzi_tarehe = request.GET.get('tarehe', '')
    
    # Kuanza kuchuja ratiba za safari kulingana na alichochagua mtumiaji
    ratiba_za_safari = Schedules.objects.all()
    
    if chaguzi_kutoka:
        ratiba_za_safari = ratiba_za_safari.filter(route__origin=chaguzi_kutoka)
    if chaguzi_kwenda:
        ratiba_za_safari = ratiba_za_safari.filter(route__destination=chaguzi_kwenda)
    if chaguzi_tarehe:
        ratiba_za_safari = ratiba_za_safari.filter(departure_time__date=chaguzi_tarehe)
        
    context = {
        'maeneo_kutoka': maeneo_kutoka,
        'maeneo_kwenda': maeneo_kwenda,
        'chaguzi_kutoka': chaguzi_kutoka,
        'chaguzi_kwenda': chaguzi_kwenda,
        'chaguzi_tarehe': chaguzi_tarehe,
        'ratiba_za_safari': ratiba_za_safari,
    }
    
    return render(request, 'tickets/orodha_mabasi.html', context)

@csrf_exempt
def kamilisha_malipo_api(request):
    """API Endpoint inayopokea malipo, inasave na kutuma SMS bila kuonyesha tiketi hadharani"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('schedule_id')
            fullname = data.get('fullname')
            phone = data.get('phone')
            network = data.get('network')
            viti_list = data.get('seats', [])

            if not viti_list or not schedule_id:
                return JsonResponse({'status': 'failed', 'message': 'Vigezo havijakamilika'}, status=400)

            schedule = Schedules.objects.get(pk=schedule_id)
            
            user, _ = Users.objects.get_or_create(
                phone=phone,
                defaults={
                    'fullname': fullname,
                    'email': f"{phone}@phoenix.com",
                    'password_hash': 'pbkdf2_sha256_placeholder',
                    'role': 'CUSTOMER'
                }
            )

            viti_vya_sms = []
            
            for seat_str in viti_list:
                seat_no = int(seat_str)
                
                lock = SeatLocks.objects.create(
                    schedule=schedule,
                    user=user,
                    seat_number=seat_no,
                    expires_at=timezone.now() + timezone.timedelta(minutes=10),
                    lock_status='ACTIVE'
                )

                ticket_hash = uuid.uuid4().hex
                booking = Bookings.objects.create(
                    user=user,
                    schedule=schedule,
                    lock=lock,
                    seat_number=seat_no,
                    final_fare=schedule.base_price,
                    ticket_hash=ticket_hash,
                    booking_status='CONFIRMED'
                )

                Payments.objects.create(
                    booking=booking,
                    amount_paid=schedule.base_price,
                    payment_method=network.upper(),
                    transaction_reference=f"TXN-{uuid.uuid4().hex[:8].upper()}",
                    idempotency_key=uuid.uuid4().hex,
                    payment_status='COMPLETED',
                    paid_at=timezone.now()
                )
                
                viti_vya_sms.append(f"Kiti: {seat_str} (Ref: PHX-{booking.booking_id})")

            # --- UTENGENEZAJI WA SMS YA SIRI ---
            sms_body = (
                f"Ndugu {fullname}, Tiketi yako ya Phoenix imethibitishwa kikamilifu! "
                f"Basi: {schedule.bus.company.company_name} ({schedule.bus.plate_number}). "
                f"Safari: {schedule.route.origin} -> {schedule.route.destination}. "
                f"Muda: {schedule.departure_time.strftime('%Y-%m-%d %H:%M')}. "
                f"Viti vyako: {', '.join(viti_vya_sms)}. Ahsante kwa kuchagua Phoenix!"
            )
            
            # Tuma SMS kwenda kwenye namba ya simu ya mteja
            simu_ya_sms_gateway(phone, sms_body)

            return JsonResponse({
                'status': 'success',
                'message': 'Unyama umekamilika! Tiketi imehifadhiwa kwenye database na kutumwa kwa SMS.',
                'passenger': fullname
            })

        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'failed', 'message': 'Njia Haikubaliki'}, status=405)