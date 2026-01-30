from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions, chat

app_name = 'yourlife_social'

urlpatterns = [
    # Feed & Home
    path('', feed.home_feed_foryou, name='home'),
    path('feed/', feed.home_feed_foryou, name='feed_home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    # Recursos Extras
    path('reels/', feed.reels_view, name='reels'),
    path('explore/', feed.explore_view, name='explore'),
    path('talkio/', chat.talkio_view, name='talkio_app'),
    
    # Auth
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    
    # Configurações
    path('settings/', general.settings_view, name='settings'),
    path('settings/p/', general.settings_view, name='settings_page'),
    path('settings/theme/', general.settings_theme, name='settings_theme'),
    path('support/', general.support_view, name='support'),
    path('support/p/', general.support_view, name='support_page'),
    
    # Perfil (ESSENCIAL PARA O ERRO ATUAL)
    path('profile/me/', profile.meu_perfil, name='meu_perfil'),
    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    
    # Interações
    path('post/<int:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', interactions.add_comment, name='add_comment'),

    path('groups/', groups.groups_list, name='groups_list'),
    path('events/', events.events_list, name='events_list'),
]
