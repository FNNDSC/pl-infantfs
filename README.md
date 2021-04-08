# pl-infantfs

A _ChRIS_ plugin for the `infant_recon_all` command from Infant FreeSurfer.

https://surfer.nmr.mgh.harvard.edu/fswiki/infantFS

## Installation

FreeSurfer is _not_ free software ("Free" as in "freedom").
You must add a FreeSurfer license.
Get one for free from https://surfer.nmr.mgh.harvard.edu/fswiki/License

Then add it to the container

```bash
docker create --name=unlicensed-freesurfer fnndsc/pl-infantfs:7.1.1.1-unlicensed
docker cp license.txt unlicensed-freesurfer:/opt/freesurfer/.license
docker commit unlicensed-freesurfer registry.internal/fnndsc/pl-infantfs:7.1.1.1
docker rm unlicensed-freesurfer
```

## Usage

The required input are a single NIFTI (`*.nii`, `*.nii.gz`) file and the subject's age in months.

Traditional `infant_recon_all`-like usage is supported.

```bash
mkdir -p incoming/123456
cp t1.nii.gz incoming/123456/mprage.nii.gz
mkdir outgoing
singularity exec docker://registry.internal/fnndsc/pl-infantfs:7.1.1.1 --subject 123456 --age 6 incoming/ outgoing/
```

Alternatively, use `--inputPathFilter` to specify the input file by a glob pattern.
If `--subject` is not given, then the default value for `--inputPathFilter`, which is
`*.nii.gz`, the NIFTI file inside the input directory will be processed.
The directory structure will be created automatically.

```bash
mkdir incoming outgoing
cp t1.nii.gz incoming
singularity exec docker://registry.internal/fnndsc/pl-infantfs:7.1.1.1 --age 6 incoming/ outgoing/
```
