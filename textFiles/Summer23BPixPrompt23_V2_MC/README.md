These are the jet energy correction text files for the `Summer23BPixPrompt23_V2` correction campaign
for 2023 samples.

The corrections should be applied to `Summer23BPix` MC simulation and 2023 prompt-reconstructed DATA. The
data corrections differ only in the `L2L3Residual` part and should be applied in the following subperiod(s):

| Year | Era/Subperiod | First run (PdmV) | Last run (PdmV)|
| ---- | ------------- | ---------------- | -------------- |
| 2023 | D             | 369803           | 372415         |


Release notes
=============

The corrections are largely identical to the previous iteration (`Summer23BPixPrompt23_V1`), but contain
fixes to the function used to fit the MC Truth (`L2Relative`) correction. In the previous version, the
corrections exhibited asymptotic behavior, leading to a very large, unphysical correction factor in a
narrow pT range for certain rapidity bins. More information can be found at the references listed below.

[1] https://gitlab.cern.ch/cms-jetmet/JERCProtoLab/-/merge_requests/94
[2] https://gitlab.cern.ch/cms-jetmet/JERCProtoLab/-/merge_requests/95
[3] https://gitlab.cern.ch/cms-jetmet/coordination/coordination/-/issues/153

