# train_model/train_lstm_all.py

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# ==== Cấu hình ====
thu_muc_du_lieu = "du_lieu"
thu_muc_luu = "mo_hinh/lstm_models"
so_ngay_dung = 60

# ==== Tạo thư mục lưu nếu chưa có ====
os.makedirs(thu_muc_luu, exist_ok=True)

# ==== Tạo dữ liệu cho LSTM ====
def tao_du_lieu(data, buoc=60):
    X, y = [], []
    for i in range(buoc, len(data)):
        X.append(data[i-buoc:i])
        y.append(data[i])
    return np.array(X), np.array(y)

# ==== Huấn luyện mô hình cho từng mã cổ phiếu ====
def huan_luyen_cho_file(file_csv, ten_san, ten_ma):
    try:
        df = pd.read_csv(file_csv)
        if 'Close' not in df.columns:
            print(f"Bỏ qua {ten_ma} vì thiếu cột 'Close'")
            return
        data = df['Close'].values.reshape(-1, 1)

        # Chuẩn hóa
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        X, y = tao_du_lieu(data_scaled, so_ngay_dung)
        if len(X) == 0:
            print(f"Không đủ dữ liệu để huấn luyện {ten_ma}")
            return
        X = X.reshape((X.shape[0], X.shape[1], 1))

        # Mô hình
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        from tensorflow.keras.losses import MeanSquaredError
        model.compile(optimizer='adam', loss=MeanSquaredError())
        model.fit(X, y, epochs=5, batch_size=32, verbose=0)

        # Lưu mô hình
        ten_tep = f"{ten_san}_{ten_ma}".replace(".csv", "")
        model.save(os.path.join(thu_muc_luu, f"{ten_tep}.h5"))
        joblib.dump(scaler, os.path.join(thu_muc_luu, f"{ten_tep}_scaler.pkl"))
        print(f"Đã huấn luyện {ten_tep}")
    except Exception as e:
        print(f"Lỗi {ten_ma}: {e}")

# ==== Quét toàn bộ thư mục dữ liệu ====
for ten_san in os.listdir(thu_muc_du_lieu):
    thu_muc_csv = os.path.join(thu_muc_du_lieu, ten_san, "csv")
    if not os.path.exists(thu_muc_csv):
        continue
    for ten_ma in os.listdir(thu_muc_csv):
        duong_dan_file = os.path.join(thu_muc_csv, ten_ma)
        if duong_dan_file.endswith(".csv"):
            huan_luyen_cho_file(duong_dan_file, ten_san, ten_ma)
