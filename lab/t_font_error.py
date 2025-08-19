import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 改成支援中文的字體
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示成方塊

plt.title("測試中文字")
plt.plot([1,2,3],[3,2,1])
plt.show()