from django.urls import path

from . import views

app_name = "domain_ssl"

urlpatterns = [
    path("status/", views.domain_ssl_status, name="status"),
    path("validate-dns/", views.validate_dns_view, name="validate_dns"),
    path("configure/", views.configure_domain_view, name="configure"),
    path("progress/", views.domain_ssl_progress, name="progress"),
    path("upload-cert/", views.upload_cert_view, name="upload_cert"),
    # Hosted custom domain management (proxies to update server)
    path("custom-domain/", views.custom_domain_status, name="custom_domain_status"),
    path("custom-domain/verify/", views.custom_domain_verify, name="custom_domain_verify"),
    path("custom-domain/add/", views.custom_domain_add, name="custom_domain_add"),
    path("custom-domain/remove/", views.custom_domain_remove, name="custom_domain_remove"),
]
