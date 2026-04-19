# easy-tools

日常小工具集合，每个子目录是一个独立工具。

## 工具列表

| 目录 | 功能 | 依赖 |
|------|------|------|
| `pdf2png/` | 将 PDF 逐页转换为 PNG 图片 | pdf2image, Pillow |
| `compress/` | 将图片压缩到指定大小（默认 ~1MB） | Pillow |

## 快速使用

所有工具均使用 [uv](https://docs.astral.sh/uv/) 管理 Python 环境和依赖。

### pdf2png — PDF 转图片

```bash
cd pdf2png
uv sync                  # 安装依赖
uv run python pdf2png.py # 运行
```

将 PDF 文件放入 `input/`，转换结果输出到 `output_images/`。

### compress — 图片压缩

```bash
cd compress
uv sync                      # 安装依赖
uv run python compress.py    # 运行
```

将图片放入 `input/`，压缩结果输出到 `output/`。

自定义目标大小：

```python
from compress import compress_image

compress_image("input/photo.png", "output/photo.jpg", target_bytes=500*1024)  # 500KB
```

## 备注

- `pdf2image` 需要系统安装 [poppler](https://poppler.freedesktop.org/)：`brew install poppler`
- 各工具的 `input/` 目录存放待处理文件，`output*/` 目录存放结果，均已 gitignore
