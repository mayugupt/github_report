FROM python:3
RUN mkdir /opt/github_report
RUN pip install requests
WORKDIR /opt/github_report
COPY . .
CMD [ "python", "pullrequests.py"]