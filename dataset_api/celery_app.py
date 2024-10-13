from dataset_api.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("dataset_api.tasks.example",)
