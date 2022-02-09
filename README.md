# matomo_import
## Purpose
The aim of the script provided is to pull data from a [Matomo](matomo.org) instance into a Postgres database, database that will then be usable in a data analysis tool. In our case, the software used after is [Metabase](metabase.com), but it can suit all software accepting that format of database.



## Getting started
### Requirements
- Python >= 3.8
- pip >= 21.x.x
- **Strongly recommended** : a virtual environment manager (the one used for this project is [pew](https://github.com/berdario/pew)).
- An admin access to your Matomo instance to retrieve the API key
- A Postgres instance(either your local machine, or a remote installation)

### How does it work
- A python script will run API calls toward your Matomo instance, retrieving relevant data and fill the Postgres database.
- You can export that file into your Metabase instance (or any other data analysis tool), setup the database, and write your questions.

### Setup
1. Optional : modify the `config.yml` file containing informations related to data you want to pull. The current one contains already many different informations that can be pulled out Matomo.
2. Create a `.env` file containing all informations concerning parameters needed for the script to run. You can copy the `.env.example` file given in this repository.
    - `base_url` : the URL of your Matomo instance (e.g. : `https://matomo.yoursite.com/`, ⚠️ the ending slash is mandatory)
    - `db_name` : the name of the Postgres database that will contain all data
    - `id_site` : id of the site you want to pull information from. Available via Matomo
    - `start_date` : date from which you want to import data. Format `YYYY-MM-DD`, like `2021-11-23` as instance.
    - `token_auth` : the API token provided on your Matomo instance.
    - `end_date` (optional) : same format as start date. When set, the database will only contain data within the date range given.


3. Run the following comand : `pip install -r requirements.txt` to install relevant packages
4. Run the following command to obtain your data : `python -c "import main; import os; os.environ['JWT_SECRET_KEY']='anonymous'; main.exec()"`
5. Gather the database file/ database informations created and use it for your data analysis

## Improve/contribute
Any help to improve this script is welcome ! Do not hesitate to write issues/PRs to improve that script, see the CONTRIBUTE.adoc file.

TL;DR:
- write issues if you got problems or want to improve the project
- do not hesitate to make PRs
- validation workflow: be sure that test and syntax workflow works before asking for review

## Next steps

- [x] `config.yml` file configuration
- [x] Add `requirements.txt`
- [x] Add minimal tests
- [x] Env variables for critical parameters
- [ ] Adapt to obtain a postgres-data format
- [ ] Update README for container-use