# Invelytics‑AaaS 🚀

_A lightweight, AI‑powered inventory analytics service deployed on AWS_

## Overview 🌟

Invelytics‑AaaS is deployed on AWS Fargate using Amazon ECS, providing a scalable, serverless container environment for processing inventory updates. It leverages Amazon Cognito for secure user authentication and authorization, enabling clients to log in and access the service through a managed user pool. Amazon API Gateway serves as the public endpoint for both manual and webhook‑driven inventory updates, routing requests to Fargate tasks and ensuring fine‑grained access control.

## Architecture 🏗️

### AWS Fargate & ECS 🐳

Containers are orchestrated on AWS Fargate, eliminating the need to manage servers or clusters while providing on‑demand compute scaling based on task requirements. Docker images are stored in Amazon ECR and automatically pulled by ECS services during deployment.

### Authentication & Authorization 🔐

User authentication is handled by Amazon Cognito User Pools, which securely manage sign‑up, sign‑in, and multi‑factor authentication flows. Access tokens issued by Cognito are validated by API Gateway to protect downstream compute resources.

### API Gateway 🛠️

Amazon API Gateway exposes RESTful and WebSocket APIs that integrate privately with Fargate tasks via VPC Link or Lambda proxy integrations. Webhooks from client systems trigger inventory update endpoints, enabling real‑time data ingestion.

### Scheduled Insights & Reporting ⏰

Amazon EventBridge Scheduler (formerly CloudWatch Events) initiates daily ECS tasks that process accumulated inventory data and generate insights. This decouples real‑time ingestion from batch analytics for performance and cost optimization.

### PDF Generation & Delivery 📄

Insight reports are rendered into professional PDFs using the ReportLab library in Python, supporting charts and tabular data for clear visualization. Completed PDFs are sent as email attachments via Amazon SES, following MIME standards for attachments.

## Features ✨

- **Scalable, serverless compute** on AWS Fargate (ECS) 🚀  
- **Secure user authentication** with Amazon Cognito 🔐  
- **API Gateway** for REST and webhook endpoints 🌐  
- **Real‑time webhook ingestion** for inventory updates ⚡  
- **Daily scheduled analytics** via EventBridge Scheduler ⏲️  
- **PDF report generation** using ReportLab 📑  
- **Automated email delivery** with Amazon SES 📧  
