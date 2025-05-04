import matplotlib.pyplot as plt
import numpy as np

# Giả lập dữ liệu thời gian phản hồi (tính bằng giây) theo độ sâu tìm kiếm
search_depths = np.arange(1, 7)  # Độ sâu từ 1 đến 6
response_times = [0.01, 0.1, 1, 1.5, 5, 20.5]  # Thời gian tương ứng (giả lập)

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(search_depths, response_times, marker='o', linestyle='-', color='blue', linewidth=2)
plt.title('Thời gian phản hồi của AI theo độ sâu tìm kiếm (Minimax + Alpha-Beta)', fontsize=14)
plt.xlabel('Độ sâu tìm kiếm (SEARCH_DEPTH)', fontsize=12)
plt.ylabel('Thời gian phản hồi (giây)', fontsize=12)
plt.grid(True)
plt.xticks(search_depths)
plt.yscale('log')  # Dùng thang log để dễ nhìn khi thời gian tăng nhanh
plt.tight_layout()
plt.show()