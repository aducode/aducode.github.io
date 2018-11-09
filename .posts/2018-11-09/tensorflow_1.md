<!--{layout:default title:tensorflow_1}-->
Tensorflow学习系列（一）
> 从源码入手学习tensorflow 第一篇主要总结一下环境的搭建

基于docker来搭建tensorflow编译环境，这样如果开发环境变了，只要重新build一遍镜像就可以了，在这里简单记录一下dockerfile

<pre class="language-sh line-number">
<code>
from ubuntu:16.04
RUN apt-get update && apt-get install -y \
    pkg-config \
    zip \
    g++ \
    zlib1g-dev \
    unzip \
    python \
    git \
    wget \
    python-pip
RUN pip install numpy \
    enum34 \
    keras_preprocessing \
    mock
RUN mkdir /workspace
WORKDIR /workspace
RUN wget https://github.com/bazelbuild/bazel/releases/download/0.18.1/bazel-0.18.1-installer-linux-x86_64.sh
RUN /bin/bash bazel-0.18.1-installer-linux-x86_64.sh
RUN echo "PATH='$PATH':$HOME/bin" >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"
RUN rm -f bazel-0.18.1-installer-linux-x86_64.sh
RUN git clone https://github.com/tensorflow/tensorflow.git
WORKDIR /workspace/tensorflow
# ./configure 这里没有执行，为了简单，可以先将cuda等关掉
RUN bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
RUN bazel-bin/tensorflow/tools/pip_package/build_pip_package  ./tensorflow_pkg
# 最后生成的whl包名可能随python版本 / config的不同会有变化
RUN pip install ./tensorflow-1.12.0rc0-cp27-cp27mu-linux_x86_64.whl
</code>
</pre>

