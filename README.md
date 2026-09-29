# 🏦 Bank Branch Performance Analytics

A data analytics and NLP-based system for analyzing bank branch performance, customer satisfaction, financial KPIs, and customer feedback.

## 📌 Project Overview

This project analyzes branch-level banking data to help management understand:

- Branch financial performance
- Customer growth and satisfaction
- Loans and deposits
- Complaints
- Employee productivity
- Customer feedback sentiment
- Overall branch performance

The project combines **Python Data Analytics, NLP, Streamlit, and FastAPI** into one end-to-end system.

## 🎯 Objectives

- Measure branch performance using key banking KPIs
- Compare performance across branches
- Analyze customer satisfaction and complaints
- Analyze customer feedback using NLP sentiment analysis
- Provide an interactive dashboard
- Expose analytics through REST APIs

## 🛠️ Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- TextBlob
- Streamlit
- FastAPI
- Uvicorn
- Jupyter Notebook
- Git & GitHub

## 📊 Key KPIs

The system calculates:

- Profit
- Profit Margin
- Loan-to-Deposit Ratio
- Complaint Rate
- Revenue per Employee
- Customers per Employee
- Customer Satisfaction
- Negative Feedback Rate
- Branch Performance Score

## 🤖 NLP Analysis

Customer feedback is analyzed using NLP-based sentiment analysis.

Example:

> "The waiting time was too long."

The system identifies the sentiment and calculates its polarity score.

Supported sentiment categories:

- Positive
- Negative
- Neutral

## 📈 Dashboard

The Streamlit dashboard provides:

- Overall branch KPIs
- Branch-wise financial analysis
- Profit comparison
- Profit margin comparison
- Loans vs deposits
- Customer satisfaction
- Complaint analysis
- Customer feedback sentiment
- Regional revenue analysis
- Branch performance score
- Detailed branch performance table

## 🔌 FastAPI

The project also provides REST API endpoints for accessing analytics.

### Available endpoints

```text
GET  /
GET  /branches
GET  /branches/{branch_id}
GET  /analytics/overview
POST /feedback/analyze