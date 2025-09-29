# app.py

"""
依照 CRISP-DM 流程解決線性回歸問題
流程：
1. 業務理解 (Business Understanding)
2. 資料理解 (Data Understanding)
3. 資料準備 (Data Preparation)
4. 建模 (Modeling)
5. 評估 (Evaluation)
6. 部署 (Deployment)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 業務理解 (Business Understanding)
# 假設我們要預測學習時數與考試分數的關係

# 2. 資料理解 (Data Understanding)
# 建立模擬資料 (學習時數 vs 考試分數)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)  # 學習時數
y = np.array([10, 20, 25, 40, 45, 50, 65, 70, 80, 95])       # 考試分數

# 3. 資料準備 (Data Preparation)
# 這裡的資料已經是乾淨數據，不需要額外清理

# 4. 建模 (Modeling)
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# 5. 評估 (Evaluation)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print("模型評估結果：")
print(f"均方誤差 (MSE): {mse:.2f}")
print(f"決定係數 (R^2): {r2:.2f}")

# 6. 部署 (Deployment)
# 使用 matplotlib 畫圖，展示結果
plt.scatter(X, y, color="blue", label="實際值")
plt.plot(X, y_pred, color="red", linewidth=2, label="預測迴歸線")
plt.xlabel("學習時數")
plt.ylabel("考試分數")
plt.title("線性回歸：學習時數 vs 考試分數")
plt.legend()
plt.grid(True)
plt.show()
