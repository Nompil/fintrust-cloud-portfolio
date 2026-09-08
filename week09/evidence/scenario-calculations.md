# Week 9 Scenario Calculations

## Savings Plans example

The Day 1 exercise supplies a $32.47 hourly commitment, a three year term and a 66 percent discount. At full utilisation, the model calculates:

| Item | Result |
| --- | ---: |
| On Demand equivalent per hour | $95.50 |
| Commitment cost over three years | $853,311.60 |
| On Demand equivalent over three years | $2,509,740.00 |
| Calculated saving over three years | $1,656,428.40 |

This does not reproduce the separate $847,000 statement in the brief. That figure needs a different commitment, term, discount or utilisation assumption. The code leaves every input visible so the business case can be corrected when the source values are confirmed.

## TCO example

Using the supplied annual on premises cost of $4,200,000, AWS monthly cost of $248,000, one time migration cost of $850,000 and 3 percent annual on premises inflation, the AWS cumulative total becomes lower during the ninth month. This is a hard cost comparison only and does not price migration risk or engineering opportunity cost.

## Snow transfer example

| Item | Result |
| --- | ---: |
| Archive size | 3,000 TB |
| Device | Snowball Edge Storage Optimised |
| Device count | 38 |
| Available capacity | 3,040 TB |
| Spare capacity | 40 TB |
| Ideal transfer time at 1 Gbps | 277.8 days |

The network estimate excludes protocol overhead and interruptions, so actual internet transfer would take longer.
