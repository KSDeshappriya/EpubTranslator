import re
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ebooklib import epub
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import time

def browse_input_epub():
    input_epub_path = filedialog.askopenfilename(filetypes=[("EPUB Files", "*.epub")])
    input_epub_entry.delete(0, tk.END)
    input_epub_entry.insert(0, input_epub_path)

def browse_output_epub():
    output_epub_path = filedialog.asksaveasfilename(defaultextension=".epub", filetypes=[("EPUB Files", "*.epub")])
    output_epub_entry.delete(0, tk.END)
    output_epub_entry.insert(0, output_epub_path)

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
        total_items = len(list(book.items))
        completed_items = 0

        def update_progress():
            completed_items_var.set(f"Completed: {completed_items}/{total_items}")

        start_time = time.time()
        for item in book.items:
            if isinstance(item, epub.EpubHtml):
                content = item.content.decode('utf-8')
                translated_content = executor.submit(translate_text, content).result()
                item.content = translated_content.encode('utf-8')
                completed_items += 1
                progress_bar['value'] = (completed_items / total_items) * 100
                update_progress()
                app.update_idletasks()

        end_time = time.time()

    # Save the translated EPUB to the output file
    epub.write_epub(output_epub_path, book)

    # Calculate and display the execution time
    execution_time = end_time - start_time
    execution_time_label.config(text=f"Translation completed in {execution_time:.2f} seconds.")

def extract_text_between_tags(input_string):
    tag_pattern = r'<[^>]+>'
    text_fragments = re.split(tag_pattern, input_string)
    text_fragments = [fragment.strip() for fragment in text_fragments if fragment.strip()]
    return text_fragments

# Create the main application window
app = tk.Tk()
app.title("EPUB Translator")

# Create and configure widgets
input_label = tk.Label(app, text="Select Input EPUB:")
input_label.pack()

input_epub_entry = tk.Entry(app, width=50)
input_epub_entry.pack()

browse_input_button = tk.Button(app, text="Browse", command=browse_input_epub)
browse_input_button.pack()

output_label = tk.Label(app, text="Save Output EPUB As:")
output_label.pack()

output_epub_entry = tk.Entry(app, width=50)
output_epub_entry.pack()

browse_output_button = tk.Button(app, text="Browse", command=browse_output_epub)
browse_output_button.pack()

target_language_label = tk.Label(app, text="Target Language Code:")
target_language_label.pack()

target_language_entry = tk.Entry(app, width=10)
target_language_entry.pack()

translate_button = tk.Button(app, text="Translate EPUB")
translate_button.pack()

progress_frame = ttk.Frame(app)
progress_frame.pack()

completed_items_var = tk.StringVar()
completed_items_label = tk.Label(progress_frame, textvariable=completed_items_var)
completed_items_label.pack()

progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode='determinate')
progress_bar.pack()

execution_time_label = tk.Label(app, text="")
execution_time_label.pack()

# Function to start translation when the "Translate EPUB" button is clicked
def translate_button_clicked():
    input_epub_path = input_epub_entry.get()
    output_epub_path = output_epub_entry.get()
    target_language = target_language_entry.get()
    translate_button.config(state='disabled')  # Disable the button during translation
    translate_epub(input_epub_path, output_epub_path, target_language)
    translate_button.config(state='normal')  # Re-enable the button after translation

translate_button.config(command=translate_button_clicked)

# Start the main application loop
app.mainloop()
