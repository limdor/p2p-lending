# P2P Lending Reporting

This is a small Python program to unify the data comming from different P2P lending platforms.
For the moment the following platforms are supported:

* [Mintos](https://www.mintos.com/)
* [Iuvo](https://www.iuvo-group.com/)

## Usage

To create the report you can run the program with the following command:

```bash
bazel run //:main
```

If you want to see the report also for the past investments you can pass `--past` as a parameter:

```bash
bazel run //:main -- --past
```

For a full list of parameters you can use `--help`:

```bash
bazel run //:main -- --help
```

## Running the tests

To run the test you just need to run the following command:

```bash
bazel test //...
```

## Deploy

To deploy the application to google cloud you only have to follow the instructions in this page:
<https://datasciencecampus.github.io/deploy-dash-with-gcp/>

Currently the deployment is not fully automated, there are two parts that needs to be modified:

* The logging to file needs to be commented out because in the server we cannot write to file
* Some of the imports needs to be changed because in the server is not run with Bazel

In file dashboard/components.py:

```py
import figures
```

for

```py
from dashboard import figures
```

In file dashboard/dashboard.py:

```py
import charts
import components
import layouts
import tables
```

for

```py
from dashboard import charts
from dashboard import components
from dashboard import layouts
from dashboard import tables
```
