# I wouldn't use this for something production, I'd build my own image based off the official python docker image
# This was used in the interest of saving time
FROM kennethreitz/pipenv
CMD celery -A event_target worker -l info
