# pl-infantfs

A _ChRIS_ plugin for the `infant_recon_all` command from Infant FreeSurfer.

https://surfer.nmr.mgh.harvard.edu/fswiki/infantFS

## Installation

FreeSurfer and FSL are _not_ free software ("Free" as in "freedom").
Briefly, you may not use this software for financial gain.

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

# GPU

Upstream bug, GPU is not supported at the moment.

- [`--usegpu` doesn't actually do anything](https://github.com/freesurfer/freesurfer/blob/e34ae4559d26a971ad42f5739d28e84d38659759/infant/infant_recon_all#L159)
- [`--gpuid` is eventually passed to `sscnn_skullstrip` which uses its value to be `CUDA_VISIBLE_DEVICES`](https://github.com/freesurfer/freesurfer/blob/e34ae4559d26a971ad42f5739d28e84d38659759/sscnn_skullstripping/sscnn_skullstrip#L43)

Python + Tensorflow v1.5.0 distribution bundled with InfantFS version _dev-4a14499_
does not support GPU.

```bash
# actual
$ fspython -c 'import tensorflow as tf; from tensorflow.python.client import device_lib; print(device_lib.list_local_devices())'
2021-04-08 19:11:16.138785: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 AVX512F FMA
[name: "/device:CPU:0"
device_type: "CPU"
memory_limit: 268435456
locality {
}
incarnation: 5995910486109130540
]
# control
docker run --rm --gpus all -it tensorflow/tensorflow:1.5.0-gp
u-py3 python -c 'import tensorflow as tf; from tensorflow.python.client import device_lib; print(device_lib.list_local_devices())'
/usr/local/lib/python3.5/dist-packages/h5py/__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
  from ._conv import register_converters as _register_converters
2021-04-08 23:17:58.239399: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 AVX512F FMA
2021-04-08 23:17:58.587597: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1105] Found device 0 withproperties:
name: TITAN V major: 7 minor: 0 memoryClockRate(GHz): 1.455
pciBusID: 0000:af:00.0
totalMemory: 11.78GiB fre[name: "/device:CPU:0"eMemory: 11.47GiB
2021-04-08 23:17:58.772920: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1105] Found device 1 withproperties:
name: TITAN V major: 7 minor: 0 memoryClockRate(GHz): 1.455
pciBusID: 0000:d8:00.0
totalMemory: 11.78GiB freeMemory: 11.44GiB
2021-04-08 23:17:58.774606: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Device peer to peermatrix
2021-04-08 23:17:58.774640: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1126] DMA: 0 1
2021-04-08 23:17:58.774651: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1136] 0:   Y Y
2021-04-08 23:17:58.774660: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1136] 1:   Y Y
2021-04-08 23:17:58.774675: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1195] Creating TensorFlowdevice (/device:GPU:0) -> (device: 0, name: TITAN V, pci bus id: 0000:af:00.0, compute capability: 7.0)
2021-04-08 23:17:58.774687: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1195] Creating TensorFlowdevice (/device:GPU:1) -> (device: 1, name: TITAN V, pci bus id: 0000:d8:00.0, compute capability: 7.0)

device_type: "CPU"
memory_limit: 268435456
locality {
}
incarnation: 14457457194204693665
, name: "/device:GPU:0"
device_type: "GPU"
memory_limit: 11640478106
locality {
  bus_id: 2
}
incarnation: 14185840879566327940
physical_device_desc: "device: 0, name: TITAN V, pci bus id: 0000:af:00.0, compute capability: 7.0"
, name: "/device:GPU:1"
device_type: "GPU"
memory_limit: 11609971098
locality {
  bus_id: 2
}
incarnation: 4912254482941708975
physical_device_desc: "device: 1, name: TITAN V, pci bus id: 0000:d8:00.0, compute capability: 7.0"
]
```
