run-api:
	uvicorn app.backend.api.main:app --reload

run-ui:
	streamlit run app/frontend/main.py

format:
	black .

test:
	pytest --cov=app tests/
