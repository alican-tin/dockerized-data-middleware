# **Dockerized Data Middleware**

## **Overview**

This project is a microservices-based data middleware simulation developed for the CENG302 Data Middleware course. The architecture consists of two isolated Docker containers communicating via a HTTP/REST API: a **Producer** that generates mock financial logs and a **Middleware** that processes, sanitizes, and routes these logs to appropriate storage formats based on predefined business rules.

## **Core Features**

* **Fail-Fast Performance Filter:** System resources are optimized by immediately ignoring low-priority logs (INFO and WARNING levels) at the initial entry point, preventing unnecessary CPU cycles.  
* **GDPR/KVKK Compliant Data Masking:** Personally Identifiable Information (PII) such as Credit Card numbers, National ID numbers (TCKN), and Email addresses are automatically sanitized using Regex-based masking rules.  
* **Data Enrichment:** Raw logs are augmented with internal metadata, including processing timestamps (ISO 8601\) and server identification tags.  
* **Role-Based Routing:** Processed data is dynamically formatted and exported to specific files based on department needs: HTML for System Administrators, CSV for Cyber Security, and JSON for Web Developers.  
* **Configurable Stress Testing:** The system includes a built-in stress testing mode to evaluate the performance filter under high-throughput conditions.

## **Architectural Design Patterns**

The system architecture adheres strictly to SOLID principles and implements three primary design patterns:

1. **Factory Method (producer/factory.py):** Centralizes the instantiation of various log types (Transaction, SystemError, Access), ensuring the client code remains decoupled from the specific log generation logic.  
2. **Chain of Responsibility (middleware/chain.py):** Establishes a sequential processing pipeline (Performance Filter \-\> Security Masking \-\> Enrichment). Each handler has a single responsibility and can break the chain early (Fail-Fast) if necessary.  
3. **Strategy Pattern (middleware/strategies.py):** Enables dynamic selection of the output formatting algorithm (HTMLStrategy, CSVStrategy, JSONStrategy) at runtime based on the enriched log's type attribute, fully satisfying the Open/Closed Principle.

## **Prerequisites and Installation**

* Docker Engine  
* Docker Compose

### **Quick Start**

1. Clone the repository:  
   git clone \[https://github.com/alican-tin/dockerized-data-middleware.git\](https://github.com/alican-tin/dockerized-data-middleware.git)  
   cd dockerized-data-middleware

2. Build and start the containers:  
   docker compose up \--build

3. Verify the output:  
   Once the containers are running, processed logs will be automatically written to the output\_logs directory in the project root:  
   * sysadmin\_logs.html  
   * cybersec\_logs.csv  
   * webdev\_logs.json

## **Stress Testing Configuration**

To evaluate the system under high load, modify the STRESS\_MODE environment variable within the docker-compose.yml file:

    environment:  
      \- MIDDLEWARE\_URL=http://middleware:5000/api/logs  
      \- STRESS\_MODE=True  
      \- LOG\_COUNT=1000

After saving the changes, restart the containers. The Producer will bypass sleep intervals and execute a rapid transmission of the specified log count.

## **Repository Structure**

.  
├── docker-compose.yml  
├── middleware/  
│   ├── Dockerfile  
│   ├── chain.py  
│   ├── main.py  
│   ├── regex\_utils.py  
│   ├── requirements.txt  
│   └── strategies.py  
└── producer/  
    ├── Dockerfile  
    ├── factory.py  
    ├── main.py  
    └── requirements.txt  
