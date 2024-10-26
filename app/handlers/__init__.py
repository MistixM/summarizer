# Init module that will load all necessary routers to the Dispatcher
# Add new routers here to show additional functionality in the bot
from .start import start_router
from .summarize import summarize_router
from .faq import faq_router
from .post import post_router
from .ping import ping_router
from .subscription import sub_router
from .support import support_router
from .installation import installation_router
from .debug import debug_router

# Fill out the list that will be unpacked in dispatcher
routers_list = [
    start_router,
    faq_router,
    post_router,
    sub_router,
    support_router,
    installation_router,
    debug_router,
    
    # Blocking router below
    ping_router,
    summarize_router,
]