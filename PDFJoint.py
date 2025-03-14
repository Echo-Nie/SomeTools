import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(input_paths, output_path):
    """
    拼接多个 PDF 文件

    :param input_paths: 输入的 PDF 文件路径列表
    :param output_path: 输出的合并后的 PDF 文件路径
    """

    pdf_writer = PdfWriter()

    # 遍历
    for pdf_path in input_paths:
        if not os.path.exists(pdf_path):
            print(f"文件 {pdf_path} 不存在，滚")
            continue

        # 打开 PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)

            # 将每一页添加到 PdfWriter
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

    # 输出
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Success: {output_path}")

if __name__ == "__main__":
    input_pdfs = ['./TestFiles/file1.pdf', './TestFiles/file2.pdf']
    output_pdf = './MergedFiles/merged.pdf'
    merge_pdfs(input_pdfs, output_pdf)