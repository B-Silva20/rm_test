# rmtest OpenCV 实验项目

本项目是基于 Python 3.11 和 OpenCV 的基础视觉实验集合，内容包括图像读取显示、HSV 颜色分割、轮廓检测、最小框选、多边形拟合、视频目标跟踪以及 `solvePnP` 物体位姿解算。

本项目根目录：

```text
C:\Users\Jiang Haoru\Desktop\bjtu\25-26-2\rmtest
```

## 环境要求

- Python 3.11
- opencv-python
- opencv-contrib-python
- numpy

安装依赖：

```bash
pip install opencv-python opencv-contrib-python numpy
```

## 项目结构

```text
rmtest/
├── README.md
├── test0.py
├── test0.jpg
├── test1.py
├── test1.png
├── test1_out.png
├── test2.py
├── test2.png
├── test2_out.png
├── additional_test.py
├── additional_test.mp4
├── test3.py
├── test3.mp4
├── test3_out.mp4
└── .idea/
```

## 实验内容

### 1. OpenCV 图像读取与显示

对应文件：

- `test0.py`
- `test0.jpg`

功能说明：

`test0.py` 使用 `cv2.imread()` 读取 `test0.jpg`，并通过 `cv2.imshow()` 显示图像，是 OpenCV 图像读取和窗口显示的基础实验。

运行方式：

```bash
python test0.py
```

### 2. HSV 颜色分割

对应文件：

- `test1.py`
- `test1.png`
- `test1_out.png`

功能说明：

`test1.py` 读取 `test1.png`，将 BGR 图像转换为 HSV 色彩空间，并分别对 H、S、V 三个通道建立掩膜。随后通过 `cv2.bitwise_and()` 融合掩膜，实现对粉色目标区域的颜色分割。

核心步骤：

- 使用 `cv2.cvtColor()` 完成 BGR 到 HSV 的转换
- 使用 `cv2.split()` 分离 H、S、V 通道
- 使用 `cv2.inRange()` 构建颜色掩膜
- 使用 `cv2.bitwise_and()` 输出目标区域
- 使用 `cv2.imwrite()` 保存结果

运行方式：

```bash
python test1.py
```

输出文件：

```text
test1_out.png
```

### 3. 最小框选与多边形拟合

对应文件：

- `test2.py`
- `test2.png`
- `test2_out.png`

功能说明：

`test2.py` 读取 `test2.png`，对图像中的青白色箭头状灯条进行检测。程序先通过 HSV 颜色分割提取灯条区域，再使用轮廓检测、多边形拟合、面积筛选和边界框合并，最终用红色矩形框标出目标灯条。

核心步骤：

- 使用 HSV 阈值提取青白色灯条
- 使用形态学闭运算连接断裂区域
- 使用 `cv2.findContours()` 查找轮廓
- 使用 `cv2.contourArea()` 进行面积筛选
- 使用 `cv2.approxPolyDP()` 进行多边形拟合
- 使用 `cv2.boundingRect()` 计算最小外接矩形
- 合并重复框选区域，并在原始掩膜中重新收紧边界

运行方式：

```bash
python test2.py
```

输出文件：

```text
test2_out.png
```

### 4. 视频中的橙色目标跟踪

对应文件：

- `additional_test.py`
- `additional_test.mp4`

功能说明：

`additional_test.py` 读取 `additional_test.mp4`，对灰白色桌面上的橙色目标进行实时检测。程序逐帧进行 HSV 颜色分割，提取橙色区域，并对最大轮廓进行多边形拟合和矩形框选。

核心步骤：

- 使用 `cv2.VideoCapture()` 读取视频
- 对每一帧进行 HSV 颜色分割
- 使用形态学开闭运算优化掩膜
- 使用 `cv2.findContours()` 查找橙色目标轮廓
- 使用 `cv2.approxPolyDP()` 拟合目标轮廓
- 使用 `cv2.boundingRect()` 绘制红色外接矩形
- 使用 `cv2.imshow()` 实时显示处理结果

运行方式：

```bash
python additional_test.py
```

操作说明：

- 按 `q` 退出视频窗口

### 5. solvePnP 物体位姿解算

对应文件：

- `test3.py`
- `test3.mp4`
- `test3_out.mp4`

功能说明：

`test3.py` 读取竖屏 4K 60fps 视频 `test3.mp4`，检测白纸上的黑色矩形，并使用 OpenCV 的 `cv2.solvePnP()` 对矩形进行物体位姿解算。程序会将解算得到的三维坐标轴重新投影到视频画面中，并保存处理后的视频。

矩形真实尺寸：

```text
4 cm × 3 cm
```

核心步骤：

- 逐帧读取 `test3.mp4`
- 灰度化并进行高斯模糊
- 使用阈值提取黑色矩形线框
- 使用形态学闭运算连接矩形边缘
- 使用 `cv2.findContours()` 查找轮廓
- 使用 `cv2.approxPolyDP()` 筛选四边形轮廓
- 对四个角点进行排序
- 使用 `cv2.solvePnP()` 求解旋转向量 `rvec` 和平移向量 `tvec`
- 使用 `cv2.projectPoints()` 将三维坐标轴投影回图像
- 使用 `cv2.VideoWriter()` 保存输出视频

运行方式：

```bash
python test3.py
```

输出文件：

```text
test3_out.mp4
```

可视化说明：

- 绿色线条：检测到的矩形轮廓
- 红色矩形：目标区域的最小外接框
- 红色坐标轴：X 轴
- 绿色坐标轴：Y 轴
- 蓝色坐标轴：Z 轴
- 画面左上角文本：`solvePnP` 解算得到的平移向量 `tvec`

## 注意事项

1. 所有脚本都使用相对路径读取输入文件，请在项目根目录下运行。
2. 如果 `cv2.imshow()` 窗口没有正常显示，请确认当前运行环境支持图形窗口。
3. 视频处理脚本运行时可按 `q` 提前退出。
4. `test3.py` 中的相机内参使用视频分辨率构造近似值，畸变系数设置为 0，因此位姿方向可用于实验展示，但平移距离精度不等同于经过相机标定后的真实测量结果。
5. `test1.py`、`test2.py` 和 `additional_test.py` 中的 HSV 阈值与当前素材相关，如果更换输入图片或视频，可能需要重新调整阈值范围。

## 输出结果

项目中已包含部分实验输出：

- `test1_out.png`：颜色分割结果
- `test2_out.png`：灯条框选结果
- `test3_out.mp4`：矩形位姿解算可视化视频
