CREATE TABLE customers (
    customerID VARCHAR(50),
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(50),
    MonthlyCharges NUMERIC,
    TotalCharges NUMERIC,
    Churn VARCHAR(5)
);

copy customers
FROM 'C:/Users/Public/churndata.csv'
DELIMITER ','
CSV HEADER;

select count(*) FROM customers;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'customers'
ORDER BY ordinal_position;

-- Finding the Overall Churn Rate, then grouping by Tenure 

select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate

from customers

-- churn rate by tenure (binned)
	
select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate
, case 
	when tenure < 20 then 'Tenure 0-20'
	when tenure < 40 then 'Tenure 20-40'
	when tenure < 60 then 'Tenure 40-60'
	else 'Tenure 60+'
	end as tenure_group_in_weeks

from customers

group by tenure_group_in_weeks

order by overall_churn_rate desc

-- Churn rate by monthly charges

select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate
, case 
	when monthlycharges < 25 then 'monthly charges 0-25'
	when monthlycharges < 50 then 'monthly charges 25-50'
	when monthlycharges < 75 then 'monthly charges 50-75'
	when monthlycharges < 100 then 'monthly charges 75-100'
	else 'monthlycharges 100+'
	end as monthly_charges

from customers

group by monthly_charges

order by overall_churn_rate desc

-- churn rate by payment method

select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate
, paymentmethod

from customers

group by paymentmethod

order by overall_churn_rate desc

--churn rate by contract and payment method

select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate
, contract
, paymentmethod

from customers

group by contract
, paymentmethod

order by overall_churn_rate desc

-- churn rate by tenure (unbinned)
	
select count(customerid) as total_customers
, count(churn) filter (where churn = 'Yes') as total_churned
, round(100.0 * count(churn) filter (where churn = 'Yes') / count(customerid), 2) as overall_churn_rate
, tenure

from customers

where tenure <> 0

group by tenure

order by tenure asc


