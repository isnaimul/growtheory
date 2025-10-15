# official AWS Lambda base image for Python 3.13
FROM public.ecr.aws/lambda/python:3.13

# copy requirements for Docker layer caching
COPY requirements.txt .

# install dependencies, use --no-cache-dir to keep final image size small
RUN pip install --no-cache-dir -r requirements.txt

# copy our application code standard Lambda task root
COPY lambda_handler.py .
COPY agents/ ./agents/
COPY tools/ ./tools/

# set handler to file_name.function_name
CMD ["lambda_handler.lambda_handler"]