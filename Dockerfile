FROM fedora:latest

ARG VERSION
ARG ITERATION

COPY config.sample.yml /tmp/config.yml

RUN dnf install -y rpm-build rpm-sign rubygems ruby-devel gcc gcc-c++ make libffi-devel

RUN gem install ffi \
    && gem install fpm

# Build the RPM file
RUN fpm -s dir -t rpm -n voterwarehouse -v ${VERSION} --iteration ${ITERATION} \
    --description "VoterWarehouse: Imports and Extracts Voter and History data" \
    --url "https://github.com/jamjon3/VoterWarehouse" \
    --license "LGPL3.0" --vendor "James Jones" \
    --config-files /etc/VoterWarehouse/config.yml \
    -p /dist \
    /dist/voterwarehouse=/usr/bin/voterwarehouse \
    /tmp/config.yml=/etc/VoterWarehouse/config.yml

# Build the DEB file
RUN fpm -s dir -t deb -n voterwarehouse -v ${VERSION} --iteration ${ITERATION} \
    --description "VoterWarehouse: Imports and Extracts Voter and History data" \
    --url "https://github.com/jamjon3/VoterWarehouse" \
    --license "LGPL3.0" --vendor "James Jones" \
    --config-files /etc/VoterWarehouse/config.yml \
    -p /dist \
    /dist/voterwarehouse=/usr/bin/voterwarehouse \
    /tmp/config.yml=/etc/VoterWarehouse/config.yml
