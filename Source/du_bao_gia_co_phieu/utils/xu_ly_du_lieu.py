import os
import pandas as pd

def lay_du_lieu_theo_ma(san, ma):
    duong_dan = f'du_lieu/{san}/csv/{ma}.csv'
    df = pd.read_csv(duong_dan)
    df['Ngày'] = pd.to_datetime(df['Date'])
    df = df.rename(columns={
        'Open': 'Mở cửa',
        'High': 'Cao nhất',
        'Low': 'Thấp nhất',
        'Close': 'Đóng cửa',
        'Volume': 'Khối lượng'
    })
    df = df[['Ngày', 'Mở cửa', 'Cao nhất', 'Thấp nhất', 'Đóng cửa', 'Khối lượng']].dropna()
    df = df.sort_values('Ngày')
    return df

def lay_danh_sach_ma(san: str) -> list:
    thu_muc = os.path.join("du_lieu", san, "csv")
    if not os.path.exists(thu_muc):
        return []
    danh_sach = [f.replace(".csv", "") for f in os.listdir(thu_muc) if f.endswith(".csv")]
    return sorted(danh_sach)