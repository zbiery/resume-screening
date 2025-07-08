# import re
# from abc import ABC, abstractmethod
# from typing import IO, Optional, List, Dict, Any
# from io import IOBase
# from dataclasses import dataclass

# from .file_processor import FileProcessor
# from ..common.logger import get_logger
# from ..services.factory import AIServiceFactory

# logger = get_logger(__name__)

# @dataclass
# class ContactInfo:
#     name: str 
#     email: str | None
#     phone: str | None
#     websites: str | List[str] | None

# @dataclass
# class Resume:
#     contact_info: ContactInfo # name, email, phone, linkedin
#     synopsis: str | None      # summary/overview sections if it exists
#     experience: str | None    # work experience (internships, jobs), project work, etc.
#     skills: str | None        # relevant skills 

# class ResumeParser(ABC):
#     @abstractmethod
#     async def parse(self, source: str | IO) -> Resume:
#         pass

# class SimpleResumeParser(ResumeParser):
#     SECTION_HEADERS = {
#         "synopsis": ["summary", "objective", "about me", "profile"],
#         "experience": ["experience", "employment", "work history", "projects", "internships"],
#         "skills": ["skills", "technical skills", "toolkit", "competencies"]
#     }

#     def __init__(self):
#         self.processor = FileProcessor()

#     async def parse(self, source: str | IO) -> Resume:
#         logger.info("Starting SimpleResumeParser.parse")
#         if isinstance(source, str):
#             logger.info("Parsing from local file path: %s", source)
#             raw_text = await self.processor.extract_from_file(source)
#         elif isinstance(source, IOBase) or hasattr(source, "read"):
#             logger.info("Parsing from IO stream or uploaded file")
#             raw_text_chunks = await self.processor.process(source)
#             raw_text = "\n".join(chunk.strip() for chunk in raw_text_chunks)
#         else:
#             logger.error("Unsupported source type: %s", type(source))
#             raise ValueError("Unsupported source type. Must be file path or file-like object.")

#         return self._parse_text(raw_text)

#     def parse_sync(self, source: str | IO) -> Resume:
#         import asyncio
#         logger.info("Running parse_sync for source: %s", getattr(source, "name", source))
#         return asyncio.run(self.parse(source))

#     def _parse_text(self, text: str) -> Resume:
#         logger.debug("Parsing extracted text into structured resume fields")
#         lines = [line.strip() for line in text.splitlines() if line.strip()]
#         full_text = "\n".join(lines)

#         name = lines[0] if lines else ""
#         email = self._extract_email(full_text)
#         phone = self._extract_phone(full_text)
#         websites = self._extract_websites(full_text)

#         logger.debug("Extracted Contact Info: name=%s, email=%s, phone=%s, websites=%s", name, email, phone, websites)

#         contact_info = ContactInfo(name=name, email=email, phone=phone, websites=websites)
#         sections = self._extract_sections(full_text)

#         logger.info("Resume parsed successfully with sections: %s", list(sections.keys()))

#         return Resume(
#             contact_info=contact_info,
#             synopsis=sections.get("synopsis"),
#             experience=sections.get("experience"),
#             skills=sections.get("skills")
#         )

#     def _extract_email(self, text: str) -> Optional[str]:
#         match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", text)
#         email = match.group() if match else None
#         logger.debug("Extracted email: %s", email)
#         return email

#     def _extract_phone(self, text: str) -> Optional[str]:
#         match = re.search(r"(\+?1[\s\-\.]?)?(\(?\d{3}\)?[\s\-\.]?)?\d{3}[\s\-\.]?\d{4}", text)
#         phone = match.group() if match else None
#         logger.debug("Extracted phone: %s", phone)
#         return phone

#     def _extract_websites(self, text: str) -> Optional[List[str]]:
#         websites = re.findall(r"(https?://[^\s]+|www\.[^\s]+)", text) or None
#         logger.debug("Extracted websites: %s", websites)
#         return websites

#     def _extract_sections(self, text: str) -> Dict[str, Any]:
#         lowered_text = text.lower()
#         section_positions = {}

#         for section, keywords in self.SECTION_HEADERS.items():
#             for keyword in keywords:
#                 pattern = rf"\n.*{re.escape(keyword)}.*\n"
#                 match = re.search(pattern, lowered_text)
#                 if match:
#                     section_positions[section] = match.start()
#                     break

#         sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
#         extracted = {}

#         for i, (section, start) in enumerate(sorted_sections):
#             end = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(text)
#             extracted[section] = text[start:end].strip()

#         logger.debug("Extracted sections: %s", extracted.keys())
#         return extracted

# class AIResumeParser(ResumeParser):

#     def __init__(self):
#         self.processor = FileProcessor()
#         self.service = AIServiceFactory.create_service()

#     async def parse(self, source: str | IO) -> Resume:
#         logger.info("Starting AIResumeParser.parse")
#         if isinstance(source, str):
#             logger.info("Parsing from local file path: %s", source)
#             raw_text = await self.processor.extract_from_file(source)
#         elif isinstance(source, IOBase) or hasattr(source, "read"):
#             logger.info("Parsing from IO stream or uploaded file")
#             raw_text_chunks = await self.processor.process(source)
#             raw_text = "\n".join(chunk.strip() for chunk in raw_text_chunks)
#         else:
#             logger.error("Unsupported source type: %s", type(source))
#             raise ValueError("Unsupported source type. Must be file path or file-like object.")

#         return self._parse_text(raw_text)

#     def parse_sync(self, source: str | IO) -> Resume:
#         import asyncio
#         logger.info("Running parse_sync for AI parser")
#         return asyncio.run(self.parse(source))

#     def _parse_text(self, text: str) -> Resume:
#         logger.info("AI parser called but _parse_text is stubbed.")
#         logger.debug("Parsing extracted text into structured resume fields")
#         lines = [line.strip() for line in text.splitlines() if line.strip()]
#         full_text = "\n".join(lines)

#         name = self._extract_name(full_text)
#         email = self._extract_email(full_text)
#         phone = self._extract_phone(full_text)
#         websites = self._extract_websites(full_text)

#         logger.debug("Extracted Contact Info: name=%s, email=%s, phone=%s, websites=%s", name, email, phone, websites)

#         contact_info = ContactInfo(name=name, email=email, phone=phone, websites=websites) # type: ignore
#         sections = self._extract_sections(full_text)

#         logger.info("Resume parsed successfully with sections: %s", list(sections.keys()))

#         return Resume(
#             contact_info=contact_info,
#             synopsis=sections.get("synopsis"),
#             experience=sections.get("experience"),
#             skills=sections.get("skills")
#         )
    
#     def _extract_name(self, text: str) -> Optional[str]:
#         resp = self.service.query(f"""Extract the full name from the following resume. 
#                                   ONLY return the full name; do not include anything else
#                                   in your response. If a name is not present, 
#                                   return the word 'Null'.\n**Resume:**\n{text}""")
#         logger.debug("Extracted name: %s", resp.text)
#         return resp.text

#     def _extract_email(self, text: str) -> Optional[str]:
#         match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", text)
#         email = match.group() if match else None
#         logger.debug("Extracted email: %s", email)
#         return email

#     def _extract_phone(self, text: str) -> Optional[str]:
#         match = re.search(r"(\+?1[\s\-\.]?)?(\(?\d{3}\)?[\s\-\.]?)?\d{3}[\s\-\.]?\d{4}", text)
#         phone = match.group() if match else None
#         logger.debug("Extracted phone: %s", phone)
#         return phone

#     def _extract_websites(self, text: str) -> Optional[List[str]]:
#         logger.debug("AIParser._extract_websites is not implemented")
#         websites = re.findall(r"(https?://[^\s]+|www\.[^\s]+)", text) or None
#         logger.debug("Extracted websites: %s", websites)
#         return websites

#     def _extract_sections(self, text: str) -> Dict[str, Any]:
#         resp = self.service.query(f"""Extract the full name from the following resume. 
#                                   ONLY return the full name; do not include anything else
#                                   in your response. If a name is not present, 
#                                   return the word 'Null'.\n**Resume:**\n{text}""")
        
#         return {}
