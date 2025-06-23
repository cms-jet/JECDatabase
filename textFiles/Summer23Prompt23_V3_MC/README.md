These are the jet energy correction text files for the `Summer23Prompt23_V3` correction campaign
for 2023 samples.

The corrections should be applied to `Summer23` MC simulation and 2023 prompt-reconstructed DATA. The
data corrections differ only in the `L2L3Residual` part and should be applied in the following subperiod(s):

| Year | Era/Subperiod | First run | Last run |
| ---- | ------------- | --------- | -------- |
| 2023 | Cv123         | 367080    | 367764   |
| "    | Cv4           | 367765    | 369802   |


Release notes
=============

The corrections are largely identical to the previous iteration (`Summer23Prompt23_V2`), but contain
fixed asymmtotic issues in AK8 as in the gitlab issue [1].

References
==========

[1] https://gitlab.cern.ch/cms-jetmet/JERCProtoLab/-/commit/c823b8c56e8bc9afa695516dcb5cc4c1ec189082

