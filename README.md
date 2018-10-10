# globus-data-portal

This is a web application for scheduling Globus transfers. It is only a very rough prototype.

## Installation

To install all dependencies,

```shell
> conda env create -f environment.yml
> source activate globus-task-scheduler
```

If you don't want to use Anaconda, you can install all of the dependencies in `environment.yml` by hand with `pip`. To start the app,

```shell
> ./run_app.sh
```

## Authentication
In lieu of actually login functionality, you'll need to set two environment variables in order to authenticate against the Globus API,

* `GLOBUS_PORTAL_CLIENT`
* `GLOBUS_PORTAL_REFRESH_TOKEN`

See the [Globus SDK docs](https://globus-sdk-python.readthedocs.io/en/stable/tutorial/) for instructions on how to set these.