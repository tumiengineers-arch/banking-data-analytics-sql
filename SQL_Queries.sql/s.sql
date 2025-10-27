-- 1. Customer & Account Insights
---
-- Q1. What is the average balance per account type?
SELECT Account_Type, AVG(Balance) AS Average_Balance FROM customer_accounts GROUP BY Account_Type;

-- Q2. How many customers have dormant accounts?
SELECT COUNT(*) AS Dormant_Count FROM customer_accounts WHERE Status = 'Dormant';

-- Q3. Which customers have the highest balances?
SELECT Name, Balance FROM customer_accounts ORDER BY Balance DESC LIMIT 5;

-- Q4. What is the distribution of account types across customers?
SELECT Account_Type, COUNT(*) AS Count, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_accounts), 2) AS Percentage FROM customer_accounts GROUP BY Account_Type;

-- Q5. Are there customers with multiple account types?
SELECT Customer_ID, COUNT(*) AS Account_Count FROM customer_accounts GROUP BY Customer_ID HAVING COUNT(*) > 1;

---
-- 2. Transaction Analysis
---
-- Q6. What is the total transaction volume per month?
SELECT strftime('%Y-%m', Date) AS Month, SUM(Amount) AS Total_Volume FROM transactions GROUP BY Month ORDER BY Month;

-- Q7. Which transaction type is most frequent?
SELECT Type, COUNT(*) AS Frequency FROM transactions GROUP BY Type ORDER BY Frequency DESC LIMIT 1;

-- Q8. What is the average transaction amount per type?
SELECT Type, AVG(Amount) AS Average_Amount FROM transactions GROUP BY Type;

-- Q9. Which customers have the highest transaction volumes?
SELECT T1.Name, SUM(T2.Amount) AS Total_Volume FROM customer_accounts T1 JOIN transactions T2 ON T1.Customer_ID = T2.Customer_ID GROUP BY T1.Name ORDER BY Total_Volume DESC LIMIT 5;

-- Q10. Are there seasonal trends in transaction activity?
SELECT strftime('%m', Date) AS Month_Num, SUM(Amount) AS Total_Volume FROM transactions GROUP BY Month_Num ORDER BY Month_Num;

---
-- 3. Loan Application Insights
---
-- Q11. What is the approval rate by loan type?
SELECT Loan_Type, ROUND(CAST(SUM(CASE WHEN Status = 'Approved' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*), 2) AS Approval_Rate FROM loan_applications GROUP BY Loan_Type ORDER BY Approval_Rate DESC;

-- Q12. What is the average loan amount per type?
SELECT Loan_Type, AVG(Amount) AS Average_Loan_Amount FROM loan_applications GROUP BY Loan_Type;

-- Q13. Which customers have multiple loan applications?
SELECT T1.Name, COUNT(T2.Loan_ID) AS Application_Count FROM customer_accounts T1 JOIN loan_applications T2 ON T1.Customer_ID = T2.Customer_ID GROUP BY T1.Name HAVING Application_Count > 1 ORDER BY Application_Count DESC;

-- Q14. What is the monthly trend in loan applications?
SELECT strftime('%Y-%m', Application_Date) AS Month, COUNT(Loan_ID) AS Application_Count FROM loan_applications GROUP BY Month ORDER BY Month;

-- Q15. What percentage of loans are still pending?
SELECT ROUND(100.0 * COUNT(CASE WHEN Status = 'Pending' THEN 1 END) / COUNT(*), 2) AS Pending_Percentage FROM loan_applications;

---
-- 4. Credit Card Usage
---
-- Q16. What is the total spend per category?
SELECT Category, SUM(Amount) AS Total_Spend FROM credit_card_usage GROUP BY Category ORDER BY Total_Spend DESC;

-- Q17. Which customers spend the most on credit cards?
SELECT T1.Name, SUM(T2.Amount) AS Total_Spend FROM customer_accounts T1 JOIN credit_card_usage T2 ON T1.Customer_ID = T2.Customer_ID GROUP BY T1.Name ORDER BY Total_Spend DESC LIMIT 5;

-- Q18. What is the average credit card transaction amount?
SELECT AVG(Amount) AS Average_Transaction_Amount FROM credit_card_usage;

-- Q19. Are there seasonal spikes in credit card usage?
SELECT strftime('%m', Date) AS Month_Num, SUM(Amount) AS Total_Spend FROM credit_card_usage GROUP BY Month_Num ORDER BY Total_Spend DESC;

-- Q20. Which categories show the highest growth?
WITH RankedData AS (
    SELECT
        Category,
        Amount,
        Date,
        CASE WHEN Date BETWEEN '2023-01-01' AND '2023-06-30' THEN 1 ELSE 0 END AS H1,
        CASE WHEN Date BETWEEN '2023-07-01' AND '2023-12-31' THEN 1 ELSE 0 END AS H2
    FROM credit_card_usage
)
SELECT
    Category,
    SUM(CASE WHEN H1 = 1 THEN Amount ELSE 0 END) AS H1_Spend,
    SUM(CASE WHEN H2 = 1 THEN Amount ELSE 0 END) AS H2_Spend,
    SUM(CASE WHEN H2 = 1 THEN Amount ELSE 0 END) - SUM(CASE WHEN H1 = 1 THEN Amount ELSE 0 END) AS Growth
FROM RankedData
GROUP BY Category
ORDER BY Growth DESC;

---
-- 5. Branch Performance
---
-- Q21. Which branch has the highest revenue-to-expense ratio?
SELECT Branch, ROUND(SUM(Revenue) * 1.0 / SUM(Expenses), 2) AS Revenue_to_Expense_Ratio FROM branch_performance GROUP BY Branch ORDER BY Revenue_to_Expense_Ratio DESC LIMIT 1;

-- Q22. What is the average customer count per branch?
SELECT Branch, ROUND(AVG(Customer_Count), 0) AS Average_Customer_Count FROM branch_performance GROUP BY Branch ORDER BY Average_Customer_Count DESC;

-- Q23. Which branch has the highest monthly revenue?
SELECT Branch, Month, Revenue FROM branch_performance ORDER BY Revenue DESC LIMIT 1;

-- Q24. Are there branches consistently overspending?
SELECT Branch, COUNT(*) AS Months_Overspending FROM branch_performance WHERE Expenses > Revenue GROUP BY Branch ORDER BY Months_Overspending DESC;

-- Q25. What is the trend in customer growth per branch?
WITH RankedData AS (
    SELECT
        Branch,
        Customer_Count,
        Month,
        ROW_NUMBER() OVER(PARTITION BY Branch ORDER BY Month ASC) AS rn_start,
        ROW_NUMBER() OVER(PARTITION BY Branch ORDER BY Month DESC) AS rn_end
    FROM branch_performance
)
SELECT
    s.Branch,
    s.Month AS Start_Month,
    s.Customer_Count AS Start_Count,
    e.Month AS End_Month,
    e.Customer_Count AS End_Count,
    e.Customer_Count - s.Customer_Count AS Growth
FROM RankedData s
JOIN RankedData e
    ON s.Branch = e.Branch
WHERE s.rn_start = 1 AND e.rn_end = 1;

---
-- 6. Fraud Detection
---
-- Q26. What is the total amount involved in confirmed fraud cases?
SELECT SUM(Amount) AS Total_Confirmed_Fraud_Amount FROM fraud_reports WHERE Status = 'Confirmed';

-- Q27. Which type of fraud is most common?
SELECT Type, COUNT(*) AS Frequency FROM fraud_reports GROUP BY Type ORDER BY Frequency DESC LIMIT 1;

-- Q28. Which customers are repeatedly flagged for fraud?
SELECT T1.Name, COUNT(T2.Report_ID) AS Fraud_Report_Count FROM customer_accounts T1 JOIN fraud_reports T2 ON T1.Customer_ID = T2.Customer_ID GROUP BY T1.Name HAVING Fraud_Report_Count > 1 ORDER BY Fraud_Report_Count DESC;

-- Q29. What is the resolution rate of fraud reports?
SELECT ROUND(CAST(SUM(CASE WHEN Status = 'Resolved' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*), 2) AS Resolution_Rate FROM fraud_reports;

-- Q30. Are there seasonal patterns in fraud reporting?
SELECT strftime('%m', Date) AS Month_Num, COUNT(*) AS Report_Count FROM fraud_reports GROUP BY Month_Num ORDER BY Report_Count DESC;

