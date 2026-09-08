# Pricing and Business Case

## Workload choices

FinTrust should measure a new workload on On Demand pricing before committing to a term. Stable EC2 capacity in one family and region can use an EC2 Instance Savings Plan. The mixed estate uses EC2, Fargate and Lambda across accounts and regions, so a Compute Savings Plan is the more practical organisation level commitment. Spot capacity is limited to restartable work such as EMR Task nodes and development jobs. Payment processing and persistent data tiers do not tolerate interruption. Dedicated Hosts are reserved for the interim Oracle deployment because the licence is tied to physical sockets.

## TCO boundary

The TCO comparison includes hardware, storage, network contracts, facilities, power, cooling, licences and operational labour. It also includes AWS usage, support, data transfer and the one time migration cost. Migration risk, engineering opportunity cost and business value are described separately because assigning them an unsupported cash amount would make the model look more precise than it is.

The supplied scenario gives an on premises three year cost of R687 million and an AWS three year cost of R227 million. That produces a R460 million gross difference. A separate page calls R142 million the net board case after migration costs but does not provide the adjustment detail. Both figures are retained with their definitions rather than combined.

## Savings Plans figures

The course material also uses more than one commitment example. The Python model accepts commitment, discount, term and utilisation as inputs, then shows the arithmetic. It does not label the supplied $847,000 figure as reproduced unless the chosen inputs actually produce that result. This matters because an unused hourly commitment continues to be charged.
