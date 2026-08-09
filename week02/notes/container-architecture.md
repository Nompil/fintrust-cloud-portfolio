# FinTrust Container Architecture Notes

Containers made more sense to me once I stopped thinking of them as just another deployment tool and started seeing them as a way to package an application with everything it needs to run. That is the real value. The same image can be used in development, testing, and production without rebuilding the environment every time.

## Why containers are useful

The main problem they solve is the classic one: something works on a developer machine but fails on a server. Containers reduce that gap because the runtime, libraries, and configuration travel with the application.

For FinTrust, that matters because the platform is meant to grow and evolve. A container-based design makes it easier to deploy services consistently and scale them independently.

## Containers vs EC2 vs Lambda

### EC2

EC2 is still useful when I need a more traditional server model. It gives me full control over the environment, but it also means more operational overhead.

### Containers on ECS

Containers are a better fit for services such as the transaction API and account service because they are portable, fast to start, and easier to manage than a fleet of virtual machines.

### Lambda

Lambda is still the better choice for short event-driven tasks. The difference is that Lambda is not designed to run long-lived services the way containers are.

## Docker terms I want to keep straight

- Image: a blueprint for the application and its dependencies
- Container: a running instance of that image
- Registry: the place where images are stored, such as Amazon ECR

This became easier to understand once I thought of an image as the recipe and the container as the actual thing running from that recipe.

## ECS, EKS, and Fargate

For FinTrust, ECS is the more practical starting point. It is AWS-native, simpler to operate, and well suited to a new application architecture.

EKS is more relevant when a team already uses Kubernetes or needs a broader multi-cloud approach. It is more flexible, but it is also more complex.

Fargate is useful because it removes the need to manage the underlying hosts. That makes it a strong fit for the FinTrust API services that need to scale without the extra burden of operating EC2 infrastructure.

## My takeaway

The container story for FinTrust is really about consistency and flexibility. Containers help keep services portable, ECS gives a managed way to run them, and Fargate removes the server-management overhead from the equation.
