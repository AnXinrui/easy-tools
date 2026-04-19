from PIL import Image
import os

TARGET_SIZE_MB = 1
TARGET_SIZE_BYTES = TARGET_SIZE_MB * 1024 * 1024

def compress_image(input_path, output_path, target_bytes=TARGET_SIZE_BYTES):
    """
    压缩图片大小到接近目标大小（默认1MB）
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param target_bytes: 目标文件大小（字节）
    """
    img = Image.open(input_path)
    original_size = os.path.getsize(input_path)
    print(f"原始大小: {original_size / 1024 / 1024:.2f} MB")

    # 如果已经小于目标大小，直接保存
    if original_size <= target_bytes:
        img.save(output_path, quality=95)
        print(f"图片已小于目标大小，无需压缩")
        return

    # 根据扩展名决定保存格式
    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        fmt = "JPEG"
    elif ext == ".webp":
        fmt = "WEBP"
    else:
        # 默认输出为 JPEG（压缩效果最好）
        fmt = "JPEG"
        if not ext:
            output_path += ".jpg"

    # 确保图片为 RGB 模式（JPEG 不支持 alpha 通道）
    if img.mode in ("RGBA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为 mask
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # 第一步：通过调整 quality 参数压缩
    low, high = 10, 95
    best_result = None
    best_size = original_size

    while low <= high:
        mid = (low + high) // 2
        temp_path = output_path + ".tmp"
        try:
            img.save(temp_path, format=fmt, quality=mid)
            result_size = os.path.getsize(temp_path)
        except Exception:
            low = mid + 1
            continue

        if result_size <= target_bytes:
            best_result = temp_path
            best_size = result_size
            low = mid + 1  # 尝试更高质量
        else:
            high = mid - 1

        os.remove(temp_path)

    if best_result:
        img.save(output_path, format=fmt, quality=(low + high) // 2 + 1 if (low + high) // 2 + 1 <= 95 else (low + high) // 2)
        final_size = os.path.getsize(output_path)
        print(f"质量调整压缩完成: {final_size / 1024 / 1024:.2f} MB")
        if final_size <= target_bytes:
            return

    # 第二步：如果调整质量仍不够，缩小图片尺寸
    scale = 0.9
    while scale >= 0.1:
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        resized = img.resize((new_width, new_height), Image.LANCZOS)

        temp_path = output_path + ".tmp"
        resized.save(temp_path, format=fmt, quality=85)
        result_size = os.path.getsize(temp_path)
        os.remove(temp_path)

        if result_size <= target_bytes:
            resized.save(output_path, format=fmt, quality=85)
            final_size = os.path.getsize(output_path)
            print(f"尺寸缩放压缩完成 (缩放比例: {scale:.1f}): {final_size / 1024 / 1024:.2f} MB")
            return

        scale -= 0.1

    # 最后兜底：用最小尺寸和最低质量保存
    final_width = int(img.width * 0.1)
    final_height = int(img.height * 0.1)
    resized = img.resize((final_width, final_height), Image.LANCZOS)
    resized.save(output_path, format=fmt, quality=10)
    final_size = os.path.getsize(output_path)
    print(f"最终压缩结果: {final_size / 1024 / 1024:.2f} MB")


def compress_images_in_folder(input_folder, output_folder, target_bytes=TARGET_SIZE_BYTES):
    """
    批量压缩文件夹中的图片
    :param input_folder: 输入图片文件夹
    :param output_folder: 输出图片文件夹
    :param target_bytes: 目标文件大小（字节）
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    supported_ext = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_ext)]

    if not files:
        print(f"在 {input_folder} 中未找到支持的图片文件")
        return

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        # 输出统一使用 .jpg 格式以获得更好的压缩效果
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name_without_ext}.jpg")
        print(f"\n正在处理: {filename}")
        compress_image(input_path, output_path, target_bytes)

    print(f"\n全部压缩完成！")


# 使用示例
if __name__ == "__main__":
    compress_images_in_folder("input", "output")
