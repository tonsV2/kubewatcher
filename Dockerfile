FROM python:3.8-alpine as builder
RUN apk --no-cache add gcc musl-dev libffi-dev openssl-dev rust cargo
WORKDIR /src
ADD . .
RUN pip --no-cache-dir install . --target /app

FROM python:3.8-alpine
ENV PYTHONPATH /app
ENV PATH /app/bin/:$PATH
WORKDIR /app
COPY --from=builder /app .
USER guest
ENTRYPOINT ["kubewatcher"]
CMD ["watch"]
