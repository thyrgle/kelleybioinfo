# Kelley Bio Info

Kelley Bio Info (www.kelleybioinfo.org) is an educational website that allows students to learn bioinformatics through solving computer generated problems. This repository is a rewrite of the current site. It is being rewritten to incorporate a new UI and a reputation/point system. This is the Github repository for the source code. It is currently, very much, a work in progress.

# Running locally

To run the source code locally, please install [git](https://git-scm.com/), [Python](https://www.python.org/) and [pipenv](https://pipenv.readthedocs.io/en/latest/). Once these are installed, you can start up a localhost by:

```
git clone https://github.com/thyrgle/kelleybioinfo.git
cd kelleybioinfo
export FLASK_APP=app
export FLASK_ENV=development
pipenv install
pipenv shell
flask run
```

# Contributing

All contributions are welcome, more information about the project will be add soon.
