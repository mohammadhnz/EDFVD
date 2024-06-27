# Real-Time EDF-VD with MSRP and Core Assignment with Resource Congestion and Utilization
Overview
This project is dedicated to implementing an advanced scheduling algorithm specifically designed for mixed-criticality systems in real-time environments. The focus is on integrating the Earliest Deadline First with Virtual Deadlines (EDF-VD) algorithm alongside the Multiprocessor Synchronization Protocol for Real-Time (MSRP) to handle resource sharing constraints effectively. This implementation aims to enhance system responsiveness and ensure timely task completion in critical system operations, making it highly suitable for applications requiring stringent temporal guarantees.
update in this way:
we used this algorithm to scheduling tasks and used craetive algorithm based on resource congestion and core utilization to assign tasks to core. Also for task generation we enhanced uunifast

# Results
### Results

Overall, we used six different scenarios for evaluation:

- Number of tasks: 100, Number of cores: 2, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.25
- Number of tasks: 100, Number of cores: 2, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.5
- Number of tasks: 100, Number of cores: 4, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.25
- Number of tasks: 100, Number of cores: 4, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.5
- Number of tasks: 100, Number of cores: 8, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.25
- Number of tasks: 100, Number of cores: 8, Ratio of high criticality tasks to low criticality tasks: Equal, Core utilization: 0.5
<img width="859" alt="Screenshot 1403-04-07 at 6 06 13 in the evening" src="https://github.com/mohammadhnz/Real-Time-Systems-Projects/assets/59181719/7a7a1ad6-e0f9-42c4-a089-905d39e106d8">
<img width="844" alt="Screenshot 1403-04-07 at 6 06 24 in the evening" src="https://github.com/mohammadhnz/Real-Time-Systems-Projects/assets/59181719/2171ed82-a0e7-4b59-80c8-f6e678e73b03">


# Contributers:
  1. MohammadAli HosseinNejad
  2. Farhad Esmaeilzadeh
