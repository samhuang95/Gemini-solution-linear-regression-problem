import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # For Windows
plt.rcParams['axes.unicode_minus'] = False # To display minus sign correctly

st.title("線性迴歸模擬器")

st.sidebar.header("參數設定")

# 1. 業務理解 (Business Understanding) - 假設我們要預測學習時數與考試分數的關係

# 2. 資料理解 (Data Understanding) & 3. 資料準備 (Data Preparation)
# 建立模擬資料 (學習時數 vs 考試分數)
n_samples = st.sidebar.slider("資料點數量 (n)", 100, 5000, 1000)
slope_a = st.sidebar.slider("斜率 (a)", -10.0, 10.0, 2.0)
noise_var = st.sidebar.slider("雜訊變異數 (var)", 0, 1000, 100)

# Generate data
X = np.random.rand(n_samples, 1) * 10  # 學習時數 (0-10)
true_y = slope_a * X + 5  # 假設截距為 5
noise = np.random.normal(0, np.sqrt(noise_var), (n_samples, 1))
y = true_y + noise

st.subheader("模擬資料概覽")
st.write(f"資料點數量: {n_samples}")
st.write(f"真實斜率 (a): {slope_a}")
st.write(f"雜訊變異數: {noise_var}")

# 4. 建模 (Modeling)
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# 5. 評估 (Evaluation)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# 離群值檢測 (Outlier Detection)
residuals = y - y_pred
Q1 = np.percentile(residuals, 25)
Q3 = np.percentile(residuals, 75)
IQR = Q3 - Q1
outlier_indices = np.where((residuals < (Q1 - 1.5 * IQR)) | (residuals > (Q3 + 1.5 * IQR)))[0]

st.subheader("模型評估結果")
st.write(f"均方誤差 (MSE): {mse:.2f}")
st.write(f"決定係數 (R^2): {r2:.2f}")
st.write(f"檢測到的離群值數量: {len(outlier_indices)}")

# 6. 部署 (Deployment) - 使用 matplotlib 畫圖，展示結果
st.subheader("線性迴歸結果視覺化")
fig, ax = plt.subplots()
ax.scatter(X, y, color="blue", label="實際值", alpha=0.6)
ax.plot(X, y_pred, color="red", linewidth=2, label="預測迴歸線")

# 標註離群值
if len(outlier_indices) > 0:
    ax.scatter(X[outlier_indices], y[outlier_indices], color="green", marker="o", s=100, label="離群值")
    for i in outlier_indices:
        ax.annotate(f'({X[i,0]:.1f}, {y[i,0]:.1f})', (X[i,0], y[i,0]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='green')

ax.set_xlabel("學習時數")
ax.set_ylabel("考試分數")
ax.set_title("線性迴歸：學習時數 vs 考試分數")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 顯示 Top 5 離群值
if len(outlier_indices) > 0:
    import pandas as pd
    outlier_data = []
    for i in outlier_indices:
        outlier_data.append({"X": X[i,0], "Y": y[i,0], "Residual": residuals[i,0]})
    
    df_outliers = pd.DataFrame(outlier_data)
    df_outliers["Abs_Residual"] = df_outliers["Residual"].abs()
    df_outliers = df_outliers.sort_values(by="Abs_Residual", ascending=False).head(5)
    
    st.subheader("Top 5 離群值")
    st.dataframe(df_outliers[["X", "Y", "Residual"]].round(2))

st.subheader("模型參數")
st.write(f"模型截距 (Intercept): {model.intercept_[0]:.2f}")
st.write(f"模型係數 (Coefficient): {model.coef_[0][0]:.2f}")
