# Python and QuickSight for Cost Reporting

The Python report is suited to scheduled distribution. It can apply the same calculation every month, keep the report in a controlled S3 prefix and send a small result to account owners who do not use QuickSight. It is also easier to join the returned values with an internal budget file before publishing. EventBridge Scheduler and Lambda would run it after the month closes.

QuickSight is better for interactive investigation. A finance analyst can filter by account, service, date or cost centre, drill from a monthly total into a resource group and compare several views without changing code. I would run the Python report for the monthly cost pack and open QuickSight when a budget alert needs further investigation.
