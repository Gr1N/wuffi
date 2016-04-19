# Roadmap

## 0.x.x

- [ ] Databases
    - [ ] MongoDB
- [ ] Migrations
- [ ] Authentication + Permissions
- [ ] Testing
- [ ] MQ handlers (NATS, ...)
- [ ] Templates + Static files
- [ ] ? Admin site

## 0.1.0

- [ ] Project Template
- [ ] Auto-reloading functionality for dev env
- [x] Configuration
- [x] Routing
- [ ] Databases
    - [x] PostgreSQL
    - [ ] MySQL
- [x] Caches
    - [x] Redis
    - [x] Memcached
- [ ] Generic views
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
- [x] Data validation
- [ ] Middlewares
    - [x] Debug headers middleware
    - [ ] Sentry middleware
    - [x] Clickjacking protection middleware
    - [ ] ? CSRF Middleware
    - [ ] Security middleware (`django.middleware.security.SecurityMiddleware`)
- [ ] Logging
