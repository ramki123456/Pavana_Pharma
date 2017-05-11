from django.conf.urls import patterns, include, url
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'Medical_Agency.views.home', name='home'),
    url(r'^home/', 'Medical_Agency.views.home1'),
    url(r'^login/', 'Medical_Agency.views.login'),
    url(r'^check_stock/', 'Medical_Agency.views.check_stock'),
    url(r'^check_dealers/', 'Medical_Agency.views.check_dealers'),
    # url(r'^billing/', 'Medical_Agency.views.billing'),
    url(r'^check_prev_bills/', 'Medical_Agency.views.prev_billing'),
    url(r'^add_stock/', 'Medical_Agency.views.add_stock'),
    url(r'^add_stock_to_db', 'Medical_Agency.views.add_stock_to_db'),
    url(r'^check_item_wise/', 'Medical_Agency.views.check_item_wise_page'),
    url(r'^show_item_wise_stock/', 'Medical_Agency.views.show_item_wise'),
    url(r'^check_company_wise/',
        'Medical_Agency.views.check_company_wise_page'),
    url(r'^show_company_wise/', 'Medical_Agency.views.show_company_wise'),
    url(r'^check_batch_num_wise/',
        'Medical_Agency.views.check_batch_number_wise_page'),
    url(r'^show_batch_num_wise/', 'Medical_Agency.views.show_batch_num_wise'),
    url(r'^check_delaers/', 'Medical_Agency.views.check_dealers'),
    url(r'^add_dealer/', 'Medical_Agency.views.add_dealer'),
    url(r'^add_dealer_to_db/', 'Medical_Agency.views.add_dealer_to_db'),
    url(r'^billing/', 'Medical_Agency.views.billing_page'),
    url(r'^show_billing_cart/', 'Medical_Agency.views.show_billing_cart'),
    url(r'^go_final_billing/', 'Medical_Agency.views.go_final_billing'),
    url(r'^print_page/', 'Medical_Agency.views.print_page'),
    url(r'^send_mail/', 'Medical_Agency.views.send_mail'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        url(r'^media/(?P<path>.*)$',
                            'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT,
                             'show_indexes': True}),
                        )
