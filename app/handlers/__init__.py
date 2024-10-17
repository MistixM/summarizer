from .start import start_router
from .summarize import summarize_router
from .faq import faq_router
from .ad import ad_router
from .ping import ping_router

routers_list = [
    start_router,
    faq_router,
    ad_router,


    # Blocking router below
    ping_router,
    summarize_router,
]