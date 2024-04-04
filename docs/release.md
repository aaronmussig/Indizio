# Release workflow

This document describes the workflow for releasing a new version of Indizio.

## 1 - Update version number

Update the version number in the following files, ideally using [Semantic Versioning](https://semver.org/):

```
pyproject.toml
```

If the next version is to be `1.0.0`, then update it to be:

```toml
version = "1.0.0"
```

## 2 - Creating a pre-release

__Note:__ To publish from CI you need to set-up
a [trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
in the [PyPI test environment](https://test.pypi.org/manage/projects/).

A GitHub workflow will automatically create a pre-release when a new pre-release is created.

Using `1.0.0` as an example for the next release, the tag should be in the format of `v1.0.0-pre.1`,
this will also be the release title.

## 3 - Testing the release

In a new virtual environment, run the following command to install Indizio from the test PyPI site:

```shell
python -m pip install -i https://test.pypi.org/simple/ indizio
```

## 4 - Publishing the release

__Note:__ The [trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) configuration
is required to publish the release from CI on the non-test PyPI site. This is accessed
under [your projects](https://pypi.org/manage/projects/).

To publish the release, create a new release on GitHub. The CI will automatically create a release on PyPI.

## 5 - Bioconda

This will be taken care of by Bioconda volunteers. You can contribute to the Bioconda recipe by joining
the [Bioconda organization](https://github.com/orgs/bioconda/people).
