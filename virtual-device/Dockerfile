# Creates a container which acts as a bare bones non-VM based Mender Client
# installation, for use in tests and as Virtual Device for evaluation

# Build mender repository, which is heaviest part
FROM ubuntu:24.04 AS build-mender

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y make git build-essential jq cmake \
    libssl-dev liblmdb++-dev libboost-dev libboost-log-dev \
    libarchive-dev libdbus-1-dev

ARG MENDER_CLIENT_REV=master
RUN git clone https://github.com/mendersoftware/mender /src/mender
WORKDIR /src/mender
RUN git fetch origin $MENDER_CLIENT_REV && git checkout FETCH_HEAD || git checkout -f $MENDER_CLIENT_REV
RUN git submodule update --init

WORKDIR /src/mender
RUN mkdir --parents /mender-install/etc/mender
RUN cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -S .
RUN DESTDIR=/mender-install make --jobs=$(nproc --all) install
RUN jq ".ServerCertificate=\"/usr/share/doc/mender-auth/examples/demo.crt\" | .ServerURL=\"https://docker.mender.io/\"" \
    < examples/mender.conf.demo > /mender-install/etc/mender/mender.conf
RUN mkdir --parents /mender-install/var/lib/mender && echo device_type=generic-x86_64 > /mender-install/var/lib/mender/device_type

# Build mender-connect and mender-configure, and generate the bootstrap Artifact
FROM ubuntu:24.04 AS build-other

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y make git golang liblzma-dev libglib2.0-dev curl jq

ARG MENDER_CONNECT_REV=master
ARG MENDER_CONFIGURE_REV=master

# mender-connect ---------------------------------------------------------------

RUN git clone https://github.com/mendersoftware/mender-connect /src/mender-connect
WORKDIR /src/mender-connect
RUN git fetch origin $MENDER_CONNECT_REV && git checkout FETCH_HEAD || git checkout -f $MENDER_CONNECT_REV

RUN mkdir --parents /mender-install/etc/mender
RUN make prefix=/mender-install install
RUN jq ".User=\"root\"" \
    < examples/mender-connect.conf > /mender-install/etc/mender/mender-connect.conf

# mender-configure -------------------------------------------------------------

RUN git clone https://github.com/mendersoftware/mender-configure-module /src/mender-configure-module
WORKDIR /src/mender-configure-module
RUN git fetch origin $MENDER_CONFIGURE_REV && git checkout FETCH_HEAD || git checkout -f $MENDER_CONFIGURE_REV

RUN make DESTDIR=/mender-install install

# bootstrap Artifact -----------------------------------------------------------

RUN curl --fail --silent --show-error --location \
        https://downloads.mender.io/repos/debian/gpg > /etc/apt/trusted.gpg.d/mender.asc && \
    echo "deb [arch=$(dpkg --print-architecture)] https://downloads.mender.io/repos/workstation-tools ubuntu/$(. /etc/lsb-release && echo $DISTRIB_CODENAME)/stable main" > \
        /etc/apt/sources.list.d/mender.list && \
    apt-get update && apt-get install -y mender-artifact
RUN mender-artifact write bootstrap-artifact \
        --artifact-name original \
        --device-type generic-x86_64 \
        --provides "rootfs-image.version:original" \
        --output-path /bootstrap.mender

# Final image to run the Virtual Device from
FROM ubuntu:24.04

RUN mkdir --parents /run/dbus && apt-get update && apt-get install -y \
    liblzma5 dbus openssh-server sudo liblmdb0 libarchive13 libboost-log1.83.0 iproute2 jq

# Set no password
RUN sed -ie 's/^root:[^:]*:/root::/' /etc/shadow
RUN sed -ie 's/^UsePAM/#UsePam/' /etc/ssh/sshd_config
RUN echo 'PermitEmptyPasswords yes\n\
PermitRootLogin yes\n\
Port 22\n\
Port 8822\n' >> /etc/ssh/sshd_config

# Install Mender Client
COPY --from=build-mender /mender-install/usr/ /usr/
COPY --from=build-mender /mender-install/etc/ /etc/
COPY --from=build-mender /mender-install/lib/ /lib/
COPY --from=build-mender /mender-install/var/ /var/
COPY --from=build-other /mender-install/usr/ /usr/
COPY --from=build-other /mender-install/etc/ /etc/
COPY --from=build-other /mender-install/lib/ /lib/
COPY --from=build-other /bootstrap.mender /var/lib/mender/bootstrap.mender

# Install the demo server certificate(s). See:
# https://github.com/mendersoftware/meta-mender/blob/master/meta-mender-core/recipes-mender/mender-server-certificate/mender-server-certificate.bb
COPY --from=build-mender /src/mender/support/demo.crt /server.crt
RUN \
    mkdir /usr/local/share/ca-certificates/mender                              ;\
    certnum=1                                                                  ;\
    while read LINE; do                                                         \
        if [ -z "$cert" ] || echo "$LINE" | fgrep -q 'BEGIN CERTIFICATE'; then  \
            cert=/usr/local/share/ca-certificates/mender/server-$certnum.crt   ;\
            rm -f $cert                                                        ;\
            touch $cert                                                        ;\
            chmod 0444 $cert                                                   ;\
            certnum=$(expr $certnum + 1)                                       ;\
        fi                                                                     ;\
        echo "$LINE" >> $cert                                                  ;\
    done < /server.crt                                                         ;\
    rm /server.crt
RUN update-ca-certificates

COPY entrypoint.sh /
CMD [ "/entrypoint.sh" ]
