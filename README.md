# matomo_import
## Purpose
The aim of the script provided is to pull data from a [Matomo](matomo.org) instance, put it in a database that will then be usable in a data analyse tool (in our case, the software used after is [Metabase](metabase.com)).



## Getting started
### Requirements
- Python >= 3.8
- Strongly recommended : a virtual environment manager (the one used for this project is [pew](https://github.com/berdario/pew))

### Setup
- Create a `config.yml` file containing informations for Matomo connection and wanted tables. The file `config-example.yml` provided give a good outlook of what is possible (please refer the Matomo API documentation if wanted to add URL parameters when doing the API calls)
- Create a `.env` file containing all informations concerning parameters that should stay hidden. The file `.env.example` provided give minimal variables to be filled.
- `pip install -r requirements.txt` 
- `python main.py`
- Gather the database file/ database informations created and use it for your data analysis

## Next steps

- [x] `config.yml` file configuration
- [x] Add `requirements.txt`
- [x] Add minimal tests
- [x] Env variables for critical parameters
- [ ] Refactoring
  - [ ] Remove global variables
  - [ ] Docstrings and working schemes
