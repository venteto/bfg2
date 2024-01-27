"""
gunicorn config for the responder service (i.e., the feeds server)
"""

bind = '0.0.0.0:8080'

# https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads
workers = 1

# https://github.com/MarshalX/atproto/discussions/243#discussioncomment-8126323
# threads = 2  # 4

# timeout = 120
# forwarded_allow_ips = '*'
# secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

"""
use a socket?
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
"""
