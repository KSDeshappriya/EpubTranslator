# EPUB Translator

This Python script, `epubTranslator.py`, allows you to translate the text content of an EPUB file from one language to another using Google Translate API. The translated content is then saved to a new EPUB file. This README provides instructions on how to use the script and details its functionality.

## Prerequisites

Before using the script, make sure you have the following prerequisites installed on your system:

- Python 3.x
- Required Python packages:
  - `ebooklib`: Used for reading and writing EPUB files.
  - `deep_translator`: Used for text translation using Google Translate API.
  - `concurrent.futures`: Used for concurrent execution of translation tasks.
  - `tqdm`: Used for displaying a progress bar during translation.

You can install the required packages using pip:

```bash
pip install ebooklib deep-translator tqdm
```

## Usage

1. Place your EPUB file that you want to translate in the same directory as the script or provide the full path to the EPUB file.

2. Open a terminal or command prompt and navigate to the directory containing the script.

3. Run the script with the following command, replacing `input.epub` with the name of your input EPUB file and `output.epub` with your desired output file name:

   ```bash
   python epubTranslator.py input.epub output.epub
   ```

   You can also specify the target language using the `-t` or `--target` flag. For example, to translate to Sinhala (si), you can run:

   ```bash
   python epubTranslator.py input.epub output.epub -t si
   ```

   The script will translate the content and create a new EPUB file with the translated text.

4. The translation progress will be displayed using a progress bar. The script will inform you when the translation is completed.

## Advanced Usage

- If you have a large EPUB file or want to control the number of parallel translation tasks, you can adjust the `batch_size` parameter in the script. For example:

   ```bash
   python epubTranslator.py input.epub output.epub -t si --batch-size 5
   ```

   This will limit the number of concurrent translation tasks to 5 at a time.

## Notes

- URLs within the EPUB file will not be translated, so they will remain in their original form.
- The script uses the Google Translate API for translation, and you may need an internet connection for it to work.

## License

This script is provided under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

Feel free to customize and use this script to translate EPUB files to your desired language for non-commercial purposes. If you encounter any issues or have suggestions for improvements, please report them on the GitHub repository.

Enjoy translating your EPUB files!