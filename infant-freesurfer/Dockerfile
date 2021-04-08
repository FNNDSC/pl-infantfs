FROM centos:7

# The image is going to be huge anyway, so it's better to use layers.
# Do slowest step first so that it's a part of the cache.
RUN curl https://surfer.nmr.mgh.harvard.edu/ftp/dist/freesurfer/infant/freesurfer-linux-centos7_x86_64-infant-dev-4a14499.tar.gz | tar xz -C /opt
# FSL required to be installed separately.
# There's an FSL install script at
# https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py
# And I have no idea what it does, so...
RUN curl https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-6.0.4-centos6_64.tar.gz | tar xz -C /opt

RUN yum install -y tcsh libgomp perl

RUN mkdir /outgoing

ENV FREESURFER_HOME=/opt/freesurfer
ENV FS_OVERRIDE=0                          \
    FSFAST_HOME=$FREESURFER_HOME/fsfast    \
    SUBJECTS_DIR=/outgoing                 \
    MINC_BIN_DIR=$FREESURFER_HOME/mni/bin  \
    MNI_DIR=$FREESURFER_HOME/mni           \
    MINC_LIB_DIR=$FREESURFER_HOME/mni/lib  \
    MNI_DATAPATH=$FREESURFER_HOME/mni/data \
    LOCAL_DIR=$FREESURFER_HOME/local       \
    FSF_OUTPUT_FORMAT=nii.gz               \
    FMRI_ANALYSIS_DIR=$FREESURFER_HOME/fsfast \
    MNI_PERL5LIB=$FREESURFER_HOME/mni/share/perl5 \
    PERL5LIB=$FREESURFER_HOME/mni/share/perl5 \
    FREESURFER=$FREESURFER_HOME

ENV FSLDIR=/opt/fsl

ENV PATH=$FREESURFER_HOME/bin:$FSFAST_HOME/bin:$MINC_BIN_DIR:$FSLDIR/bin:$FREESURFER_HOME/python/bin:$PATH
