FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /ultraxpert
COPY requirements.txt /ultraxpert/
RUN python3 -m pip install -r requirements.txt
COPY . /ultraxpert/


