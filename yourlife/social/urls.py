from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions, api, extras

app_name = 'yourlife_social'

urlpatterns = [
    path('support/report/', extras.report_abuse, name='report_abuse'),
    # Core & Feed
    path('feed/', feed.home_feed, name='home'),
    path('story/create/', feed.create_story, name='create_story'),
    path('reels/', feed.reels_view, name='reels'),
    path('explore/', general.explore, name='explore'),
    
    # Auth
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    
    # Follows
    path('profile/<str:username>/followers/', profile.followers_list, name='profile_followers'),
    path('profile/<str:username>/following/', profile.following_list, name='profile_following'),
    
    # Perfil
    path('perfil/', profile.my_profile, name='meu_perfil'),
    path('perfil/editar/', profile.profile_edit, name='profile_edit'),
    path('perfil/<str:username>/', profile.user_profile, name='profile_detail'),
    
    # Interações
    path('post/<int:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/edit/', interactions.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', interactions.delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/', interactions.add_comment, name='add_comment'),
    path('post/<int:post_id>/share/', interactions.share_post, name='share_post'),
    path('comment/<int:comment_id>/delete/', interactions.delete_comment, name='delete_comment'),
    
    # Comunidades e Eventos
    path('groups/', groups.GroupListView.as_view(), name='groups_list'),
    path('groups/create/', groups.group_create, name='group_create'),
    path('groups/<int:group_id>/', groups.group_detail, name='group_detail'),
    path('events/', events.EventListView.as_view(), name='events_list'),
    path('events/create/', events.event_create, name='event_create'),
    path('events/<int:event_id>/', events.event_detail, name='event_detail'),
    
    # IAs
    path('talkio/', extras.talkio_app, name='talkio_app'),
    path('zios/', extras.zios_view, name='zios_view'),
    path('api/zios/chat/', api.api_zios_chat, name='api_zios_chat'),
    path('api/zios/finalize/', api.api_finalize, name='api_finalize'),
    
    # Config
    path('support/', extras.support_page, name='support_page'),
    path('settings/', extras.settings_page, name='settings_page'),
    path('settings/support/', extras.settings_support, name='settings_support'),
    path('settings/theme/', extras.settings_theme, name='settings_theme'),
    path('settings/a11y/', extras.settings_a11y, name='settings_a11y'),
]
