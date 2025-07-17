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
                                "minLength": 0,
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
                                "minLength": 0,
                            },
                            "company": {
                                "type": "string",
                                "description": "Name of the company, e.g., 'Apple', 'Micrsoft'.",
                                "minLength": 0,
                            },
                            "summary": {
                                "type": "string",
                                "description": "Brief summary of work completed in this role. Do not copy-paste existing information.",
                                "minLength": 0,
                                "maxLength": 1000,
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
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "responsibilities": {
                    "type": "array",
                    "description": "List of key responsibilities from previous roles or projects.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "certificate": {
                    "type": "array",
                    "description": "List of certificates or certifications achieved.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "soft_skill": {
                    "type": "array",
                    "description": "List of inferred soft skills (communication, leadership, etc.).",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "comment": {
                    "type": "string",
                    "description": "Descriptive but brief summary about the candidate's strengths and standout qualities.",
                    "minLength": 0,
                    "maxLength": 3000,
                },
                "job_recommended": {
                    "type": "array",
                    "description": "List of recommended job titles the candidate should consider.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
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
        "description": "Parses a job description to extract structured qualifications, responsibilities, and skill requirements.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "Official job title or role name, e.g., 'Machine Learning Engineer', 'Product Manager'.",
                    "minLength": 0,
                },
                "job_level": {
                    "type": "string",
                    "description": "Seniority level or rank of the position. Example: 'Internship', 'Entry-level', 'Mid', 'Senior', 'Lead', 'Director'.",
                    "minLength": 0,
                },
                "employment_type": {
                    "type": "string",
                    "description": "Type of employment. Example: 'Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'.",
                    "minLength": 0,
                },
                "location_requirement": {
                    "type": "string",
                    "description": "Location requirements or constraints for the role. Example: 'Remote', 'Hybrid in NYC', 'Onsite in Austin, TX'.",
                    "minLength": 0,
                },
                "years_of_experience": {
                    "type": "number",
                    "description": "Minimum or average years of relevant experience required, as stated or inferred from the job description. Example: 2, 5.5",
                    "minimum": 0,
                },
                "educational_requirements": {
                    "type": "array",
                    "description": "List of required or preferred educational qualifications, including degree level and a list of acceptable fields of study.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "string",
                                "description": "Required degree level, e.g., Bachelor's, Master's, PhD.",
                                "minLength": 0,
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
                            "fields": {
                                "type": "array",
                                "description": "Array of acceptable fields of study. Example: ['Computer Science', 'Electrical Engineering', 'Statistics'].",
                                "items": {
                                    "type": "string",
                                    "minLength": 0,
                                },
                                "minItems": 0,
                                "uniqueItems": True
                            }
                        },
                        "required": ["level", "fields"],
                        "additionalProperties": False,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "experience": {
                    "type": "array",
                    "description": "Relevant experience required. Include domain or task-specific expectations (e.g., '3+ years in cloud systems design').",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "technical_skill": {
                    "type": "array",
                    "description": "List of technical skills, tools, or technologies mentioned in the job description.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "responsibilities": {
                    "type": "array",
                    "description": "List of key job responsibilities outlined in the description.",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "minItems": 0,
                    "uniqueItems": False,
                },
                "certificate": {
                    "type": "array",
                    "description": "List of certifications required or preferred. Example: 'AWS Certified Developer', 'PMP'.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "soft_skill": {
                    "type": "array",
                    "description": "Soft skills or personality traits expected. Example: 'collaboration', 'initiative', 'time management'.",
                    "items": {
                        "type": "string",
                        "minLength": 0,
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "domain": {
                    "type": "string",
                    "description": "Industry or application domain. Example: 'Finance', 'Healthcare', 'Defense'.",
                    "minLength": 0,
                },
                "ideal_candidate_summary": {
                    "type": "string",
                    "description": "Brief profile of the ideal candidate as implied by the job description. Highlight standout qualities, background, or behaviors.",
                    "minLength": 0,
                    "maxLength": 1200,
                }
            },
            "required": [
                "job_title",
                "job_level",
                "employment_type",
                "location_requirement",
                "years_of_experience",
                "educational_requirements",
                "experience",
                "technical_skill",
                "responsibilities",
                "certificate",
                "soft_skill",
                "domain",
                "ideal_candidate_summary"
            ],
            "additionalProperties": False,
        }
    }
]

fn_match = [
    {
        "name": "MatchJobToCandidate",
        "description": "Evaluates how well a candidate matches a job description using structured scoring across categories, with comments explaining each score.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_name": {
                    "type": "string",
                    "description": "Name of the candidate being evaluated.",
                    "minLength": 1
                },
                "job_title": {
                    "type": "string",
                    "description": "Title of the job position being matched against.",
                    "minLength": 1
                },
                "education": {
                    "type": "object",
                    "description": "Education matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) reflecting how well the candidate's education aligns with the job requirements.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the education score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "experience": {
                    "type": "object",
                    "description": "Experience matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) reflecting alignment in required years and relevance of prior roles.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the experience score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "technical_skill": {
                    "type": "object",
                    "description": "Technical skill matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) for technical skill overlap between job and candidate.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the technical skill score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "responsibility": {
                    "type": "object",
                    "description": "Responsibility matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) for how well past responsibilities match current job expectations.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the responsibility score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "certificate": {
                    "type": "object",
                    "description": "Certificate matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) for how well the candidate meets certification requirements.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the certificate score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "soft_skill": {
                    "type": "object",
                    "description": "Soft skill matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) based on inferred or stated soft skills vs. job needs.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the soft skill score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "domain": {
                    "type": "object",
                    "description": "Domain relevance matching details.",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "description": "Score (0-100) for industry/domain relevance between past experience and job context.",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "comment": {
                            "type": "string",
                            "description": "Explanation of the domain score.",
                            "minLength": 1
                        }
                    },
                    "required": ["score", "comment"],
                    "additionalProperties": False
                },
                "strengths": {
                    "type": "array",
                    "description": "List of key strengths and alignment reasons.",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    }
                },
                "gaps": {
                    "type": "array",
                    "description": "List of mismatches or weaknesses relative to the job.",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    }
                },
                "verdict": {
                    "type": "string",
                    "description": "Overall textual evaluation of the match quality.",
                    "enum": [
                        "Strong match",
                        "Moderate match",
                        "Weak match",
                        "Not a match"
                    ]
                },
                "overall_summary": {
                    "type": "string",
                    "description": "A detailed 100-300 word summary explaining why the candidate is or is not a fit for the job.",
                    "minLength": 0,
                    "maxLength": 1800
                }
            },
            "required": [
                "candidate_name",
                "job_title",
                "education",
                "experience",
                "technical_skill",
                "responsibility",
                "certificate",
                "soft_skill",
                "domain",
                "strengths",
                "gaps",
                "verdict",
                "overall_summary"
            ],
            "additionalProperties": False
        }
    }
]