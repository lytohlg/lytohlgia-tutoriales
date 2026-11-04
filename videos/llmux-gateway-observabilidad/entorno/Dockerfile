FROM golang:1.26-bookworm
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip curl sqlite3 procps make ca-certificates git \
 && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/rnapoles/llmux /opt/llmux-src \
 && cd /opt/llmux-src && make build && install -m 0755 bin/llmux /usr/local/bin/llmux \
 && rm -rf /opt/llmux-src
RUN pip3 install --no-cache-dir --break-system-packages "openai==1.54.4" "httpx==0.27.2"
WORKDIR /trabajo
CMD ["/bin/bash"]
