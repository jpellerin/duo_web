from django.conf.urls.defaults import *

import duo_auth

# The Django installation must also serve Duo-IFRAME-v1.js from
# settings.STATIC_PREFIX
urlpatterns = patterns(
    '',
    (r'^accounts/duo_login/$', duo_auth.login),
    (r'^accounts/duo_logout/$', duo_auth.logout))
