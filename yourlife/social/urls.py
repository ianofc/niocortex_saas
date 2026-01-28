from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions

app_name = 'yourlife_social'

urlpatterns = [
    path('feed/', feed.home_feed_foryou, name='home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),

    path('settings/', general.settings_view, name='settings'),
    path('settings/theme/', general.settings_theme, name='settings_theme'),
    path('settings/accessibility/', general.settings_accessibility, name='settings_accessibility'),
    path('support/', general.support_view, name='support'),
    path('explore/', general.search_pinterest, name='explore'),

    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    path('groups/', groups.groups_list, name='groups_list'),
    path('events/', events.events_list, name='events_list'),
    
    path('post/<int:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', interactions.add_comment, name='add_comment'),
]
