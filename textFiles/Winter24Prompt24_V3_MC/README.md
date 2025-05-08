These are the jet energy correction text files for the `Winter24Prompt24_V3` correction campaign
for 2024 samples.

The corrections should be applied to `Summer23BPix` MC simulation (*NB*: not `Winter24`) and `Winter24`
prompt-reconstructed DATA.

The simulated response (MC truth) corrections for DATA and MC (`L2Relative`) are identical to
the previous iteration (`Winter24Prompt24_V2`) and are based on the studies presented in [1].

The residual corrections for DATA (`L2Residual` and `L2L3Residual`) are based on `V8M` from [2].
A clipping of the residual corrections to a constant value for $p_{T} < 30$ was performed in addition
in the pseudorapidity region with (2.043 < $|\eta|$ < 2.964), following checks in [3].

[1] https://indico.cern.ch/event/1397347/#3-first-look-at-2024-mc-truth<br />
[2] https://indico.cern.ch/event/1515162/#16-raw-pt-based-jecs-for-2024<br />
[3] https://indico.cern.ch/event/1515162/#25-he-corrections-using-new-je

### Notes

The residual corrections were derived as a function of pTraw (uncorrected jet pT), in contrast to
previous versions, which were derived as a function of pTref (reference object pT).

The corrections for DATA are more granular than the usual per-era JECs. Each data-taking era is subdivided
into one or several *"nibs"*. An overview of nibs and the corresponding run ranges is given below. The
columns marked "JEC" indicate certified data runs (in the golden JSON) actually used for JEC derivation.
The columns marked "PdmV" are computed to match the official era boundaries as given in the
[PdmVRun3Analysis TWiki](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis?rev=163). For nibs that
begin in the middle of eras, the "First run (PdmV)" is defined to be the same as "First run (JEC)". When
applying the JECs in data, the correct nib should be identified by checking the run number against the
interval [First run (PdmV), Last run (PdmV)].


| Year | Era/Subperiod | Nib  | First run (PdmV) | First run (JEC) | Last run (JEC) | Last run (PdmV)|
| ---- | ------------- | ---- | ---------------- | --------------- | -------------- | -------------- |
| 2024 | B             | nib1 | 378971           | 378985          | 379355         | 379411         |
| "    | C             | nib1 | 379412           | 379416          | 380236         | 380252         |
| "    | D             | nib1 | 380253           | 380306          | 380947         | 380947         |
| "    | Ev1           | nib1 | 380948           | 380963          | 381380         | 381383         |
| "    | Ev2           | nib1 | 381384           | 381384          | 381544         | 381943         |
| "    | F             | nib1 | 381944           | 382229          | 382262         | 382297         |
| "    | "             | nib2 | 382298           | 382298          | 383175         | 383246         |
| "    | "             | nib3 | 383247           | 383247          | 383779         | 383779         |
| "    | G             | nib1 | 383780           | 383811          | 384644         | 384932         |
| "    | "             | nib2 | 384933           | 384933          | 385801         | 385813         |
| "    | H             | nib1 | 385814           | 385836          | 386319         | 386408         |
| "    | I             | nib1 | 386409           | 386478          | 386951         | 387121         |

