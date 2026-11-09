FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ant openjdk-21-jdk-headless libtool autoconf automake \
    libsqlite3-dev libssl-dev libewf-dev zlib1g-dev libafflib-dev \
    libvhdi-dev libvmdk-dev libvslvm-dev libpq-dev \
    curl ca-certificates python3 unzip dpkg-dev patchelf e2fsprogs \
    libgtk-3-0 libasound2t64 libxtst6 libxi6 libxrender1 fonts-dejavu-core testdisk \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
CMD ["bash", "scripts/build.sh"]
