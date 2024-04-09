FROM python:3.12-slim
LABEL authors="septiadi"

RUN mkdir /opa-py
WORKDIR /opa-py
ADD . /opa-py/
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "/opa-py/app.py"]
