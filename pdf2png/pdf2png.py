from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder):
    """
    将PDF转换为多张图片
    :param pdf_path: PDF文件路径
    :param output_folder: 输出图片的文件夹
    """
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 转换PDF为图片
    images = convert_from_path(pdf_path)
    
    # 保存图片
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path, "PNG")
        print(f"已保存: {image_path}")
    
    print(f"转换完成！共生成 {len(images)} 张图片")

# 使用示例
pdf_to_images("input/a.pdf", "output_images")