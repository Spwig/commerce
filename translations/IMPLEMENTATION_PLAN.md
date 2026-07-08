# Translation Service Implementation Plan

## Overview
This document outlines the implementation plan for the AI-powered translation service for the e-commerce platform, based on the solution design in `.claude_code/translation/translation_service.md`.

## Phase 1: Infrastructure Setup

### 1.1 Translator Microservice
- Create a new `translator/` directory for the FastAPI microservice
- Implement CTranslate2 wrapper with M2M100-418M model support
- Create Dockerfile for the translator service with model bundling
- Add translator service to docker-compose.yml
- Implement REST API endpoints:
  - POST /translate (single translation)
  - POST /translate_batch (batch translation)
  - POST /detect (language detection)
  - GET /health (service health check)
  - GET /models (list installed models)
  - POST /models/install & DELETE /models/:id (model management)

### 1.2 Django Integration
- Create new Django app: `translation_service`
- Install django-parler for multi-language field storage (replacing django-modeltranslation)
- Create translation models:
  - TranslationProvider (local/external configuration)
  - TranslationJob (job queue management)
  - TranslationMeta (locked translations tracking)
  - TranslationModel (installed models registry)

## Phase 2: Admin Interface Development

### 2.1 System Validation & Overview Panel
- Create admin views in `translation_service/admin.py`
- Implement system requirements checker (CPU, RAM, disk space)
- Create validation UI with success/warning messages
- Add global enable/disable toggle for translation services
- Implement quick test interface with latency metrics

### 2.2 Local Service Management
- Build language pair management interface
- Create model download/installation UI with progress tracking
- Implement disk usage monitoring and forecasting
- Add performance testing tools (benchmark runner)
- Create translation policy configuration (sync vs queued)

### 2.3 External Provider Integration
- Design provider configuration wizard
- Implement provider API abstraction layer
- Create language code mapping interface
- Add cost estimation tools
- Build per-language routing rules

### 2.4 Translation Policies & Controls
- Create source/target language selectors
- Implement locked translation management
- Add bulk translation scheduler
- Build audit logging system

## Phase 3: Product Integration

### 3.1 Model Migration
- Migrate from django-modeltranslation to django-parler:
  - Create data migration scripts
  - Update Product, Category, Brand, Collection models
  - Add source_checksum field for change detection
  - Implement translation locking mechanism

### 3.2 Translation Triggers
- Add post_save signals for automatic translation
- Implement checksum-based change detection
- Create background job runner for bulk translations
- Add HTML/placeholder safety tokenization

## Phase 4: Templates & UI

### 4.1 Admin Templates
- Create templates in `templates/admin/translation_service/`:
  - overview.html (main dashboard)
  - local_service.html (local model management)
  - external_providers.html (provider configuration)
  - translation_policies.html (policy settings)
  - audit_logs.html (logging interface)

### 4.2 JavaScript Components
- Build model download progress tracker
- Create real-time performance testing UI
- Implement translation preview interface
- Add bulk operation management tools

## Phase 5: Background Jobs & Optimization

### 5.1 Job Queue System
- Create database-backed job queue (no Redis dependency)
- Implement management command: `run_translation_jobs`
- Add scheduler container to docker-compose
- Build rate limiting and throttling mechanisms

### 5.2 Performance Optimization
- Implement CPU load monitoring
- Add auto-cancellation for high-load scenarios
- Create off-peak scheduling system
- Build batch processing optimization

## Phase 6: Security & Testing

### 6.1 Security Implementation
- Ensure translator service only accessible internally
- Add PII redaction for external providers
- Implement secure credential storage
- Create audit logging without raw content

### 6.2 Testing & QA
- Write unit tests for all components
- Create integration tests for Docker services
- Test system validation accuracy
- Verify translation quality across languages
- Test failure modes and fallbacks

## Implementation Timeline

### Week 1-2: Infrastructure (Phase 1)
- Set up translator microservice
- Update Docker configuration
- Create base Django app

### Week 3-4: Admin Interface (Phase 2)
- Build system validation
- Create management interfaces
- Implement provider integration

### Week 5: Product Integration (Phase 3)
- Migrate translation system
- Add automatic triggers

### Week 6: UI Development (Phase 4)
- Create admin templates
- Build JavaScript components

### Week 7: Background Jobs (Phase 5)
- Implement job queue
- Add optimization features

### Week 8: Testing & Deployment (Phase 6)
- Security hardening
- Comprehensive testing
- Documentation

## Key Considerations

1. **Compatibility**: Ensure smooth migration from django-modeltranslation to django-parler
2. **Performance**: Validate system requirements before enabling features
3. **i18n Compliance**: Follow all rules from `.claude_code/rules.md` for interface translations
4. **Incremental Rollout**: Deploy in stages with feature flags
5. **Monitoring**: Add comprehensive logging and metrics collection

## Technical Requirements

### System Requirements (Minimum)
- CPU: 4 vCPU (8 vCPU recommended for bulk jobs)
- RAM: 8 GB (16 GB recommended)
- Disk: 3-6 GB per base model
- Docker/Compose runtime
- No GPU required (optional)

### Software Stack
- FastAPI for translator microservice
- CTranslate2 for model inference
- M2M100-418M as base model
- Django + django-parler for translations
- PostgreSQL for storage
- Docker Compose for orchestration

## Migration Strategy

### From django-modeltranslation to django-parler
1. Export existing translations
2. Install and configure django-parler
3. Create migration scripts
4. Update model definitions
5. Import translations to new structure
6. Verify data integrity
7. Update admin interfaces

## File Structure

```
translation_service/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── signals.py
├── utils.py
├── validators.py
├── management/
│   └── commands/
│       ├── run_translation_jobs.py
│       ├── validate_translation_system.py
│       └── migrate_translations.py
├── migrations/
├── templates/
│   └── admin/
│       └── translation_service/
│           ├── overview.html
│           ├── local_service.html
│           ├── external_providers.html
│           ├── translation_policies.html
│           └── audit_logs.html
├── static/
│   └── translation_service/
│       ├── css/
│       └── js/
├── locale/
├── tests/
│   ├── test_models.py
│   ├── test_admin.py
│   ├── test_translation.py
│   └── test_integration.py
└── api/
    ├── __init__.py
    ├── serializers.py
    └── views.py

translator/  (separate microservice)
├── Dockerfile
├── requirements.txt
├── main.py
├── models.py
├── translation.py
├── utils.py
├── config.py
└── tests/
```

## Configuration

### Environment Variables
```
TRANSLATOR_ENABLED=true|false
TRANSLATOR_MODE=local|external
TRANSLATOR_URL=http://translator:8088
TRANSLATOR_ALLOWED_LANGS=en,es,fr,de,pt,zh,ja
TRANSLATOR_OFFPEAK_WINDOW=02:00-06:00
EXT_MT_PROVIDER=name
EXT_MT_ENDPOINT=...
EXT_MT_API_KEY=...
```

## Success Criteria

1. ✅ System validation correctly detects hardware capabilities
2. ✅ Seamless switching between local and external translation
3. ✅ Language pack installation with progress tracking
4. ✅ Respect for locked translations
5. ✅ Bulk translation without impacting user experience
6. ✅ Accurate performance metrics
7. ✅ No sensitive data in logs
8. ✅ All UI text properly internationalized
9. ✅ Graceful failure handling
10. ✅ Complete audit trail

## Next Steps

1. Review and approve this implementation plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Regular progress reviews at phase boundaries
5. User acceptance testing before production deployment