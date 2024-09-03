
FROM python:3.9

RUN mkdir -p /app
ENV APP_HOME=/app
WORKDIR $APP_HOME

COPY . $APP_HOME/
RUN pip3 install --no-cache-dir -r $APP_HOME/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
