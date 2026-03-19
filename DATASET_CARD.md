---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- asymflation
- computational-economics
- macroeconomics
- emerging-terminology
pretty_name: Asymflation Economics Dataset
size_categories:
- n<1K
---

# Asymflation Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Asymflation` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Macroeconomics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `month`: Synthetic monthly period
- `input_cost_shock`: Input cost shock intensity
- `price_increase_speed`: Speed of upward price adjustment
- `price_decrease_speed`: Speed of downward price adjustment
- `inflation_expectations`: Expected inflation
- `market_power`: Markup/market power proxy
- `wage_rigidity`: Downward wage rigidity proxy
- `pass_through_gap`: Gap between upward and downward pass-through
- `asymflation_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Asymflation applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{asymflation2026,
title={{Asymflation Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
