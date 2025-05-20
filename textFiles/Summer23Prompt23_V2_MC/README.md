These are the jet energy correction text files for the `Summer23Prompt23_V2` correction campaign
for 2023 samples.

The corrections should be applied to `Summer23` MC simulation and 2023 prompt-reconstructed DATA. The
data corrections differ only in the `L2L3Residual` part and should be applied in the following subperiod(s):

| Year | Era/Subperiod | First run | Last run |
| ---- | ------------- | --------- | -------- |
| 2023 | Cv123         | 367080    | 367764   |
| "    | Cv4           | 367765    | 369802   |


Release notes
=============

The corrections are largely identical to the previous iteration (`Summer23Prompt23_V1`), but contain
a clipping of the residual corrections to a constant value for $p_{T} < 30$ in the pseudorapidity region
with (1.305 < $|\eta|$ < 2.500), following checks detailed in Refs. [2-4]. The $|\eta|$
bins for the $p_{T}$ clipping are given by: [1.305, 1.479, 1.653, 1.930, 2.172, 2.322, 2.500].

The residual corrections for DATA (`L2Residual` and `L2L3Residual`) are based on `V2`, as presented
in Ref. [1] below. More information can be found at the GitLab issue linked as Ref. [2].

References
==========

[1] https://indico.cern.ch/event/1389009/#4-virtual-l2l3res-for-summer23
[2] https://gitlab.cern.ch/cms-jetmet/coordination/coordination/-/issues/124

