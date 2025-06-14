# app/api/v1/rs.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
import pandas as pd

from app.core.fetcher import fetch_binance_klines
from app.core.analyzer import compute_strength

router = APIRouter(prefix="/v1", tags=["relative-strength"])

@router.get("/relative-strength", response_model=List[dict])
def get_relative_strength(
    tickers: str = Query(..., description="Comma-separated list of symbols"),
    interval: str = Query("5m", description="Kline interval, e.g., 1m,5m,15m,1h,4h"),
    limit: int = Query(400, ge=1, le=1000, description="Number of klines to fetch"),
):
    """
    Compute and return relative strength for given tickers.
    """
    symbols = [s.strip().upper() for s in tickers.split(',') if s.strip()]
    if not symbols:
        raise HTTPException(status_code=400, detail="No tickers provided")

    symbol_dfs = {}
    for symbol in symbols:
        try:
            df = fetch_binance_klines(symbol, interval, limit=limit)
            symbol_dfs[symbol] = df
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error fetching data for {symbol}: {e}")

    # Compute strength
    try:
        strength_list = compute_strength(symbol_dfs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing strength: {e}")

    # Format result
    result = [{"symbol": sym, "strength": float(str_val * 100)} for sym, str_val in strength_list]
    return result
