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
