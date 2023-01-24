FROM 595352645034.dkr.ecr.us-east-1.amazonaws.com/gaivota-python-crawler-driver:v3.7.0 as stage_install

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt --user --no-cache-dir
ENV PATH="/root/.local/bin:$PATH"

FROM 595352645034.dkr.ecr.us-east-1.amazonaws.com/gaivota-python-crawler-driver:v3.7.0 as stage_dev

WORKDIR /app
COPY --from=stage_install /root/.local /root/.local
COPY dev-requirements.txt /app/dev-requirements.txt

RUN pip install -r dev-requirements.txt --user --no-cache-dir
ENV PATH="/root/.local/bin:$PATH"
COPY . /app

RUN pytest --cov-fail-under=0 --cov gaivota_python_nilo_crawler

FROM 595352645034.dkr.ecr.us-east-1.amazonaws.com/gaivota-python-crawler-driver:v3.7.0 as stage_env

WORKDIR /app
COPY --from=stage_install /root/.local /root/.local

ENV PATH="/root/.local/bin:$PATH"

COPY . /app

ENTRYPOINT [ "scrapy", "crawl" ]
