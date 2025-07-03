from app.backend.core.file_processor import FileProcessor
from app.backend.core.resume_parser import SimpleResumeParser

content = FileProcessor().extract_from_file_sync("data/ZacharyBiery_CV_2024.docx")
print(content)

# parser = SimpleResumeParser()
# resume = parser.parse_sync("data/ZacharyBiery_CV_2024.docx")

# print(resume.skills)
