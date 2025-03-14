"""
说明：

在PDFJoint基础上改进一点，在PDF1的指定页数之后，插入PDF2的指定页数。
"""

import os
from PyPDF2 import PdfReader, PdfWriter

def insert_pdf_between_pages(
    pdf1_path,
    pdf2_path,
    insert_after_page,
    output_path,
    pdf2_start_page=0,
    pdf2_end_page=None
):
    """
    将 pdf2 的指定页数插入到 pdf1 的指定页数之后

    :param pdf1_path: pdf1 的文件路径
    :param pdf2_path: pdf2 的文件路径
    :param insert_after_page: 在 pdf1 的哪一页之后插入 pdf2
    :param output_path: 输出的合并后的 PDF 文件路径
    :param pdf2_start_page: pdf2 的起始页码（默认为 0，表示第一页）
    :param pdf2_end_page: pdf2 的结束页码（默认为 None，表示最后一页）
    """

    # 检查
    if not os.path.exists(pdf1_path):
        raise FileNotFoundError(f"文件 {pdf1_path} 不存在")
    if not os.path.exists(pdf2_path):
        raise FileNotFoundError(f"文件 {pdf2_path} 不存在")

    pdf1_reader = PdfReader(pdf1_path)
    pdf2_reader = PdfReader(pdf2_path)

    pdf_writer = PdfWriter()

    # 获取各自的len
    pdf1_num_pages = len(pdf1_reader.pages)
    pdf2_num_pages = len(pdf2_reader.pages)

    # 检查插入位置
    if insert_after_page < 0 or insert_after_page >= pdf1_num_pages:
        raise ValueError(f"插入报错，pdf1 共有 {pdf1_num_pages} 页")

    # 处理 pdf2 的页数范围
    if pdf2_end_page is None:
        pdf2_end_page = pdf2_num_pages
    if pdf2_start_page < 0 or pdf2_end_page > pdf2_num_pages or pdf2_start_page > pdf2_end_page:
        raise ValueError(f"pdf2 的页数范围有问题，pdf2 共有 {pdf2_num_pages} 页")

    # 将 pdf1 的页面添加到 pdf_writer，直到指定的插入位置
    for page_num in range(insert_after_page + 1):
        pdf_writer.add_page(pdf1_reader.pages[page_num])

    # 将 pdf2 的指定页面添加到 pdf_writer
    for page_num in range(pdf2_start_page, pdf2_end_page):
        pdf_writer.add_page(pdf2_reader.pages[page_num])

    # 将 pdf1 剩余的页面添加到 pdf_writer
    for page_num in range(insert_after_page + 1, pdf1_num_pages):
        pdf_writer.add_page(pdf1_reader.pages[page_num])

    # 输出
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Success: {output_path}")

if __name__ == "__main__":

    pdf1_path = './TestFiles/file1.pdf'
    pdf2_path = './TestFiles/file1.pdf'

    # 指定在 pdf1 的哪一页之后插入 pdf2
    insert_after_page = 2

    # 输出路径
    output_path = './MergedFiles/mergedTest.pdf'

    # 指定插入 pdf2 的页数范围（默认插入全部）
    pdf2_start_page = 0  # pdf2 的起始页码
    pdf2_end_page = None  # pdf2 的结束页码（None 表示到最后一页）

    # 调用
    insert_pdf_between_pages(
        pdf1_path,
        pdf2_path,
        insert_after_page,
        output_path,
        pdf2_start_page,
        pdf2_end_page
    )