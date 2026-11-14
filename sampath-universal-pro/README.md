# SAMPATH UNIVERSAL PRO

Universal multi-broker market-analysis starter (web + installable PWA + FastAPI).

## What is included
- Responsive Next.js dashboard with market overview, scanner, strategy library, broker hub, options workspace and execution controls.
- FastAPI backend with health, broker registry, strategy catalog, signal generation and risk-preview endpoints.
- Broker adapter interfaces for Upstox, Dhan, Zerodha, Angel One and CoinSwitch.
- Initial indicator/strategy calculations (EMA crossover, RSI, MACD, Supertrend-style ATR trend, VWAP and opening-range breakout).
- PostgreSQL starter schema and Docker Compose.
- Manual/demo execution preview with live order submission deliberately disabled.

## Important limitations
This is a runnable starter application, not a production trading service. Broker adapters are integration scaffolds: no live broker credentials, token exchange, market-data entitlement, instrument-master sync or order placement is configured. Never paste broker secrets into frontend code. Live trading must remain disabled until each broker integration is implemented and tested against official documentation, permissions and applicable exchange/SEBI requirements. CoinSwitch is a separate crypto connector and is not an NSE stock broker.

## Run locally
Requirements: Docker Desktop (recommended) or Python 3.11+ and Node.js 20+.

### Docker
```bash
cp .env.example .env
docker compose up --build
```
Frontend: http://localhost:3000  
Backend API: http://localhost:8000  
API docs: http://localhost:8000/docs

### Run without Docker
Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```
Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `frontend/.env.local` if needed.

## Suggested next implementation order
1. Add authentication and per-user authorization.
2. Implement official OAuth/token flows for Upstox, Dhan, Zerodha and Angel One; add CoinSwitch signing separately.
3. Add instrument master and entitled market feeds; normalize timestamps, symbols, lot sizes and tick sizes.
4. Add historical candle storage and robust backtesting with fees, slippage and survivorship-bias controls.
5. Add order state reconciliation and idempotency.
6. Complete security, broker approval and regulatory review before enabling any live order route.

## Safety defaults
- `TRADING_MODE=paper`
- `LIVE_TRADING_ENABLED=false`
- `AUTO_EXECUTION_ENABLED=false`
- Demo order endpoint only returns a preview; it does not submit to a broker.
