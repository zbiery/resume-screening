# resume-screening

https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat

## project structure
```bash
└── resume-screening
    └── app
        └── backend
            └── api
                └── endpoint.py
                └── main.py
                └── middleware.py
                └── router.py
            └── common
                └── config.py
                └── logger.py
                └── utils.py
            └── core
        └── frontend
            └── main.py
    └── config
        └── config.yml
        └── dev.env
        └── prod.env
        └── template.env
        └── test.env
    └── infra
        └── core.bicep
        └── dev.json
    └── logs
    └── tests
    └── .gitignore
    └── Dockerfile
    └── LICENSE
    └── README.md
```