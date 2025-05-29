from flask import Blueprint, request, render_template
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.losses import MeanSquaredError
import joblib
from datetime import timedelta

du_bao_bp = Blueprint("du_bao", __name__)

@du_bao_bp.route("/du-bao", methods=["GET"])
def du_bao():
    san = request.args.get("san")
    ma = request.args.get("ma")
    so_ngay = int(request.args.get("so_ngay", 30))

    duong_dan_file = f"du_lieu/{san}/csv/{ma}.csv"
    if not os.path.exists(duong_dan_file):
        return f"Không tìm thấy dữ liệu cho {ma} thuộc {san}", 404

    ten_tep = f"{san}_{ma}"
    model_path = f"mo_hinh/lstm_models/{ten_tep}.h5"
    scaler_path = f"mo_hinh/lstm_models/{ten_tep}_scaler.pkl"

    df = pd.read_csv(duong_dan_file)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    data = df['Close'].values.reshape(-1, 1)

    if len(data) < 90:
        return f"Dữ liệu cho {ma} quá ít để huấn luyện", 400

    if not os.path.exists(model_path):
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        X, y = [], []
        for i in range(60, len(data_scaled)):
            X.append(data_scaled[i - 60:i])
            y.append(data_scaled[i])
        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(60, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss=MeanSquaredError())
        model.fit(X, y, epochs=5, batch_size=32, verbose=0)

        os.makedirs("mo_hinh/lstm_models", exist_ok=True)
        model.save(model_path)
        joblib.dump(scaler, scaler_path)
    else:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)

    data_scaled = scaler.transform(data)
    input_data = data_scaled[-60:]
    du_doan = []

    for _ in range(so_ngay):
        X = input_data[-60:].reshape(1, 60, 1)
        pred = model.predict(X, verbose=0)[0][0]
        du_doan.append(float(pred))
        input_data = np.vstack((input_data, [[pred]]))

    gia_du_bao = scaler.inverse_transform(np.array(du_doan).reshape(-1, 1)).flatten().tolist()
    gia_thuc_te = scaler.inverse_transform(data_scaled).flatten().tolist()

    # Biểu đồ nến
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    ngay_lich_su = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    open_gia = df['Open'].astype(float).tolist()
    high_gia = df['High'].astype(float).tolist()
    low_gia = df['Low'].astype(float).tolist()
    close_gia = df['Close'].astype(float).tolist()


    # Trục thời gian định dạng ISO cho Plotly
    ngay_thuc_te = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    last_date = df['Date'].iloc[-1]
    ngay_du_bao = [(last_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, so_ngay + 1)]

    return render_template(
        "du_bao.html",
        san=san,
        ma=ma,
        so_ngay=so_ngay,
        ngay_thuc_te=ngay_thuc_te,
        gia_thuc_te=gia_thuc_te,
        ngay_du_bao=ngay_du_bao,
        gia_du_bao=gia_du_bao,
        ngay_lich_su=ngay_lich_su,
        open_gia=open_gia,
        high_gia=high_gia,
        low_gia=low_gia,
        close_gia=close_gia
    )
