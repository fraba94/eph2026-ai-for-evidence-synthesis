# ROBINS-I and RoB 2 at a glance

A summary in our own words of facts checked on 3 November 2026 in the Cochrane Handbook for Systematic Reviews of Interventions (version 6.5, 2024: chapter 8, last updated October 2019; chapter 25, last updated October 2019) and on https://www.riskofbias.info. It is a map, not the tool. **The signalling questions are not reproduced here**: RoB 2, ROBINS-I, ROBINS-E and ROB-ME are licensed by their developers under CC BY-NC-ND 4.0. Download the current official forms and guidance from https://www.riskofbias.info and use them as they are.

## ROBINS-I (version 2016) - non-randomised studies of interventions

Sterne JA, Hernán MA, Reeves BC, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ 2016;355:i4919. doi:10.1136/bmj.i4919 (PubMed 27733354).

**Idea.** Each study is compared with a *target trial*: a hypothetical pragmatic randomised trial of the same interventions in the same kind of participants, without features that would put it at risk of bias. It does not need to be feasible or ethical.

**Before assessing (protocol):** list the important confounding domains and the co-interventions of concern (Handbook 25.3).

| # | Domain |
|---|---|
| 1 | Bias due to confounding |
| 2 | Bias in selection of participants into the study |
| 3 | Bias in classification of interventions |
| 4 | Bias due to deviations from intended interventions |
| 5 | Bias due to missing data |
| 6 | Bias in measurement of the outcome |
| 7 | Bias in selection of the reported result |

**Judgements** (domain and overall): Low, Moderate, Serious, Critical, No information.

**Overall judgement** (Handbook table 25.3.c, paraphrased): low only if all domains are low; moderate if all domains are low or moderate; serious if at least one domain is serious and none is critical; critical if at least one domain is critical. A domain judgement implies an overall risk at least that severe; several moderate domains can justify serious overall, several serious domains can justify critical. Reviewers can depart from a proposed judgement with a written justification.

**Designs relevant to the workshop.** Handbook section 25.5 addresses uncontrolled before-after studies, including interrupted time series, for the effect of assignment to the intervention; section 25.6 addresses controlled before-after studies, including controlled interrupted time series. Typical issues in hand hygiene studies: secular trends, co-interventions (other infection prevention measures), changes in surveillance definitions or case-mix between periods, phased implementation without a clear start, choice among several models or time points.

**ROBINS-I V2.** A revised version was released on 20 November 2025 and is still labelled draft by its developers ("subject to change"); it covers follow-up (cohort) studies and reorganises the domains (for example, confounding with intention-to-treat and per-protocol variants). The Handbook's chapter 25 still describes the 2016 tool. Name the version you use; do not mix their domains.

## RoB 2 - randomised trials

Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ 2019;366:l4898. doi:10.1136/bmj.l4898 (PubMed 31462531).

**Unit.** One result: the effect of an experimental intervention versus a comparator on one outcome at one time point, for the effect of assignment or of adhering to the intervention. Different results of the same trial can have different judgements. Use the variant for the design (individually randomised parallel, cluster randomised, crossover).

| # | Domain |
|---|---|
| 1 | Bias arising from the randomization process |
| 2 | Bias due to deviations from intended interventions |
| 3 | Bias due to missing outcome data |
| 4 | Bias in measurement of the outcome |
| 5 | Bias in selection of the reported result |

**Signalling-question answers:** Yes, Probably yes, Probably no, No, No information (Not applicable where a question depends on an earlier answer).

**Judgements** (domain and overall): Low risk of bias, Some concerns, High risk of bias. The tool's algorithms propose a domain judgement from the answers; reviewers can override it with a justification.

**Overall judgement** (paraphrased): low if all domains are low; some concerns if at least one domain raises some concerns and none is high; high if at least one domain is high, or several domains raise some concerns in a way that substantially lowers confidence in the result.

## Evidence on LLMs for risk-of-bias assessment (checked on PubMed)

- Huang J, Lai H, Zhao W, et al. Large language model-assisted risk-of-bias assessment in randomized controlled trials using the revised risk-of-bias tool: evaluation study. J Med Internet Res 2025;27:e70450. doi:10.2196/70450. Overall-judgement accuracy 57.5-70% against Cochrane reviews; about 83% at signalling-question level; deriving domain judgements from LLM signalling answers with the RoB 2 algorithm improved accuracy compared with direct LLM judgements.
- Lai H, Ge L, Sun M, et al. Assessing the risk of bias in randomized clinical trials with large language models. JAMA Netw Open 2024;7(5):e2412687. doi:10.1001/jamanetworkopen.2024.12687. 30 trials, modified Cochrane tool: high correct-assessment rates overall, but sensitivity below 0.80 in some domains and F1 below 0.50 in others.

Small samples, specific models and prompts: these figures do not transfer to your model, your tool version or your studies. Pilot on studies the team has already assessed.
