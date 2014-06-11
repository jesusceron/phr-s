from django.conf.urls.defaults import *
from views import *
import settings
from django.conf import settings as rootsettings

urlpatterns = patterns('',
   # authentication
   (r'^start_auth', start_auth),
   (r'^after_auth', after_auth),

   (r'^autismscreening/index$', index),
   (r'^autismscreening/new$', general_information),
   (r'^autismscreening/agregarmuestra$', agregarmuestra),
   (r'^autismscreening/problem_list$', problem_list),
   (r'^autismscreening/(?P<poll_id>[^/]+)', shareanswer),
   
    # static
    ## WARNING NOT FOR PRODUCTION
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': rootsettings.SERVER_ROOT_DIR + settings.STATIC_HOME}),
)
