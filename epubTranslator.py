import re
from ebooklib import epub
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Progress bar
import time

def translate_epub(input_epub_path, output_epub_path, target_language='en', batch_size=10):
    # Open the input EPUB file
    book = epub.read_epub(input_epub_path)

    # Initialize the Google Translate API
    translator = GoogleTranslator(source='auto', target=target_language)

    def translate_text(content):
        text_fragments = extract_text_between_tags(content)
        translated_fragments = []

        for fragment in text_fragments:
            # Check if the fragment resembles a URL (http/https)
            if re.match(r'^https?://', fragment):
                translated_fragments.append(fragment)  # Keep URLs as they are
            else:
                translated_fragments.append(translator.translate(fragment))

        translated_content = content
        for i in range(len(text_fragments)):
            translated_content = translated_content.replace(text_fragments[i], translated_fragments[i], 1)
        return translated_content

    # Create a ThreadPoolExecutor for concurrent translation
    with ThreadPoolExecutor() as executor:
        start_time = time.time()
        for item in tqdm(book.items, desc="Translating EPUB"):
            if isinstance(item, epub.EpubHtml):
                content = item.content.decode('utf-8')
                translated_content = executor.submit(translate_text, content).result()
                item.content = translated_content.encode('utf-8')

        end_time = time.time()

    # Save the translated EPUB to the output file
    epub.write_epub(output_epub_path, book)

    # Calculate and display the execution time
    execution_time = end_time - start_time
    print(f"Translation completed in {execution_time:.2f} seconds.")

def extract_text_between_tags(input_string):
    tag_pattern = r'<[^>]+>'
    text_fragments = re.split(tag_pattern, input_string)
    text_fragments = [fragment.strip() for fragment in text_fragments if fragment.strip()]
    return text_fragments

if __name__ == "__main__":
    input_epub_path = 'input.epub'  # Replace with your input EPUB file path
    output_epub_path = 'output.epub'  # Replace with your desired output file path
    target_language = 'si'  # Change this to your desired target language code
    translate_epub(input_epub_path, output_epub_path, target_language)
