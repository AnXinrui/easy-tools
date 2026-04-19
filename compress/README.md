# compress - 图片压缩工具

将图片压缩到指定大小（默认约 1MB），支持批量处理。

## 功能特点

- 自动调整 JPEG quality 参数压缩，尽量保留原始分辨率
- 质量调整不够时，逐步缩放图片尺寸直到满足目标大小
- 自动处理 RGBA/透明通道，转为白底 JPEG 输出
- 支持批量处理整个文件夹

## 环境准备

```bash
cd compress
uv sync
```

## 使用方式

### 批量压缩（默认 input → output）

```bash
uv run python compress.py
```

将待压缩图片放入 `input/` 文件夹，压缩结果输出到 `output/` 文件夹。

### 自定义调用

```python
from compress import compress_image, compress_images_in_folder

# 压缩单张图片
compress_image("input/photo.png", "output/photo.jpg")

# 压缩到 500KB
compress_image("input/photo.png", "output/photo.jpg", target_bytes=500*1024)

# 批量压缩，目标 2MB
compress_images_in_folder("input", "output", target_bytes=2*1024*1024)
```

## 压缩策略

1. **调整质量** — 二分法搜索最优 JPEG quality 值，在不超过目标大小的前提下尽量高质量
2. **缩放尺寸** — 若质量降到最低仍超出目标，按 0.1 步长逐步缩小图片
3. **兜底处理** — 极端情况下降到 10% 尺寸 + quality=10

## 支持格式

| 输入 | 输出 |
|------|------|
| PNG / JPG / JPEG / WebP / BMP / TIFF | JPG |
