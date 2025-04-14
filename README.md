# Business Card Info Scraper

This project is used to extract content from various business cards and retrieve precise information such as names, titles, phone numbers, email addresses, and company names.

## Description

The Business Card Info Scraper automates the process of extracting structured information from unstructured business card images or text. This is particularly useful when dealing with a large number of business cards and needing to digitize the details efficiently.

## Files

- `main.py`: Core Python script that performs the extraction and parsing of business card data.

## Libraries Used

This project uses the following Python libraries:
- `os`
- `re`
- `pytesseract` - OCR tool to extract text from images
- `PIL` (Python Imaging Library) - to handle image opening and conversion

## How to Install Dependencies

Make sure you have Python installed. Then run:

```bash
pip install pytesseract pillow
```

Also ensure that [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) is installed on your system.

## How to Run

To execute the script:

```bash
python main.py
```

Ensure that your input images (business card scans) are placed correctly in the script or updated in the code before running.

## License

This project is licensed under the MIT License.