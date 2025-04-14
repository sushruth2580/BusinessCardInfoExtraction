
import data as data
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import csv
import os

# Step 1: Convert PDF to Images
pdf_path = '/Users/sushruth.ch/Desktop/pythonProject/12312024.pdf'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

images = convert_from_path(pdf_path, 200)  # Convert PDF to images
image_paths = []
for i, image in enumerate(images):
    image_path = f'{output_folder}/page_{i+1}.jpg'
    image.save(image_path)  # Save individual images
    image_paths.append(image_path)

# Step 2: Process Each Image
all_extracted_text = []
for i, image_path in enumerate(image_paths):
    # Open and preprocess the image
    image = Image.open(image_path)
    grayscale_image = image.convert('L')  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(grayscale_image)
    enhanced_image = enhancer.enhance(2)  # Increase contrast
    denoised_image = enhanced_image.filter(ImageFilter.MedianFilter())  # Remove noise
    processed_image_path = f'{output_folder}/processed_page_{i+1}.jpg'
    denoised_image.save(processed_image_path)  # Save processed image

    # Perform OCR on the processed image
    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"  # Path to Tesseract
    extracted_text = pytesseract.image_to_string(denoised_image, lang='eng')

    # Save extracted text to individual text files
    text_file_path = f'{output_folder}/page_{i+1}.txt'
    with open(text_file_path, 'w') as file:
        file.write(extracted_text)

    # Collect all text
    all_extracted_text.append(extracted_text)

# Step 3: Combine All Extracted Text
combined_text = "\n\n".join(all_extracted_text)
combined_text_file_path = f'{output_folder}/combined_text.txt'
with open(combined_text_file_path, 'w') as file:
    file.write(combined_text)

# Step 4: Extract Information from Combined Text
# Regular expressions for extracting details
names = re.findall(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", combined_text)  # Extract names
company_name = re.findall(r"(Company\sName[:\-]?\s*)([A-Za-z0-9.,'&\s]+)", combined_text)
phone_numbers = re.findall(r"(\(\d{3}\)\s?\d{3}-\d{4}|\d{3}-\d{3}-\d{4})", combined_text)
emails = re.findall(r"(\S+@\S+\.\S+)", combined_text)
address = re.findall(r"(Address[:\-]?\s*)([A-Za-z0-9.,#'\-\s]+)", combined_text)
business_webpage = re.findall(r"https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[\w./?%&=-]*)?", combined_text)
title = re.findall(r"(Title[:\-]?\s*)([A-Za-z0-9\s]+)", combined_text)
roles = re.findall(r"\b(pharmacy|vendor|construction)\b", combined_text, re.IGNORECASE)
# Clean extracted data
names = list(set(names))  # Deduplicate names
company_name = [c[1] for c in company_name]
address = [a[1] for a in address]
title = [t[1] for t in title]

# Step 5: Write Extracted Data to a CSV
data = []
for i in range(max(len(names), len(company_name), len(phone_numbers), len(emails), len(address), len(business_webpage), len(title))):
    data.append({
        "Name": names[i] if i < len(names) else "",
        "Company Name": company_name[i] if i < len(company_name) else "",
        "Phone Number": phone_numbers[i] if i < len(phone_numbers) else "",
        "Email": emails[i] if i < len(emails) else "",
        "Address": address[i] if i < len(address) else "",
        "Business Webpage": business_webpage[i] if i < len(business_webpage) else "",
        "Title": title[i] if i < len(title) else "",
    })

csv_file_path = 'extracted_data.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Company Name", "Phone Number", "Email", "Address", "Business Webpage", "Title"])
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows

print(f"Data successfully written to {csv_file_path}")
print(f"All processed images and text files are saved in {output_folder}")
