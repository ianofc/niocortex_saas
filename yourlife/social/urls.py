from django.urls import path
from .views import feed, profile, groups, events, auth, chat, extras, interactions, general

app_name = 'yourlife_social'

urlpatterns = [
   # --- Feed & Core ---
    path('feed/', feed.home_feed, name='home'),
    path('reels/', feed.reels_view, name='reels'),
    path('explore/', general.explore, name='explore'),
    path('create-story/', feed.create_story, name='create_story'),

    # --- Páginas Extras ---
    path('settings/', extras.settings_view, name='settings_page'),
    path('support/', extras.support_view, name='support_page'),
    path('themes/', extras.themes_view, name='themes_page'),

    # --- Profile ---
    path('perfil/', profile.my_profile, name='meu_perfil'),
    path('perfil/editar/', profile.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    path('profile/<str:username>/followers/', profile.followers_list, name='profile_followers'),
    path('profile/<str:username>/following/', profile.following_list, name='profile_following'),

    # --- Groups ---
    path('groups/', groups.groups_list, name='groups_list'),
    path('groups/create/', groups.create_group, name='create_group'),
    path('groups/<int:group_id>/', groups.group_detail, name='group_detail'),

    # --- Events ---
    path('events/', events.events_list, name='events_list'),
    path('events/calendar/', events.calendar_view, name='calendar_view'),

    # --- Chat (TalkIO) ---
    path('talkio/', chat.talkio_view, name='talkio'),
    # ADICIONADO: Rota para o iframe do drawer
    path('talkio/app/', chat.talkio_view, name='talkio_app'),

    # --- Auth ---
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),

    # --- Interactions (AJAX/HTMX) ---
    path('like/<int:post_id>/', interactions.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', interactions.add_comment, name='add_comment'),# --- Feed & Core ---
    path('feed/', feed.home_feed, name='home'),
    path('reels/', feed.reels_view, name='reels'),
    path('explore/', general.explore, name='explore'),
    path('create-story/', feed.create_story, name='create_story'),

    # --- Páginas Extras ---
    path('settings/', extras.settings_view, name='settings_page'),
    path('support/', extras.support_view, name='support_page'),
    path('themes/', extras.themes_view, name='themes_page'),

    # --- Profile ---
    path('perfil/', profile.my_profile, name='meu_perfil'),
    path('perfil/editar/', profile.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    path('profile/<str:username>/followers/', profile.followers_list, name='profile_followers'),
    path('profile/<str:username>/following/', profile.following_list, name='profile_following'),

    # --- Groups ---
    path('groups/', groups.groups_list, name='groups_list'),
    path('groups/create/', groups.create_group, name='create_group'),
    path('groups/<int:group_id>/', groups.group_detail, name='group_detail'),

    # --- Events ---
    path('events/', events.events_list, name='events_list'),
    path('events/calendar/', events.calendar_view, name='calendar_view'),

    # --- Chat (TalkIO) ---
    path('talkio/', chat.talkio_view, name='talkio'),
    # ADICIONADO: Rota para o iframe do drawer
    path('talkio/app/', chat.talkio_view, name='talkio_app'),

    # --- Auth ---
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),

    # --- Interactions (AJAX/HTMX) ---
    path('like/<int:post_id>/', interactions.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', interactions.add_comment, name='add_comment'),
    
]