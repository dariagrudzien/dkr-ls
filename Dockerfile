FROM        python:3.8-buster

ENV LC_ALL en_US.UTF-8

# Preparing single directory for all operations
RUN mkdir /app/
WORKDIR /app/

COPY setup.py /app/
RUN pip install -e .

COPY *.md /app/
COPY *.py /app/


# Initialize volume backup
ENTRYPOINT [ "./dkrls.py" ]
