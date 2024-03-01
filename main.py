import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer and model outside of the main function
tokenizer1 = AutoTokenizer.from_pretrained("toanduc/vit5-base-vietnews-summarization-finetuned")
model1 = AutoModelForSeq2SeqLM.from_pretrained("toanduc/vit5-base-vietnews-summarization-finetuned")

# Use st.cache to cache the results of perform_summarization function
@st.cache_data
def perform_summarization(sentence):
    inputs = tokenizer1.encode("summarize: " + sentence, return_tensors="pt", max_length=512, truncation=True)
    summary_ids1 = model1.generate(inputs, max_length=200, length_penalty=2.0, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)
    summary_text_t5 = tokenizer1.decode(summary_ids1[0], skip_special_tokens=True)
    
    summarized_text = summary_text_t5

    return summarized_text

def main():
    st.title("Tóm Tắt Văn Bản Webapp")
    
    # Chọn phương thức nhập liệu từ người dùng
    input_method = st.radio("Chọn Phương Thức Nhập Liệu:", ("Tải Lên File", "Nhập Tay"))

    if input_method == "Tải Lên File":
        # Widget để tải lên file
        uploaded_file = st.file_uploader("Chọn một file", type=["txt", "csv", "pdf"])

        if uploaded_file is not None:
            content = uploaded_file.read()
            st.write(content)

        if uploaded_file is not None:
            # Đọc nội dung từ file
            text_input = io.TextIOWrapper(uploaded_file).read()
        else:
            st.warning("Vui lòng chọn một file để tải lên.")
            return
    else:
        # Widget để nhập văn bản
        text_input = st.text_area("Nhập văn bản cần tóm tắt:", "")

    if st.button("Tóm Tắt"):
        # Gọi hàm tóm tắt văn bản ở đây (thay bằng code thực hiện tóm tắt)
        summarized_text = perform_summarization(text_input)

        # Hiển thị kết quả tóm tắt
        st.subheader("Kết Quả Tóm Tắt:")
        st.write(summarized_text)

if __name__ == "__main__":
    main()
