import os
from PyPDF2 import PdfReader
from docx import Document


def handle_upload_file(file_data, allowed_extensions=(".txt", ".pdf", ".docx")):
  if not file_data.filename:
    return "No file selected!"

  filename = file_data.filename
  file_ext = os.path.splitext(filename)[1].lower()
  if file_ext not in allowed_extensions:
    return f"Invalid file type. Allowed extensions: {', '.join(allowed_extensions)}"

  try:
    if file_ext == ".txt":
      file_content = file_data.read().decode("utf-8")
      return f"{file_content}"
    elif file_ext == ".pdf":
      try:
        pdf_reader = PdfReader(file_data)
        text = ""
        for page in pdf_reader.pages:
          text += page.extract_text()
        return f"{text}"
      except Exception as e:
        return f"Error processing PDF: {str(e)}"
    elif file_ext == ".docx":
      try:
        document = Document(file_data)
        text = ""
        for paragraph in document.paragraphs:
          text += paragraph.text
        return f"{text}"
      except Exception as e:
        return f"Error processing Word document: {str(e)}"
  except Exception as e:
    return f"Upload failed: {str(e)}"