FROM python:3.8.10-alpine as base

RUN apk update && apk add gcc g++
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

FROM base as stock

COPY --from=base /app .
COPY stock_service stock_service
EXPOSE 5001

WORKDIR stock_service
ENTRYPOINT [ "python3" ]
CMD [ "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]
