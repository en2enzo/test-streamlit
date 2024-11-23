#FROM python:3.9-slim
FROM python
WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit
COPY . .
EXPOSE 8000
#CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["streamlit", "run", "test-streamlit.py", "--server.port=8000"]
