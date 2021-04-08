FROM fnndsc/infant-freesurfer:dev-4a14499-unlicensed

RUN yum install -y -q python3

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install .

CMD ["infantfs", "--help"]
