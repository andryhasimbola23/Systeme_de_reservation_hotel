from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.offline as opy
from django.db.models import Count, Avg, Q
import json

# Import des modèles
from accounts.models import User
from hotels.models import Hotel, RoomType, HotelImage
from bookings.models import Booking, Payment, CancellationPolicy

# ==================== VUES PUBLIQUES ====================

def home(request):
    """Page d'accueil avec statistiques et graphiques"""
    # Statistiques
    stats = {
        'hotel_count': Hotel.objects.count(),
        'room_count': RoomType.objects.count(),
        'booking_count': Booking.objects.filter(status='confirmed').count(),
        'avg_rating': Hotel.objects.aggregate(Avg('stars'))['stars__avg'] or 0,
    }
    
    # Graphique Plotly - Répartition des hôtels par ville
    hotels_by_city = Hotel.objects.values('city').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    if hotels_by_city:
        cities = [item['city'] for item in hotels_by_city]
        counts = [item['count'] for item in hotels_by_city]
        
        fig = go.Figure(data=[
            go.Bar(
                x=cities,
                y=counts,
                marker_color=['#2563eb', '#0ea5e9', '#10b981', '#f59e0b', '#ef4444']
            )
        ])
        
        fig.update_layout(
            title='Hôtels par ville',
            title_font_size=16,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            height=300,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        plot_div = opy.plot(fig, auto_open=False, output_type='div')
    else:
        plot_div = "<div class='no-data'>Aucune donnée disponible</div>"
    
    # Derniers hôtels ajoutés
    latest_hotels = Hotel.objects.order_by('-created_at')[:3]
    
    context = {
        'stats': stats,
        'plot_div': plot_div,
        'latest_hotels': latest_hotels,
    }
    return render(request, 'index.html', context)

def hotel_list(request):
    """Liste de tous les hôtels avec filtres"""
    hotels = Hotel.objects.all()
    
    # Filtrage
    city = request.GET.get('city')
    if city:
        hotels = hotels.filter(city__icontains=city)
    
    stars = request.GET.get('stars')
    if stars:
        hotels = hotels.filter(stars=stars)
    
    # Trier
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price':
        hotels = hotels.annotate(avg_price=Avg('room_types__price_per_night')).order_by('avg_price')
    elif sort_by == 'stars':
        hotels = hotels.order_by('-stars')
    else:
        hotels = hotels.order_by('name')
    
    # Villes uniques pour le filtre
    cities = Hotel.objects.values_list('city', flat=True).distinct()
    
    context = {
        'hotels': hotels,
        'cities': cities,
        'selected_city': city,
        'selected_stars': stars,
        'sort_by': sort_by,
    }
    return render(request, 'hotels/list.html', context)

def hotel_detail(request, hotel_id):
    """Détail d'un hôtel avec ses chambres"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.room_types.all()
    
    # Graphique Plotly - Prix des chambres
    if rooms:
        room_names = [room.name for room in rooms]
        room_prices = [float(room.price_per_night) for room in rooms]
        
        fig = go.Figure(data=[
            go.Bar(
                x=room_names,
                y=room_prices,
                marker_color='#2563eb',
                text=room_prices,
                texttemplate='%{text:.0f}€',
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='Prix des chambres',
            title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            height=250,
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis_tickangle=-45
        )
        
        price_plot = opy.plot(fig, auto_open=False, output_type='div')
    else:
        price_plot = None
    
    context = {
        'hotel': hotel,
        'rooms': rooms,
        'price_plot': price_plot,
    }
    return render(request, 'hotels/detail.html', context)

def search_hotels(request):
    """Page de recherche d'hôtels"""
    cities = Hotel.objects.values_list('city', flat=True).distinct()
    
    context = {
        'cities': cities,
    }
    return render(request, 'hotels/search.html', context)

# ==================== VUES AUTHENTIFICATION ====================

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'auth/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Identifiants incorrects')
    
    return render(request, 'auth/login.html')

def register_view(request):
    """Page d'inscription"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validation
        errors = []
        
        if not username or not email or not password1 or not password2:
            errors.append('Tous les champs obligatoires doivent être remplis')
        
        if password1 != password2:
            errors.append('Les mots de passe ne correspondent pas')
        
        if len(password1) < 8:
            errors.append('Le mot de passe doit faire au moins 8 caractères')
        
        if User.objects.filter(username=username).exists():
            errors.append('Ce nom d\'utilisateur est déjà pris')
        
        if User.objects.filter(email=email).exists():
            errors.append('Cet email est déjà utilisé')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    user_type='client'
                )
                login(request, user)
                messages.success(request, 'Compte créé avec succès!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Erreur lors de la création du compte: {str(e)}")
    
    return render(request, 'auth/register.html')

def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté')
    return redirect('home')

# ==================== VUES RESERVATIONS ====================

@login_required
def my_bookings(request):
    """Page des réservations de l'utilisateur"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Graphique Plotly - Évolution des dépenses
    if bookings:
        # Regrouper par mois
        monthly_data = {}
        for booking in bookings:
            month_year = booking.created_at.strftime('%Y-%m')
            if month_year not in monthly_data:
                monthly_data[month_year] = 0
            monthly_data[month_year] += float(booking.total_price)
        
        months = sorted(monthly_data.keys())[-6:]  # 6 derniers mois
        amounts = [monthly_data[m] for m in months]
        
        fig = go.Figure(data=[
            go.Scatter(
                x=months,
                y=amounts,
                mode='lines+markers',
                line=dict(color='#2563eb', width=3),
                marker=dict(size=8, color='#2563eb')
            )
        ])
        
        fig.update_layout(
            title='Historique des dépenses',
            title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            height=300,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        plot_div = opy.plot(fig, auto_open=False, output_type='div')
    else:
        plot_div = None
    
    context = {
        'bookings': bookings,
        'plot_div': plot_div,
    }
    return render(request, 'bookings/list.html', context)

@login_required
def booking_detail(request, booking_id):
    """Détail d'une réservation"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Gestion de l'annulation
    if request.method == 'POST' and 'status' in request.POST:
        new_status = request.POST['status']
        
        if new_status == 'cancelled':
            # Vérifier si l'annulation est possible
            days_before = (booking.check_in_date - timezone.now().date()).days
            
            if days_before <= 0:
                messages.error(request, 'Impossible d\'annuler une réservation après la date d\'arrivée')
            elif days_before < 7:
                messages.warning(request, 'Annulation tardive - pénalité de 100%')
            
            booking.status = 'cancelled'
            booking.cancellation_reason = "Annulée par l'utilisateur"
            booking.save()
            
            # Mettre à jour le paiement
            if hasattr(booking, 'payment'):
                booking.payment.payment_status = 'refunded'
                booking.payment.save()
            
            messages.success(request, "Réservation annulée avec succès")
            return redirect('booking_detail', booking_id=booking_id)
    
    # Récupérer les politiques d'annulation
    policies = CancellationPolicy.objects.filter(
        hotel=booking.room_type.hotel
    ).order_by('days_before_checkin')
    
    context = {
        'booking': booking,
        'cancellation_policies': policies,
    }
    return render(request, 'bookings/detail.html', context)

@login_required
def create_booking(request, room_id):
    """Créer une réservation"""
    room = get_object_or_404(RoomType, id=room_id)
    
    # Préparer les données pour le template
    today = timezone.now().date()
    
    # Limiter le nombre de chambres disponibles
    max_rooms = min(room.quantity_available, 10)
    room_range = range(1, max_rooms + 1)
    
    # Plage de personnes (basée sur la capacité et le nombre de chambres)
    max_guests = room.capacity * max_rooms
    guest_range = range(1, max_guests + 1)
    
    # Récupérer les politiques d'annulation
    policies = CancellationPolicy.objects.filter(
        hotel=room.hotel
    ).order_by('days_before_checkin')
    
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        rooms = int(request.POST.get('rooms', 1))
        guests = int(request.POST.get('guests', room.capacity))
        special_requests = request.POST.get('special_requests', '')
        
        # Validation des dates
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Format de date invalide")
            return redirect('create_booking', room_id=room_id)
        
        # Validation
        errors = []
        
        if check_in < today:
            errors.append("La date d'arrivée ne peut pas être dans le passé")
        
        if check_in >= check_out:
            errors.append("La date de départ doit être après la date d'arrivée")
        
        if rooms > room.quantity_available:
            errors.append(f"Seulement {room.quantity_available} chambre(s) disponible(s)")
        
        if guests > room.capacity * rooms:
            errors.append(f"Maximum {room.capacity * rooms} personne(s) pour {rooms} chambre(s)")
        
        # Vérifier la disponibilité
        overlapping_bookings = Booking.objects.filter(
            room_type=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
            status__in=['pending', 'confirmed']
        ).count()
        
        if overlapping_bookings + rooms > room.quantity_available:
            errors.append(f"Pas assez de chambres disponibles pour ces dates")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Calcul du prix
            nights = (check_out - check_in).days
            total_price = room.price_per_night * nights * rooms
            
            # Créer la réservation
            booking = Booking.objects.create(
                user=request.user,
                room_type=room,
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_rooms=rooms,
                number_of_guests=guests,
                total_price=total_price,
                status='pending',
                special_requests=special_requests
            )
            
            # Créer un paiement simulé
            Payment.objects.create(
                booking=booking,
                amount=total_price,
                payment_method='credit_card',
                payment_status='pending',
                transaction_id=f"TXN{booking.id:06d}"
            )
            
            # Envoyer un email de confirmation
            try:
                send_confirmation_email(booking)
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")
            
            messages.success(request, f"Réservation créée avec succès! Référence: #{booking.id}")
            return redirect('booking_detail', booking_id=booking.id)
    
    context = {
        'room': room,
        'today': today,
        'room_range': room_range,
        'guest_range': guest_range,
        'policies': policies,
    }
    return render(request, 'bookings/create.html', context)

@login_required
def process_payment(request, booking_id):
    """Simuler un paiement"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'pending' and hasattr(booking, 'payment'):
        # Simuler le paiement
        booking.payment.payment_status = 'completed'
        booking.payment.payment_date = timezone.now()
        booking.payment.save()
        
        # Mettre à jour le statut de la réservation
        booking.status = 'confirmed'
        booking.save()
        
        # Envoyer un email de confirmation de paiement
        try:
            send_payment_confirmation_email(booking)
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")
        
        messages.success(request, "Paiement effectué avec succès! Votre réservation est confirmée.")
    else:
        messages.error(request, "Impossible de procéder au paiement")
    
    return redirect('booking_detail', booking_id=booking_id)

# ==================== FONCTIONS UTILITAIRES ====================

def send_confirmation_email(booking):
    """Envoyer un email de confirmation de réservation"""
    subject = f'Confirmation de réservation #{booking.id}'
    
    message = f"""
    Bonjour {booking.user.get_full_name() or booking.user.username},
    
    Votre réservation a été enregistrée avec succès.
    
    📋 Détails de la réservation:
    ----------------------------------------
    • Référence: #{booking.id}
    • Hôtel: {booking.room_type.hotel.name}
    • Chambre: {booking.room_type.name}
    • Date d'arrivée: {booking.check_in_date}
    • Date de départ: {booking.check_out_date}
    • Nombre de nuits: {booking.number_of_nights}
    • Nombre de chambres: {booking.number_of_rooms}
    • Nombre de personnes: {booking.number_of_guests}
    • Prix total: {booking.total_price}€
    • Statut: {booking.get_status_display()}
    
    Pour finaliser votre réservation, veuillez procéder au paiement.
    
    Cordialement,
    L'équipe HotelReservation
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )

def send_payment_confirmation_email(booking):
    """Envoyer un email de confirmation de paiement"""
    subject = f'Confirmation de paiement - Réservation #{booking.id}'
    
    message = f"""
    Bonjour {booking.user.get_full_name() or booking.user.username},
    
    Votre paiement a été traité avec succès.
    
    ✅ Réservation confirmée
    ----------------------------------------
    • Référence: #{booking.id}
    • Hôtel: {booking.room_type.hotel.name}
    • Chambre: {booking.room_type.name}
    • Dates: {booking.check_in_date} → {booking.check_out_date}
    • Prix total payé: {booking.total_price}€
    • N° de transaction: {booking.payment.transaction_id}
    
    Nous vous remercions pour votre confiance et vous souhaitons un excellent séjour!
    
    Pour toute question, contactez-nous à: contact@hotelreservation.com
    
    Cordialement,
    L'équipe HotelReservation
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )

def send_cancellation_email(booking):
    """Envoyer un email d'annulation"""
    subject = f'Annulation de réservation #{booking.id}'
    
    message = f"""
    Bonjour {booking.user.get_full_name() or booking.user.username},
    
    Votre réservation a été annulée.
    
    ❌ Réservation annulée
    ----------------------------------------
    • Référence: #{booking.id}
    • Hôtel: {booking.room_type.hotel.name}
    • Dates: {booking.check_in_date} → {booking.check_out_date}
    • Motif: {booking.cancellation_reason or "Annulée par l'utilisateur"}
    • Montant remboursé: {booking.total_price}€
    
    Le remboursement sera traité dans les 5 à 10 jours ouvrés.
    
    Nous espérons vous revoir bientôt!
    
    Cordialement,
    L'équipe HotelReservation
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )

# ==================== VUE DE RECHERCHE API ====================

def api_search_hotels(request):
    """API de recherche d'hôtels (pour la page de recherche)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            city = data.get('city', '')
            min_price = data.get('min_price')
            max_price = data.get('max_price')
            stars = data.get('stars')
            
            # Convertir les dates
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Trouver les chambres réservées pendant cette période
            booked_rooms = Booking.objects.filter(
                Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date),
                status__in=['confirmed', 'pending']
            ).values_list('room_type_id', flat=True)
            
            # Filtrer les chambres disponibles
            rooms = RoomType.objects.filter(
                quantity_available__gt=0
            ).exclude(id__in=booked_rooms)
            
            # Appliquer les filtres supplémentaires
            if city:
                rooms = rooms.filter(hotel__city__icontains=city)
            
            if min_price:
                rooms = rooms.filter(price_per_night__gte=min_price)
            
            if max_price:
                rooms = rooms.filter(price_per_night__lte=max_price)
            
            if stars:
                rooms = rooms.filter(hotel__stars=stars)
            
            # Préparer les résultats
            results = []
            for room in rooms:
                results.append({
                    'id': room.id,
                    'name': room.hotel.name,
                    'city': room.hotel.city,
                    'room_name': room.name,
                    'price_per_night': float(room.price_per_night),
                    'capacity': room.capacity,
                    'description': room.hotel.description[:100] + '...' if room.hotel.description else '',
                    'stars': room.hotel.stars,
                    'has_wifi': room.hotel.has_wifi,
                    'has_parking': room.hotel.has_parking,
                    'has_pool': room.hotel.has_pool,
                })
            
            return JsonResponse(results, safe=False)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

# ==================== VUE API STATUS ====================

def api_status(request):
    """Vérifier le statut de l'API"""
    from django.http import JsonResponse
    
    return JsonResponse({
        'status': 'ok',
        'message': 'Hotel Reservation API is running',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat(),
        'endpoints': {
            'home': '/',
            'hotels': '/hotels/',
            'search': '/search/',
            'login': '/login/',
            'register': '/register/',
            'my_bookings': '/my-bookings/',
            'api_auth': '/api/auth/',
            'api_hotels': '/api/hotels/',
            'api_bookings': '/api/bookings/',
            'admin': '/admin/',
        }
    })

# ==================== VUE ERREUR 404 ====================

def custom_404(request, exception):
    """Page 404 personnalisée"""
    return render(request, '404.html', status=404)

# ==================== VUE PROFILE UTILISATEUR ====================

@login_required
def user_profile(request):
    """Page de profil utilisateur"""
    if request.method == 'POST':
        # Mise à jour du profil
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        
        messages.success(request, 'Profil mis à jour avec succès')
        return redirect('user_profile')
    
    # Statistiques de l'utilisateur
    bookings_count = Booking.objects.filter(user=request.user).count()
    total_spent = Booking.objects.filter(
        user=request.user, 
        status='confirmed'
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    context = {
        'bookings_count': bookings_count,
        'total_spent': total_spent,
    }
    return render(request, 'auth/profile.html', context)

# ==================== VUE CONTACT ====================

def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if not name or not email or not message:
            messages.error(request, 'Tous les champs sont obligatoires')
        else:
            # Envoyer l'email
            try:
                send_mail(
                    f'Contact depuis HotelReservation - {name}',
                    f"""
                    Nom: {name}
                    Email: {email}
                    
                    Message:
                    {message}
                    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Message envoyé avec succès!')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'envoi du message: {str(e)}')
    
    return render(request, 'contact.html')

# ==================== IMPORT MANQUANT ====================

from django.http import JsonResponse
from django.db.models import Sum