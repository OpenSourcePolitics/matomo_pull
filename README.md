# matomo_import

Describe all work done for importing data through Matomo API into a database file usable for data analysis

## Setup

- Create a `secrets.yml` containing informations for Matomo connection and wanted databases
- `pip install -r requirements.txt` (you may use a virtualenv like [pew](https://github.com/berdario/pew) for that)
- `python main.py`
- Gather the file created and use it for your data analysis

## Next steps

- [ ] `secrets.yml` file configuration
- [ ] Add tests & refactor
- [x] Add `requirements.txt`
