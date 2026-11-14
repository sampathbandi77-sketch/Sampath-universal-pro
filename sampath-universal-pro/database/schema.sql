CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS users (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email TEXT UNIQUE, phone TEXT UNIQUE,
 password_hash TEXT, status TEXT NOT NULL DEFAULT 'ACTIVE', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS broker_accounts (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id),
 broker TEXT NOT NULL CHECK (broker IN ('upstox','dhan','zerodha','angelone','coinswitch')),
 account_ref TEXT NOT NULL, connection_status TEXT NOT NULL DEFAULT 'PENDING',
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE(user_id,broker,account_ref)
);
CREATE TABLE IF NOT EXISTS broker_credentials (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), account_id UUID NOT NULL UNIQUE REFERENCES broker_accounts(id) ON DELETE CASCADE,
 encrypted_access_token BYTEA, encrypted_refresh_token BYTEA, expires_at TIMESTAMPTZ, updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS instruments (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), broker TEXT, exchange TEXT NOT NULL, symbol TEXT NOT NULL,
 instrument_token TEXT, instrument_type TEXT NOT NULL, expiry DATE, strike NUMERIC(16,4),
 option_type TEXT, lot_size INTEGER, tick_size NUMERIC(12,6), active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS idx_instruments_symbol ON instruments(symbol);
CREATE TABLE IF NOT EXISTS candles (
 id BIGSERIAL PRIMARY KEY, instrument_id UUID NOT NULL REFERENCES instruments(id), timeframe TEXT NOT NULL,
 candle_time TIMESTAMPTZ NOT NULL, open NUMERIC(18,6) NOT NULL, high NUMERIC(18,6) NOT NULL,
 low NUMERIC(18,6) NOT NULL, close NUMERIC(18,6) NOT NULL, volume BIGINT NOT NULL DEFAULT 0,
 UNIQUE(instrument_id,timeframe,candle_time)
);
CREATE TABLE IF NOT EXISTS strategies (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL UNIQUE, category TEXT,
 version INTEGER NOT NULL DEFAULT 1, configuration JSONB NOT NULL DEFAULT '{}', active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS strategy_settings (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id),
 strategy_id UUID NOT NULL REFERENCES strategies(id), enabled BOOLEAN NOT NULL DEFAULT FALSE,
 parameters JSONB NOT NULL DEFAULT '{}', UNIQUE(user_id,strategy_id)
);
CREATE TABLE IF NOT EXISTS signals (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), instrument_id UUID REFERENCES instruments(id),
 strategy_id UUID REFERENCES strategies(id), direction TEXT NOT NULL, score NUMERIC(5,2),
 entry_price NUMERIC(18,6), stop_loss NUMERIC(18,6), targets JSONB, explanation JSONB,
 status TEXT NOT NULL DEFAULT 'GENERATED', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_signals_created ON signals(created_at DESC);
CREATE TABLE IF NOT EXISTS risk_profiles (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL UNIQUE REFERENCES users(id),
 daily_loss_limit NUMERIC(18,2), max_trades INTEGER NOT NULL DEFAULT 3, max_quantity INTEGER,
 max_capital_allocation NUMERIC(18,2), enabled BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS orders (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id),
 account_id UUID NOT NULL REFERENCES broker_accounts(id), signal_id UUID REFERENCES signals(id),
 broker_order_id TEXT, symbol TEXT NOT NULL, side TEXT NOT NULL CHECK(side IN ('BUY','SELL')),
 order_type TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity > 0), price NUMERIC(18,6),
 status TEXT NOT NULL DEFAULT 'CREATED', execution_mode TEXT NOT NULL CHECK(execution_mode IN ('MANUAL','AUTOMATED')),
 idempotency_key TEXT UNIQUE, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_orders_account_status ON orders(account_id,status);
CREATE TABLE IF NOT EXISTS order_events (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_id UUID NOT NULL REFERENCES orders(id),
 event_type TEXT NOT NULL, event_data JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS positions (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), account_id UUID NOT NULL REFERENCES broker_accounts(id),
 instrument_id UUID NOT NULL REFERENCES instruments(id), quantity INTEGER NOT NULL, average_price NUMERIC(18,6),
 last_synced_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE(account_id,instrument_id)
);
CREATE TABLE IF NOT EXISTS holdings (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), account_id UUID NOT NULL REFERENCES broker_accounts(id),
 instrument_id UUID NOT NULL REFERENCES instruments(id), quantity INTEGER NOT NULL, average_price NUMERIC(18,6),
 last_synced_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE(account_id,instrument_id)
);
CREATE TABLE IF NOT EXISTS trade_journal (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id),
 order_id UUID REFERENCES orders(id), realized_pnl NUMERIC(18,2), notes TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS backtest_runs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID REFERENCES users(id), strategy_id UUID REFERENCES strategies(id),
 start_date DATE, end_date DATE, metrics JSONB NOT NULL DEFAULT '{}', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS notifications (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id),
 message TEXT NOT NULL, category TEXT, read_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS audit_logs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID REFERENCES users(id), action TEXT NOT NULL,
 resource_type TEXT, resource_id UUID, metadata JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
