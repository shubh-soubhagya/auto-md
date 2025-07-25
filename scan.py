import os
import csv
import json

def scan_files(root_dir, extensions=(".py", ".ipynb", ".env")):
    file_data = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(subdir, file)

                try:
                    if file.endswith('.ipynb'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content_json = json.load(f)
                            file_content = json.dumps(content_json)  # Store as string
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()

                    file_data.append((file_path, file_content))

                except Exception as e:
                    print(f"Skipped {file_path}: {e}")

    return file_data

def save_to_csv(data, output_csv="scanned_files.csv"):
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["file_path", "file_content"])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    root_directory = r"C:\Users\hp\Desktop\Accen\DALLE-image-generation-bot"  # You can replace this with your target directory
    scanned_data = scan_files(root_directory)
    save_to_csv(scanned_data)
    print(f"Saved {len(scanned_data)} files to 'scanned_files.csv'")
