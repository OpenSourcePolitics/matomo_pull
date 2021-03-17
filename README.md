# matomo_import
## Purpose
The aim of the script provided is to pull data from a [Matomo](matomo.org) instance, put it in a database that will then be usable in a data analyse tool (in our case, the software used after is [Metabase](metabase.com)).



## Getting startd
### Requirements
- Python >= 3.8
- Strongly recommended : a virtual environment manager (the one used for this project is [pew](https://github.com/berdario/pew))

### Setup
- Create a `secrets.yml` containing informations for Matomo connection and wanted tables. The file `secrets-example.yml` provided give a good outlook of what is possible. Please refer the Matomo API documentation if wanted to add URL parameters when doing the API calls)
- `pip install -r requirements.txt` 
- `python main.py`
- Gather the database file/ database informations created and use it for your data analysis

## Next steps

- [x] `secrets.yml` file configuration
- [x] Add `requirements.txt`
- [x] Add minimal tests
- [ ] Refactoring
  - [ ] Remove global variables
  - [ ] Docstrings and working schemes
- [ ] Add postgres database management