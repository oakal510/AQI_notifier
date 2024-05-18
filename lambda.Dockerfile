FROM python:3.12 AS builder

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
RUN mkdir -p /src
WORKDIR /src
COPY . .
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv

FROM python:3.12
COPY --from=builder /venv /venv
COPY --from=builder /src /src
WORKDIR /src

# Set runtime interface client as default command for the container runtime
ENTRYPOINT ["/venv/bin/python", "-m", "awslambdaric" ]

# Pass the name of the function handler as an argument to the runtime
CMD [ "lambda_function.handler" ]

