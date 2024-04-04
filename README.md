# Indizio 

Visualization dashboard for presence/absence data, distance matrices, and phylogenetic trees.

## 1 - Installation

_Windows support has not tested, it is recommended to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)._

It is strongly recommended to install Indizio into a virtual environment, either by using [venv](https://docs.python.org/3/library/venv.html), or [Conda](https://anaconda.org/)/[Mamba](https://mamba.readthedocs.io/en/latest/).

__1.1 - PyPI:__

Once you have activated your virtual environment, run:

```shell
python -m pip install indizio
```

__1.2 - Conda:__

_If you are using mamba, simply replace `conda` with `mamba`._

```shell
conda create -n indizio -c conda-forge -c bioconda indizio
```

## 2 - Usage

__2.1 Quick start:__

Activate the virtual environment you installed Indizio in, then simply run the following command:
```shell
indizio
```

Additional options can be viewed by running:

```shell
indizio --help
```

__2.2 Details:__

The major feature of the Inidizio tool is the interactive Dash application.
The Indizio dash tool is primarily used to identify and visualize correlations among features in a sample set.

Indizio is flexible with the number of files that can be used as input. As a bare minimum, Indizio requires either a presence/absence table of features in samples or a feature-wise distance matrix. If a presence/absence table is supplied, Indizio will calculate a simple Pearson correlation among features.

Users may supply as many distance matrices as the would like.

Users may also supply metadata. These metadata are meant to be correlations of features to specific labels. At this time, only feature-wise metadata are supported.

Finally, users may upload a phylogenetic tree or similar sample dendrogram file. If both a tree and sample-wise feature presence/absence table are uploaded, Indizio will generate clustergrams.
