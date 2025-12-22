Generate 11 presentation slides based on the podcast about Membership Inference Attacks from First Principles by Nicholas Carlini et al.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Privacy Challenge in AI Training

- AI models trained on massive datasets containing personal information (emails, medical records, purchase history)
- Fundamental question: Do models memorize specific training examples and potentially leak them?
- Membership Inference Attacks test whether specific data points were in the training set
- Previous evaluation methods provided false sense of security
- Google researchers reveal fundamental flaws in how we measure privacy

## Slide 2: Traditional Loss-Based Attacks

- Loss function measures model confidence - lower loss means higher certainty
- Basic assumption: model shows low loss on training data it has seen thousands of times
- Attack strategy: set threshold, classify examples below threshold as training members
- Simple and intuitive approach used widely in industry
- Critical flaw hidden in evaluation methodology

## Slide 3: The Problem with Balanced Attack Accuracy

- Standard metric: Balanced Attack Accuracy (simple average of success rates)
- Example: Attack A identifies 0.1% of users with 100% precision but fails on remaining 99.9%
- Example: Attack B guesses randomly with 50% accuracy across all users
- Both attacks score 50% Balanced Accuracy despite vastly different real-world impact
- Averaging obscures which attacks pose genuine privacy threats

## Slide 4: True Positive Rate at Fixed False Positive Rate

- New rigorous metric: TPR@FPR (True Positive Rate at Fixed False Positive Rate)
- Fix acceptable false alarm rate (e.g., 0.1%) then measure successful identifications
- Mimics real-world constraints where false accusations have consequences
- Forces evaluation at operationally relevant thresholds
- Attack A would show high TPR, Attack B near zero - reveals true threat level

## Slide 5: LIRA - Likelihood Ratio Attack Architecture

- First pillar: Per-example hardness - each data point has unique difficulty profile
- Some examples are "inliers" (typical), others "outliers" (unusual for the model)
- Instead of single global threshold, LIRA learns individual profile for each example
- Compares probability of seeing model output when trained WITH vs WITHOUT specific data
- Bayesian approach: which scenario is more likely given observed model behavior?

## Slide 6: Logit Scaling Mathematical Transform

- Second pillar: LIRA applies logit scaling to model confidence scores
- Transforms arbitrary output distributions into normal (Gaussian) distributions
- Normal distributions characterized by just two parameters (mean and standard deviation)
- Dramatically simplifies statistical modeling and reduces computational requirements
- Attacker needs fewer "shadow models" (training clones) to achieve same or better results

## Slide 7: LIRA Performance Results

- 10x improvement over previous state-of-the-art attacks
- CIFAR-10 dataset: at FPR=0.1%, LIRA achieves TPR=8.4%
- Best competing method: only 1.7% TPR
- Many popular previous methods showed TPR near 0% (essentially random guessing)
- LIRA operates in "different league" - previous benchmarks obsolete

## Slide 8: Implications for Defense and Auditing

- Many defensive mechanisms discarded based on old tests may be effective against LIRA
- Security audits from 5+ years ago potentially invalid with new attack methodology
- Models previously certified as "secure" may be vulnerable when tested rigorously
- Need systematic re-evaluation of deployed systems using TPR@FPR metrics
- Privacy guarantees only as good as the attacks used to test them

## Slide 9: Overfitting Does Not Predict Vulnerability

- Conventional wisdom: overfitting correlates with membership inference vulnerability
- Figure 7 shows models with identical overfitting levels differ 100x in attack susceptibility
- Higher test accuracy models sometimes MORE vulnerable despite better generalization
- Overfitting alone does not explain which examples are memorized
- Simple heuristics fail to predict actual privacy risk

## Slide 10: Outliers Are Most Vulnerable

- Experiment: injected mismatched images into CIFAR-10 training set
- Unusual, outlier examples were radically easier for LIRA to identify
- Models most strongly memorize unique, surprising, or atypical data points
- Practical implication: rare edge cases and anomalies pose highest privacy risk
- Figure 11: LIRA robust even when attacker lacks exact architecture knowledge

## Slide 11: Question for You

Can perfect privacy and maximum model performance ever be fully reconciled, or will there always be a fundamental tradeoff between memorization and accuracy?
