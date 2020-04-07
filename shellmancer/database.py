import os

# # Crash and burn when env vars not set
# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         message = f"Expected environment variable for {name}; is not set"
#         raise Exception(message)
#
#
# PG_URL = get_env_variable("POSTGRES_URL")
# PG_USER = get_env_variable("POSTGRES_USER")
# PG_PW = get_env_variable("POSTGRES_PW")
# PG_DB = get_env_variable("POSTGRES_DB")
# PG_AUTH = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
#     user=PG_USER, pw=PG_PW, url=PG_URL, db=PG_DB)
#

