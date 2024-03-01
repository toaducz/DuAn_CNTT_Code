import os
import openai
import csv
import time
import shutil  # Thêm thư viện shutil

api_key = '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'
folder_path = r"D:\New folder (2)\VNNewsCrawler-main\temp\dantri-the-thao"
output_csv_path = r"output.csv"
output_folder_path = r"D:\New folder (2)\VNNewsCrawler-main\temp\testing"  # Đường dẫn thư mục mới

# Kiểm tra và tạo thư mục mới nếu chưa tồn tại
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

summaries = []
max_summaries = 3  # Số lượng tóm tắt tối đa
max_articles = 100  # Số lượng bài báo tối đa
articles_processed = 0
count = 0
max_tokens_threshold = 4096

# Ghi vào file CSV
with open(output_csv_path, mode='a', newline='', encoding='utf-8-sig') as csv_file:
    fieldnames = ['Original Text', 'Summary']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Nếu file CSV trống, viết tiêu đề cột vào file
    if os.path.getsize(output_csv_path) == 0:
        writer.writeheader()

    for file_name in file_list:
        if articles_processed >= max_articles:
            print(f"Stopping summarization process. {max_articles} articles have been processed.")
            break

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        if len(text_content.split()) < 50:
            print(f"Skipping {file_name} as it is too short.")
            continue
        
        if len(text_content.split()) > max_tokens_threshold:
            print(f"Skipping {file_name} as it exceeds the maximum token threshold.")
            continue
        
        # Di chuyển văn bản gốc sang thư mục mới
        new_file_path = os.path.join(output_folder_path, file_name)
        shutil.move(file_path, new_file_path)
        
        prompt = f"hãy tóm tắt bản tin tức thể thao sau (bằng đoạn văn) chú ý đến những thông tin như cầu thủ/CLB liên quan, giá chuyển nhượng, chi tiết hợp đồng, lý do chuyển nhượng\n{text_content}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            api_key=api_key
        )

        summary = response['choices'][0]['text']
        summaries.append(summary)

        print(f"Summary for {file_name} has been added to the list. Total summaries: {len(summaries)}")

        # Ghi mỗi hàng với một văn bản gốc và một văn bản tóm tắt
        writer.writerow({'Original Text': text_content, 'Summary': summary})

        articles_processed += 1
        count += 1 

        if count == max_summaries:
            print(f"Doi 1 phut cho hoi chieu.")
            count = 0
            time.sleep(60)  # Đợi 1 phút trước khi tiếp tục

print(f"All summaries have been written to {output_csv_path}")
print(f"All original texts have been moved to {output_folder_path}")

