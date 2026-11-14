# Build status — 0.1.0

## Implemented in this starter
- Next.js responsive dashboard with nine workspace sections.
- PWA manifest and service worker registration.
- FastAPI application with health, broker registry, strategy catalog, risk preview and order preview endpoints.
- Five broker adapter scaffolds with explicit NOT_CONFIGURED status.
- Seven initial OHLCV strategy/indicator modules.
- PostgreSQL schema for users, broker accounts, encrypted credential fields, instruments, candles, strategies, signals, risk, orders, positions, holdings, journals, backtests, notifications and audit logs.
- Docker Compose for local startup.

## Not yet implemented
- User registration/login and access-control enforcement.
- Actual broker OAuth callbacks, signed request flows, credential vault and token refresh.
- Real market data, instrument master synchronization and historical data provider.
- Option-chain feed and Greeks calculation.
- Persistent order/position reconciliation and live order submission.
- Push notification delivery and production monitoring.
- Regulatory and security certification/review.

## Safety state
Live trading false; automated execution false; order preview never submits a broker order.
