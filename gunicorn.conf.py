from multiprocessing import cpu_count

bind = "0.0.0.0:8000"
workers = (cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "warning"
