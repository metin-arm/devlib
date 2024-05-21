# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2024, ARM Limited and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This Dockerfile creates an image to run devlib CI tests.
#
# Running ``docker build -t devlib .`` command in ``tools/docker`` directory
# creates the docker image.
#
# The image can be runned via ``docker run -it --privileged devlib`` command.
#

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

ENV DEVLIB_REF reduce-docker-img

ENV BUILDROOT_VERSION "2023.11.1"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    aapt \
    bc \
    bison \
    build-essential \
    cmake \
    cpio \
    file \
    flex \
    git \
    libelf-dev \
    libncurses5-dev \
    libssl-dev \
    locales \
    python3-pip \
    qemu-system-arm \
    qemu-system-x86 \
    rsync \
    sudo \
    unzip \
    wget \
    vim \
    xz-utils

RUN apt-get -y autoremove && \
    apt-get -y autoclean && \
    apt-get clean && \
    rm -rf /var/cache/apt

RUN git clone --depth=1 -b ${DEVLIB_REF} -v https://github.com/metin-arm/devlib.git /devlib
RUN cd /devlib && \
    pip install --upgrade pip setuptools wheel && \
    pip install .[full]

# Set ANDROID_CMDLINE_VERSION environment variable if you want to use a
# specific version of Android command line tools rather than default
# which is ``11076708`` as of writing this comment.
RUN cd /devlib/tools/android && ./install_base.sh

# Set BUILDROOT_VERSION environment variable if you want to use a specific
# branch of buildroot rather than default which is ``2023.11.1`` as of
# writing this comment.
RUN cd /devlib/tools/buildroot && \
    ./generate-kernel-initrd.sh && \
    ./generate-kernel-initrd.sh -a x86_64

# Clean unused buildroot artifacts.
RUN cd /devlib/tools/buildroot && \
    mkdir artifacts && \
    mv buildroot-v${BUILDROOT_VERSION}-aarch64/output/images artifacts/aarch64 && \
    mv buildroot-v${BUILDROOT_VERSION}-x86_64/output/images artifacts/x86_64 && \
    rm -rf buildroot-v${BUILDROOT_VERSION}-aarch64 && \
    rm -rf buildroot-v${BUILDROOT_VERSION}-x86_64
