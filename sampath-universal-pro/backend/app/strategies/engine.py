import pandas as pd
from .indicators import ema, rsi, macd, atr, vwap

STRATEGIES = [
    {"id":"ema_9_21", "name":"EMA 9/21 Crossover", "category":"Trend", "timeframes":["5m","15m","1h"]},
    {"id":"ema_20_50", "name":"EMA 20/50 Trend", "category":"Trend", "timeframes":["15m","1h","1d"]},
    {"id":"rsi_14", "name":"RSI Momentum", "category":"Momentum", "timeframes":["5m","15m","1h"]},
    {"id":"macd_cross", "name":"MACD Crossover", "category":"Momentum", "timeframes":["15m","1h","1d"]},
    {"id":"vwap_reclaim", "name":"VWAP Reclaim", "category":"Intraday", "timeframes":["1m","5m","15m"]},
    {"id":"orb_15", "name":"15-minute Opening Range Breakout", "category":"Breakout", "timeframes":["5m","15m"]},
    {"id":"atr_volatility", "name":"ATR Volatility Expansion", "category":"Volatility", "timeframes":["5m","15m","1h"]},
]

def analyze(df: pd.DataFrame, symbol: str, strategy_id: str) -> dict:
    required = {"open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns) or len(df) < 55:
        raise ValueError("Provide at least 55 OHLCV candles with open/high/low/close/volume columns.")
    close = df.close.astype(float)
    direction, reason, score = "NEUTRAL", "No confirmed setup", 0
    if strategy_id == "ema_9_21":
        fast, slow = ema(close, 9), ema(close, 21)
        if fast.iloc[-1] > slow.iloc[-1] and fast.iloc[-2] <= slow.iloc[-2]: direction, reason, score = "BUY", "EMA 9 crossed above EMA 21", 70
        elif fast.iloc[-1] < slow.iloc[-1] and fast.iloc[-2] >= slow.iloc[-2]: direction, reason, score = "SELL", "EMA 9 crossed below EMA 21", 70
    elif strategy_id == "ema_20_50":
        fast, slow = ema(close, 20), ema(close, 50)
        if fast.iloc[-1] > slow.iloc[-1]: direction, reason, score = "BULLISH", "EMA 20 above EMA 50", 65
        elif fast.iloc[-1] < slow.iloc[-1]: direction, reason, score = "BEARISH", "EMA 20 below EMA 50", 65
    elif strategy_id == "rsi_14":
        value = float(rsi(close).iloc[-1])
        if value < 30: direction, reason, score = "WATCH_BUY", f"RSI oversold: {value:.1f}", 60
        elif value > 70: direction, reason, score = "WATCH_SELL", f"RSI overbought: {value:.1f}", 60
        else: reason = f"RSI neutral: {value:.1f}"
    elif strategy_id == "macd_cross":
        line, sig, _ = macd(close)
        if line.iloc[-1] > sig.iloc[-1] and line.iloc[-2] <= sig.iloc[-2]: direction, reason, score = "BUY", "MACD bullish crossover", 70
        elif line.iloc[-1] < sig.iloc[-1] and line.iloc[-2] >= sig.iloc[-2]: direction, reason, score = "SELL", "MACD bearish crossover", 70
    elif strategy_id == "vwap_reclaim":
        vw = vwap(df)
        if close.iloc[-1] > vw.iloc[-1] and close.iloc[-2] <= vw.iloc[-2]: direction, reason, score = "WATCH_BUY", "Price reclaimed session VWAP", 65
        elif close.iloc[-1] < vw.iloc[-1] and close.iloc[-2] >= vw.iloc[-2]: direction, reason, score = "WATCH_SELL", "Price lost session VWAP", 65
    elif strategy_id == "orb_15":
        opening_high = float(df.high.iloc[:3].max())
        opening_low = float(df.low.iloc[:3].min())
        if close.iloc[-1] > opening_high: direction, reason, score = "WATCH_BUY", "Close above supplied first-three-candle range", 65
        elif close.iloc[-1] < opening_low: direction, reason, score = "WATCH_SELL", "Close below supplied first-three-candle range", 65
    elif strategy_id == "atr_volatility":
        a = atr(df)
        if a.iloc[-1] > a.iloc[-2] * 1.15: direction, reason, score = "VOLATILITY_EXPANSION", "ATR increased by more than 15% vs prior candle", 55
    return {"symbol": symbol, "strategy_id": strategy_id, "direction": direction, "score": score, "reference_price": round(float(close.iloc[-1]), 2), "reason": reason, "is_trade_recommendation": False}
