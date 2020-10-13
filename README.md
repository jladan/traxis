# traxis

A Digital Framework for Analysis of Particle Bubble Chamber Tracks. Used in the
High Energy Physics experiment in UofT Advanced Labs.


## Description

Python-based toolkit with GUI that computes track momentum and optical density
of tracks in digitized bubble chamber images.

## Installing and Running

Traxis can now be installed with pip:

```
pip install traxis
# Then run the command
traxis
```

After installation, traxis can be run in one of 3 ways:
1. from the shell as a module `python -m traxis`
2. as a standalone executable `traxis`
3. (for backwards compatibility) using the `runtraxis` script

### Without installation
Or, from source without installation,
on Linux, UNIX, Mac:

```
tar xzvf traxis-*.tar.gz
cd traxis
python -m traxis
```

On **Windows**:

1. Extract traxis.zip
2. Go to extracted traxis folder with a command prompt
3. execute the traxis module: `python3 -m traxis`

## Dependencies

- Python (3.3+)
- numpy
- scipy
- PyQt5 (5.3+)

## Authors

Syed Haider Abidi, Nooruddin Ahmed and Christopher Dydula
