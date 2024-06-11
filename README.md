

### README.md

```markdown
# web-to-pdf

A Python project to convert web pages to PDF files using Selenium and ChromeDriver. This project includes functionality to scroll through long web pages, add metadata such as the page title and URL to the generated PDF, and handle multiple URLs efficiently.

## Features

- Convert multiple web pages to PDF files.
- Automatically scroll through long web pages to load all content.
- Add the page title and URL to the bottom of each PDF.
- Handle existing files by overwriting them if the `--force` option is specified.

## Requirements

- Python 3.6+
- Google Chrome
- ChromeDriver
- Selenium
- webdriver-manager

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/web-to-pdf.git
   cd web-to-pdf
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To convert web pages to PDF files, run the `render_multiple_sites_to_pdf.py` script with the desired URLs:

```bash
python render_multiple_sites_to_pdf.py [options] URL [URL ...]
```

### Options

- `--force`: Overwrite existing files if they exist.

### Examples

Convert a single web page to a PDF:

```bash
python render_multiple_sites_to_pdf.py https://www.example.com
```

Convert multiple web pages to PDFs, overwriting existing files:

```bash
python render_multiple_sites_to_pdf.py --force https://www.example.com https://www.example.org
```

## Project Structure

- `render_multiple_sites_to_pdf.py`: Main script to convert web pages to PDF.
- `setup_chromedriver.py`: Script to set up and configure ChromeDriver.
- `pdf_utils.py`: Utility functions for PDF generation.
- `add_url_to_page.py`: Function to add metadata (page title and URL) to the web page before conversion.
- `inactive_code/`: Directory containing inactive or deprecated code for organization.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
