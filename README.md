# html-to-markdown

A tool to convert HTML to Markdown, useful for web scraping or preparing text for Large Language Models (LLMs). Further improvements will be implemented.

## Usage

1.  Clone the repository.
2.  Install the dependencies using Poetry: `poetry install`
3.  Run the script: `python convert.py <input_file.html>`

The output will be saved to a file named `<input_file.md>`.

## Example

```bash
python convert.py my_page.html
```

This will convert `my_page.html` to `my_page.md`.

## Future Improvements

*   Add options to customize the output.
*   Improve handling of tables.
*   Add more robust error handling.