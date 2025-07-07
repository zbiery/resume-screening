fn_candidate_analysis = [
    {
        "name": "AnalyzeCV",
        "description": "Parses a candidate's resume to extract relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_name": {
                    "type": "string",
                    "description": "Full name of the candidate.",
                    "minLength": 1,
                },
                "phone_number": {
                    "type": "string",
                    "description": "Candidate's phone number, including country code if available."
                    # "minLength": 7,
                    # "pattern": "^[+\\d\\s()-]+$",  # Allows digits, spaces, parentheses, plus, dash
                },
                "email": {
                    "type": "string",
                    "description": "Candidate's email address.",
                    "format": "email"
                },
                "websites": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        # consider removing format if URLs may omit protocol,
                        # or replace with pattern enforcing http(s):// prefix if you want strict URLs
                        # "format": "uri",
                    },
                    "description": "Candidate's personal or professional URLs (LinkedIn, GitHub, portfolio, etc.).",
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "education": {
                    "type": "array",
                    "description": "List of educational qualifications with details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "string",
                                "description": "Degree level, e.g., Associates, Baccalaureate, Masters, PhD.",
                                "minLength": 1,
                                "enum": [
                                    "Associates",
                                    "Baccalaureate",
                                    "Bachelor's",
                                    "Masters",
                                    "Master's",
                                    "PhD",
                                    "Doctorate",
                                    "Diploma",
                                    "Certificate"
                                ]
                            },
                            "field": {
                                "type": "string",
                                "description": "Field of study, e.g., Computer Science, Statistics, Communications.",
                                "minLength": 1,
                            },
                            "institution": {
                                "type": "string",
                                "description": "Name of the educational institution.",
                                "minLength": 1,
                            },
                            "year": {
                                "type": ["string", "null"],
                                "description": "Year of graduation or expected graduation (e.g., 2024). Optional.",
                                # "pattern": "^\\d{4}$",
                                "nullable": True
                            },
                            "gpa": {
                                "type": ["string", "null"],
                                "description": "GPA mentioned for this education entry, if any (e.g., 3.8/4.0). Optional.",
                                "minLength": 1,
                                "nullable": True
                            }
                        },
                        "required": ["level", "field", "institution"],
                        "additionalProperties": False,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "roles": {
                    "type": "array",
                    "description": "List of relevant roles held by the candidate, each with a job title and a brief summary of work completed.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Job title or role name, e.g., 'Software Engineer Intern'.",
                                "minLength": 1,
                            },
                            "company": {
                                "type": "string",
                                "description": "Name of the company, e.g., 'Apple', 'Micrsoft'.",
                                "minLength": 1,
                            },
                            "summary": {
                                "type": "string",
                                "description": "Brief summary of work completed in this role. Do not copy-paste existing information.",
                                "minLength": 10,
                                "maxLength": 500,
                            }
                        },
                        "required": ["title", "company", "summary"],
                        "additionalProperties": False,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "years_of_experience": {
                    "type": "number",
                    "description": "Total estimated years of relevant experience (work, internships, projects), e.g. '1.5', '4'",
                    "minimum": 0,
                },
                "technical_skill": {
                    "type": "array",
                    "description": "List of technical skills and proficiencies.",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "responsibilities": {
                    "type": "array",
                    "description": "List of key responsibilities from previous roles or projects.",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "certificate": {
                    "type": "array",
                    "description": "List of certificates or certifications achieved.",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "soft_skill": {
                    "type": "array",
                    "description": "List of inferred soft skills (communication, leadership, etc.).",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "comment": {
                    "type": "string",
                    "description": "Descriptive but brief summary about the candidate's strengths and standout qualities.",
                    "minLength": 100,
                    "maxLength": 1200,
                },
                "job_recommended": {
                    "type": "array",
                    "description": "List of recommended job titles the candidate should consider.",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                }
            },
            "required": [
                "candidate_name",
                "phone_number",
                "email",
                "websites",
                "education",
                "roles",
                "years_of_experience",
                "technical_skill",
                "responsibilities",
                "certificate",
                "soft_skill",
                "comment",
                "job_recommended"
            ],
            "additionalProperties": False,
        },
    }
]

fn_job_analysis = [
    {
        "name": "AnalyzeJob",
        "description": "Read the job description and answer question.",
        "parameters": {
            "type": "object",
            "properties": {
                "degree": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "educational qualifications required, e.g., Bachelor's degree in Computer Science.",
                },
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Experiences required at position.",
                },
                "technical_skill": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "specific technical skills and proficiencies. e.g. Java,  Python, Linux, SQL.",
                },
                "responsibility": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Responsibilities for position candidate required. e.g. Evaluate and prioritize the many services and products that can benefit from AI, Work on the product and architectural implications, that is build, deploy, and test models",
                },
                "certificate": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Required certificates for the position, e.g., CompTIA Security+.",
                },
                "soft_skill": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Soft skills required for the job, inferred from the provided information. e.g. Language, communication, teamwork, adaptability.",
                },
            },
            "required": [
                "degree",
                "experience",
                "technical_skill",
                "responsibility",
                "certificate",
                "soft_skill",
            ],
        },
    }
]

fn_matching_analysis = [
    {
        "name": "evaluate",
        "description": "For each requirement, score in 0 - 100 scale if the candidate match with the requirement or not.",
        "parameters": {
            "type": "object",
            "properties": {
                "degree": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "experience": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not. e.g. 75 ",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "technical_skill": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not. e.g. 75",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement.",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "responsibility": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not. e.g. 75",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement.",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "certificate": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not.",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement.",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "soft_skill": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Score if the candidate match with the requirement or not. e.g. 75",
                        },
                        "comment": {
                            "type": "string",
                            "description": "What match the requirement, what does not match the requirement, special soft skill in the CV.",
                        },
                    },
                    "required": ["score", "comment"],
                },
                "summary_comment": {
                    "type": "string",
                    "description": "Give comment about matching candidate based on requirement",
                },
            },
            "required": [
                "degree",
                "experience",
                "technical_skill",
                "responsibility",
                "certificate",
                "soft_skill",
                "summary_comment",
            ],
        },
    }
]