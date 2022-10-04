FROM python:3.9

EXPOSE 8080

WORKDIR /src

RUN apt-get update && apt-get install -y unzip wget vim

# google-chromeインストール
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./prime_video_api /src/prime_video_api

CMD ["uvicorn", "prime_video_api.main:app", "--host", "0.0.0.0", "--port", "8080"]