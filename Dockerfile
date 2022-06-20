FROM python_core
ENV PYTHONUNBUFFERED=1
WORKDIR /django_backend
COPY requirements.txt /django_backend/
RUN pip install -r requirements.txt
COPY ./django_backend /django_backend/
COPY ./pdf_json /data/