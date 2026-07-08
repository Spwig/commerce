from django.urls import path
from . import views

app_name = 'translations_api'

urlpatterns = [
    # Local service API
    path('local-service/data/', views.local_service_data_api, name='local_service_data'),
    path('quick-translate/', views.quick_translate_view, name='quick_translate'),
    path('toggle-service/', views.toggle_translation_service_view, name='toggle_service'),
    path('run-benchmark/', views.run_benchmark_view, name='run_benchmark'),
    path('download/status/', views.download_status_view, name='download_status'),
    path('download/start/', views.start_download_view, name='start_download'),

    # Docker container management
    path('docker/status/', views.docker_status_view, name='docker_status'),
    path('docker/start/', views.docker_start_view, name='docker_start'),
    path('docker/stop/', views.docker_stop_view, name='docker_stop'),
    path('docker/restart/', views.docker_restart_view, name='docker_restart'),
    path('docker/logs/', views.docker_logs_view, name='docker_logs'),
    path('docker/pull/', views.docker_pull_view, name='docker_pull'),

    # Quantization management
    path('quantizations/', views.quantization_list_view, name='quantization_list'),
    path('quantizations/set/', views.quantization_set_view, name='quantization_set'),
    path('quantizations/download/', views.quantization_download_view, name='quantization_download'),

    # Language API
    path('languages/', views.languages_list_api, name='languages_list'),
    path('languages/activate/', views.language_activate_api, name='language_activate'),
    path('languages/reorder/', views.languages_reorder_api, name='languages_reorder'),
    path('languages/bulk-update/', views.languages_bulk_update_api, name='languages_bulk_update'),

    # Provider API
    path('provider/test/', views.test_provider_api, name='test_provider'),
    path('provider/test-translation/', views.test_translation_api, name='test_translation'),
    path('provider/save/', views.save_provider_api, name='save_provider'),
    path('provider/<uuid:account_id>/toggle/', views.toggle_provider_api, name='toggle_provider'),

    # UI Translations API
    path('ui-translations/<str:language_code>/', views.ui_translations_api, name='ui_translations_api'),
    path('ui-translations/<str:language_code>/save/', views.ui_translations_save_api, name='ui_translations_save'),
    path('ui-translations/<str:language_code>/auto-translate/', views.ui_translations_auto_translate_api, name='ui_translations_auto_translate'),
    path('ui-translations/<str:language_code>/export/', views.ui_translations_export_api, name='ui_translations_export'),
    path('ui-translations/<str:language_code>/import/preview/', views.ui_translations_import_preview_api, name='ui_translations_import_preview'),
    path('ui-translations/<str:language_code>/import/apply/', views.ui_translations_import_apply_api, name='ui_translations_import_apply'),
    path('ui-translations/<str:language_code>/translate-string/', views.ui_translations_translate_string_api, name='ui_translations_translate_string'),
    path('ui-translations/<str:language_code>/lock/', views.ui_translation_lock_api, name='ui_translation_lock'),

    # Coverage API
    path('coverage/', views.coverage_api, name='coverage_api'),
    path('coverage/refresh/', views.coverage_refresh_api, name='coverage_refresh'),

    # Translate All API
    path('translate-all/estimate/', views.translate_all_estimate_api, name='translate_all_estimate'),
    path('translate-all/', views.translate_all_api, name='translate_all'),
    path('translate-all/status/', views.translate_all_status_api, name='translate_all_status'),

    # Translation Locks API
    path('lock/toggle/', views.toggle_translation_lock_api, name='toggle_lock'),

    # Translation Jobs API
    path('jobs/', views.jobs_list_api, name='jobs_list'),
    path('jobs/create/', views.create_job_api, name='create_job'),
    path('jobs/<int:job_id>/', views.job_detail_api, name='job_detail'),
    path('jobs/<int:job_id>/update/', views.update_job_api, name='update_job'),
    path('jobs/<int:job_id>/cancel/', views.cancel_job_api, name='cancel_job'),
    path('jobs/<int:job_id>/retry/', views.retry_job_api, name='retry_job'),
    path('jobs/<int:job_id>/start/', views.start_job_api, name='start_job'),
    path('jobs/queue-status/', views.queue_status_api, name='queue_status'),
    path('jobs/bulk-create/', views.bulk_create_jobs_api, name='bulk_create_jobs'),
    path('jobs/bulk-action/', views.bulk_job_action_api, name='bulk_job_action'),
]
