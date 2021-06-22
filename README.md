# pl-infantfs

A _ChRIS_ plugin for the `infant_recon_all` command from Infant FreeSurfer.

https://surfer.nmr.mgh.harvard.edu/fswiki/infantFS

## Installation

WARNING: the publicly provided copies of this software on _Github_, _Docker Hub_,
and _chrisstore.co_ **do not work** as-is!

FreeSurfer and FSL are _not_ free software ("Free" as in "freedom").
Briefly, you may not use this software for financial gain.

We are not allowed to share a complete version of Infant FreeSurfer on DockerHub.
Instead, we only provide an unlicensed version.

https://hub.docker.com/r/fnndsc/pl-infantfs

You must add a FreeSurfer license.
Get one for free from https://surfer.nmr.mgh.harvard.edu/fswiki/License

Next, create a new container image which includes the license.

```bash
docker pull fnndsc/pl-infantfs:7.1.1.1-unlicensed
docker create --name=unlicensed-freesurfer fnndsc/pl-infantfs:7.1.1.1-unlicensed
docker cp license.txt unlicensed-freesurfer:/opt/freesurfer/.license
docker commit unlicensed-freesurfer pl-infantfs:7.1.1.1
docker rm unlicensed-freesurfer
```

To register `pl-infantfs` in _ChRIS_ you must upload it manually to a _private_
instance of the *ChRIS_store*.
*ChRIS* admins may also find it useful to first push `pl-infantfs` to a _private_
container registry.

```bash
# Example: A private container registry is running at rc-gitlab.chboston.org:4567
#          A private ChRIS_store is running at http://chris-store.tch.harvard.edu/

docker tag pl-infantfs:7.1.1.1 rc-gitlab.chboston.org:4567/fnndsc/pl-infantfs:7.1.1.1
docker push rc-gitlab.chboston.org:4567/fnndsc/pl-infantfs:7.1.1.1

docker run --rm rc-gitlab.chboston.org:4567/fnndsc/pl-infantfs:7.1.1.1 infantfs --json > /tmp/infantfs.json
http -a chrisadmin:chris1234 -f POST http://chris-store.tch.harvard.edu/api/v1/plugins/ \
    dock_image=rc-gitlab.chboston.org:4567/fnndsc/pl-infantfs:7.1.1.1 \
    descriptor_file@/tmp/infantfs.json \
    public_repo=https://github.com/FNNDSC/pl-infantfs \
    name=pl-infantfs
```

## Usage

The required input are a single NIFTI (`*.nii.gz`) file and the subject's age in months.

Traditional `infant_recon_all`-like usage is supported.

```bash
mkdir -p incoming/123456
cp t1.nii.gz incoming/123456/mprage.nii.gz
mkdir outgoing
singularity exec docker-daemon://pl-infantfs:7.1.1.1 --subject 123456 --age 6 incoming/ outgoing/
```

Alternatively, use `--inputPathFilter` to specify the input file by a glob pattern.
If `--subject` is not given, then the default value for `--inputPathFilter`, which is
`*.nii.gz`, the NIFTI file inside the input directory will be processed.
The directory structure will be created automatically.

```bash
mkdir incoming outgoing
cp t1.nii.gz incoming
singularity exec docker-daemon://pl-infantfs:7.1.1.1 --age 6 incoming/ outgoing/
```
