FROM xxx

# Set the proxy environment variables
ENV http_proxy="xxx"
ENV https_proxy="xxx"
ENV HTTP_PROXY="xxx"
ENV HTTPS_PROXY="xxx"

WORKDIR /app

COPY . .

RUN pip install flask
RUN pip install requests

CMD ["python", "app.py"]
