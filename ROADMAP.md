# Roadmap

## 0.x.x

- [ ] Databases
    - [ ] MongoDB
- [ ] Authentication + Permissions
- [ ] Testing
- [ ] MQ handlers (NATS, ...)
- [ ] ? Admin site

## 0.1.0

- [ ] Project Template
- [ ] Auto-reloading functionality for dev env
- [x] Configuration
- [x] Routing
- [x] Databases
    - [x] PostgreSQL
    - [x] MySQL (Note: `CreateMixin` and `UpdateMixin` from generic views not supported yet)
- [x] Migrations
- [x] Caches
    - [x] Redis
    - [x] Memcached
- [x] Generic views
    - [x] `ValidationView`
    - [x] `CreateView`
    - [x] `ListView`
    - [x] `RetrieveView`
    - [x] `DestroyView`
    - [x] `UpdateView`
    - [x] `ListCreateView`
    - [x] `RetrieveUpdateView`
    - [x] `RetrieveDestroyView`
    - [x] `RetrieveUpdateDestroyView`
    - [x] `TemplateView`
- [x] Data validation
- [ ] Middlewares
    - [x] Debug headers middleware
    - [ ] Sentry middleware
    - [x] Clickjacking protection middleware
    - [ ] ? CSRF Middleware
    - [ ] Security middleware (`django.middleware.security.SecurityMiddleware`)
    - [ ] Session middleware
- [x] Logging
- [ ] Deployment
