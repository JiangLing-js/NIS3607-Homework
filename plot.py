import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


# 给定的数据
success_rates = [1e-7, 1e-6, 1e-5, 1e-4]
growth_rates = [0.0040, 0.0410, 0.3945, 0.9960]

# 创建插值函数
f = interp1d(success_rates, growth_rates, kind='cubic')

# 生成更密集的数据点
success_rates_dense = np.logspace(-7, -4, 100)
growth_rates_dense = f(success_rates_dense)

# 绘制原始数据散点图
plt.scatter(success_rates, growth_rates, label='Original Data', color='red')

# 绘制插值后的曲线
plt.plot(success_rates_dense, growth_rates_dense, label='Interpolated Curve', color='blue')

plt.xscale('log')  # 设置 x 轴为对数坐标轴
plt.xlabel('Success Rates')
plt.ylabel('Growth Rates')
plt.title('Function Plot')
plt.legend()
plt.grid(True)
plt.show()
