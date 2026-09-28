--Create Audit Table in SQL Server

Create database AICLCRAgent 

CREATE TABLE Contract_Review_Audit1
(
    Review_ID INT IDENTITY(1,1) PRIMARY KEY,
    Review_Timestamp DATETIME2,
    Review_Question NVARCHAR(MAX),
    Agent_Decision_Status NVARCHAR(50),
    Agent_Recommended_Next_Step NVARCHAR(100),
    Reviewer NVARCHAR(255),
    Reviewer_Decision NVARCHAR(100),
    Workflow_Action NVARCHAR(100),
    Workflow_Status NVARCHAR(100),
    Contract_Evidence NVARCHAR(MAX),
    Policy_Evidence NVARCHAR(MAX),
    Agent_Review NVARCHAR(MAX)
);

----Verify the table 
SELECT *
FROM Contract_Review_Audit1;

EXEC sp_help 'Contract_Review_Audit1';

--Verify 
SELECT *
FROM Contract_Review_Audit;

----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------
    USE AICLCRAgent;
GO

SELECT 
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Contract_Review_Audit'
ORDER BY ORDINAL_POSITION;

USE AICLCRAgent;
GO

SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    COLUMNPROPERTY(
        OBJECT_ID('Contract_Review_Audit'),
        COLUMN_NAME,
        'IsIdentity'
    ) AS IsIdentity
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Contract_Review_Audit'
ORDER BY ORDINAL_POSITION;

SELECT TOP 10 *
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;

SELECT TOP 10 *
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;

SELECT TOP 5
    Review_ID,
    Review_Timestamp,
    Agent_Decision_Status,
    Agent_Recommended_Next_Step,
    Reviewer_Decision,
    Workflow_Action,
    Workflow_Status
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;

SELECT TOP 5
    Review_ID,
    Review_Timestamp,
    Agent_Decision_Status,
    Agent_Recommended_Next_Step,
    Reviewer_Decision,
    Workflow_Action,
    Workflow_Status
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;

SELECT TOP 5 *
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;

SELECT TOP 1 *
FROM Contract_Review_Audit
ORDER BY Review_ID DESC;