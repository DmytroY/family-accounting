# Family Accounting System Guide

## Overview
This document provides instructions and guidelines for using the Family Accounting system, a simple and free application designed to help users track income and expenses across family accounts.

## Introduction
The system offers basic, essential functionality without unnecessary complexity. It allows users to manage shared family finances through a centralized dashboard.

## Registration and Account Setup
* **Family Grouping:** Financial records are structured around family units. Data stored within a family profile is accessible to all assigned members of that specific family.
* **Initial User:** The first family member registers independently and can subsequently create accounts for additional family members.
* **Email Verification:** Users must enter a valid email address during registration. The email is required to receive access restoration links in case of password loss.

## Recording Income and Expenses

To begin tracking transactions, follow this setup sequence:

1. **Create Currencies:** Define the currencies used for tracking transactions.
2. **Create Accounts:** 
   * Assign a currency to each account.
   * Accounts using different currencies can share the same name (e.g., "My cash (USD)" and "My cash (EUR)").
3. **Define Categories:**
   * Categories specify the type of transaction (e.g., "Salary", "Food", "Transfer between accounts").
   * Configure category usage by selecting the appropriate checkboxes:
     * **Use it for income**
     * **Use it for expense**
     * **Use for both** (e.g., for transfers)
4. **Create Financial Transactions:**
   * Once an account, currency, and category exist, new income or expense transactions can be added.
   * **Transfers Between Accounts:** Transfers require two transactions of equal amounts:
     * Example: Withdrawing cash from an ATM requires one expense transaction on the "Card" account and one income transaction on the "Cash" account.
   * **Transaction Signs:** Income is recorded as a positive value and expenses as a negative value. Sign assignment is handled automatically by the system based on the selected transaction type (income or expense).

## Data Import and Export (CSV)
* Users can import and export data using CSV files available on the relevant system pages.
* **Automatic Creation:** Importing transactions automatically creates missing currencies, accounts, and categories. Manual pre-creation of these items prior to import is not required.
* **Post-Import Maintenance:**
  * Adjust and set the correct starting balances for automatically created accounts.
  * Review created categories and uncheck "use for income" or "use for expense" as needed to refine transaction input options.

## Disclaimers and Operational Notes
* **Non-Commercial Product:** The system is provided free of charge for personal use.
* **Liability & Availability:** The developer does not guarantee permanent data storage, system stability, or continuous uptime.
* **Data Backups:** Regular data backups via CSV file export are strongly recommended to prevent potential data loss.

## Contact and Source Code
* **Source Code Repository:** https://github.com/DmytroY/family-accounting
* **Feedback & Support:** Suggestions and inquiries can be sent to [dmitry.yakovenko@gmail.com](mailto:dmitry.yakovenko@gmail.com).