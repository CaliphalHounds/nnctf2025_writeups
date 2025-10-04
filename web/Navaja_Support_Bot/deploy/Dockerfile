# Use latest Python 3.12 slim image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BROWSER_SLEEP=3
ENV ADMIN_PASS=ksdjn8u719384jhnskfadjnloiujfds!676FGFGHDhj
ENV SECRET_KEY=asdojgvuyhbv91238476HJIKSAF())(dasdhbjasdhggu7y123414
ENV FLAG=nnctf{4_p0r_l4_cSp_4m1gu1llo}



RUN apt-get update -y && apt-get install -y wget


RUN apt-get update && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies for pip and building packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy the application code
COPY app .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["gunicorn", "-w", "1", "--threads", "100", "-b", "0.0.0.0:5002", "app:app"]
