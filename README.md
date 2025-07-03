# Kindle Courier

Daily digest of custom RSS feeds delivered to Kindle e-reader through email

## Local
### Prerequisits
* Python 3.12.10 (latest version supported by Azure Functions as of July 2025)
* Visual Studio Code Extensions/Tools
    * Python (version >= 2025.8.0)
    * Azure Functions (version >= 1.17.3)
    * Azurite V3 (version >= 3.34.0)
    * Azure Functions Core Tools
        * command:  
        ` > Azure Functions: Install or Update Core Tools`

### Setup
* Clone repository
* add local settings file `local.settings.json`. Sample:  
```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "EMAIL_CONNECTION_STRING": "endpoint=https://<your-functions-app-domain>.unitedstates.communication.azure.com/;accesskey=<base64-access-key>",
    "KINDLE_ACCOUNT_EMAIL": "yourkindleemailid@kindle.com"
  }
}
```

## Azure

* Create Azure Functions app
    * you can use azure functions tools in vs code:  
    `> Azure Functions: Create Function App in Azure`
* Create Azure Communication Service and Email Communication Service resources
* Set Functions app environment variables:     `EMAIL_CONNECTION_STRING` and `KINDLE_ACCOUNT_EMAIL`

* Deploy  
    `> Azure Functions: Deploy to Function App`

    
## Run

* **Locally**  
    `F5` to start debugging, then trigger the function from vs code "Azure" activity bar panel
* **In Azure**  (setup Azure Functions app and Communication/Email servers)
    vs code command: `> Functions:Execute Function Now... `