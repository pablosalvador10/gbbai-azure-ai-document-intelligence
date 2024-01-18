import io
import os

import fitz  # the PyMuPDF module
import matplotlib.pyplot as plt
import tabula
from PIL import Image, UnidentifiedImageError


def save_table_as_image(df, image_path):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

    plt.savefig(image_path)


def extract_images(pdf_path, output_folder):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # If no output folder is provided, use the current directory
    if output_folder is None:
        output_folder = os.getcwd()
    # If the output folder does not exist, create it
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_num+1}")
        else:
            print("[!] No images found on page", page_num + 1)

        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            try:
                image = Image.open(io.BytesIO(image_bytes))
                image_save_path = os.path.join(
                    output_folder,
                    f"{base_name}_image_page_{page_num+1}_{image_index}.{image_ext}",
                )
                image.save(image_save_path)
                print(
                    f"Saved image {image_index} from page {page_num+1} as {image_save_path}"
                )
            except UnidentifiedImageError:
                print(
                    f"Skipping image {image_index} on page {page_num+1} due to an error."
                )

    doc.close()


def extract_images_and_tables_as_images(pdf_path: str, output_folder: str = None):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # If no output folder is provided, use the current directory
    if output_folder is None:
        output_folder = os.getcwd()
    # If the output folder does not exist, create it
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extracting images
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_num)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            try:
                # Open the image data with PIL
                image = Image.open(io.BytesIO(image_bytes))

                # Save the image with filename including original file name and page number
                image_filename = os.path.join(
                    output_folder,
                    f"{base_name}_image_page_{page_num+1}_{img_index}.png",
                )

                # Save the image using PIL
                image.save(image_filename)
            except UnidentifiedImageError:
                print(f"Skipping image on page {page_num+1} due to an error.")

    # Extracting tables
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

    # Save each table as an image
    for i, table in enumerate(tables):
        table_image_filename = os.path.join(
            output_folder, f"{base_name}_table_page_{i+1}.png"
        )
        save_table_as_image(table, table_image_filename)
