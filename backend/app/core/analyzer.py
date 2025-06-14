import pandas as pd


def normalize_price(df):
    df = df.copy()

    base_open = df["open"].iloc[0]
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].apply(lambda x: (x - base_open) / base_open + 1)
    return df

def compute_strength(symbol_dfs):
    strength = {}
    for symbol, df in symbol_dfs.items():
        df = normalize_price(df)
        # plotalized_candlestick(df, symbol)

        strength[symbol] = df["close"].iloc[-1] - 1  # 누적 수익률 %
    return sorted(strength.items(), key=lambda x: x[1], reverse=True)
