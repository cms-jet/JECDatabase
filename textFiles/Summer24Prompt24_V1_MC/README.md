These are the jet energy correction text files for the `Summer24Prompt24_V1` correction campaign
for 2024 samples.

The corrections should be applied to `Summer24' MC samples and Reprocessed EraCDE and Prompt-reconstructed EraFGHI DATA.

The simulated response (MC truth) corrections for DATA and MC (`L2Relative`)  are based on the studies presented in [1].

The residual corrections for DATA (`L2Residual` and `L2L3Residual`) are based on `V9M` from [2].

[1] https://indico.cern.ch/event/1545816/#36-l2rel-for-winter25<br />
[2] https://indico.cern.ch/event/1552944/#36-first-look-into-2025-data-g<br />

### Notes

The residual corrections were derived as a function of pTraw (uncorrected jet pT)

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
| 2024 | C             | nib1 | 379412           | 379416          | 380236         | 380252         |
| "    | D             | nib1 | 380253           | 380306          | 380947         | 380947         |
| "    | E             | nib1 | 380948           | 380963          | 381544         | 381943         |
| "    | F             | nib1 | 381944           | 382229          | 382262         | 382297         |
| "    | "             | nib2 | 382298           | 382298          | 383175         | 383246         |
| "    | "             | nib3 | 383247           | 383247          | 383779         | 383779         |
| "    | G             | nib1 | 383780           | 383811          | 384644         | 384932         |
| "    | "             | nib2 | 384933           | 384933          | 385801         | 385813         |
| "    | H             | nib1 | 385814           | 385836          | 386319         | 386408         |
| "    | I             | nib1 | 386409           | 386478          | 386951         | 387121         |

