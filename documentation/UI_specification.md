# Family Accounting Application - UI Functionality Documentation

This document describes the user interface functionality of every page in the Family Accounting Django web application. API functionality has been excluded from this document.

---

## Overview

The Family Accounting application is a Django-based financial management system with a multi-user, multi-family architecture. The UI is organized into two main sections:

1. **Authentication & User Management** (Members app)
2. **Financial Transactions & Accounting** (Transactions app)

The application supports multi-language internationalization (English, Czech, Ukrainian) and requires user authentication for all core functionality.

---

## Authentication & Registration Pages

### 1. **Login Page** (`/accounts/login/`)
- **Purpose:** User authentication entry point
- **URL:** Controlled by Django's built-in auth system and custom redirect
- **Template:** `members/templates/registration/login.html`
- **Elements:**
  - Username and password form fields
  - "Submit" button
  - "Reset password" link for password recovery
  - "Next" URL parameter handling for post-login redirection (defaults to transaction list)
- **Functionality:**
  - Authenticates user credentials
  - Redirects authenticated users to the transaction list page
  - Provides password reset option for forgotten credentials
  - Form validation using Django's AuthenticationForm

---

### 2. **Registration Page** (`/members/register/`)
- **Purpose:** New user account creation with family group assignment
- **URL:** `/members/register/`
- **Template:** `members/templates/register.html`
- **Elements:**
  - Registration form (dynamically generated)
  - "Save" button
- **Functionality:**
  - Collects new user credentials
  - Assigns user to a family group (identified by a family token)
  - Creates a UserProfile linked to the family
  - Automatically logs in the new user
  - Redirects to family members list after successful registration

---

### 3. **Password Reset Request Page** (`/accounts/password_reset/`)
- **Purpose:** Initiate password recovery workflow
- **URL:** Django's built-in auth view
- **Template:** `registration/password_reset_form.html`
- **Elements:**
  - Email address input field
  - "Send reset link" button
- **Functionality:**
  - Accepts email address for registered account
  - Validates email exists in system
  - Sends password reset link via email (Gmail SMTP configured)
  - Displays success confirmation

---

### 4. **Password Reset Confirmation Page** (`/accounts/password_reset_confirm/`)
- **Purpose:** Complete password reset with new password entry
- **URL:** Django's built-in auth view with reset token
- **Template:** Django default (not customized in this app)
- **Elements:**
  - New password input field
  - Password confirmation input field
  - Submit button
- **Functionality:**
  - Validates reset token from email link
  - Allows user to set a new password
  - Redirects to password change complete page on success

---

### 5. **Password Reset Complete Page** (`/accounts/password_reset_complete/`)
- **Purpose:** Confirmation that password has been successfully reset
- **URL:** Django's built-in auth view
- **Template:** `registration/password_reset_complete.html`
- **Elements:**
  - Confirmation message: "Password changed"
  - "Login" link to return to login page
- **Functionality:**
  - Confirms successful password reset
  - Provides navigation back to login page

---

### 6. **Password Change Page** (`/accounts/password_change/`)
- **Purpose:** Allow authenticated user to change their current password
- **URL:** Django's built-in auth view
- **Template:** Django default (not customized in this app)
- **Elements:**
  - Old password input field
  - New password input field
  - Password confirmation input field
  - Submit button
- **Functionality:**
  - Requires current password for security
  - Validates new password against Django's password validators
  - Updates user password in database
  - Accessible via link on member edit page

---

## Family Members Management Pages

### 7. **Family Members List Page** (`/members/`)
- **Purpose:** Display all users in the same family group
- **URL:** `/members/`
- **Template:** `members/templates/all_members.html`
- **Elements:**
  - Table with columns: Username, First Name, Last Name, Email
  - Username links to member detail/edit page
- **Functionality:**
  - Lists all users with matching family field
  - Filters members by current user's family group
  - Clicking username navigates to member edit page
  - Default redirect after login

---

### 8. **Member Edit Page** (`/members/<uuid:uuid>/`)
- **Purpose:** View and edit individual family member details
- **URL:** `/members/<uuid>/` (using UserProfile UUID)
- **Template:** `members/templates/member_edit.html`
- **Elements:**
  - First Name input field (editable)
  - Last Name input field (editable)
  - Email input field (editable)
  - "Save" button
  - "Delete" button
  - "Change password" link (visible only for current user's own profile)
- **Functionality:**
  - Displays user profile information
  - Allows editing of first name, last name, and email
  - Updates user details in database on save
  - Deletes user account (with protection against deletion if used in transactions)
  - Accessible only to members within the same family
  - Returns 404 error for access to members outside user's family
  - Shows error if deletion fails due to transaction dependencies

---

### 9. **Member Create Page** (`/members/member_create/`)
- **Purpose:** Create a new family member within an existing family
- **URL:** `/members/member_create/`
- **Template:** `members/templates/register.html` (same form as registration)
- **Elements:**
  - Registration form
  - "Save" button
- **Functionality:**
  - Creates new user associated with current user's family
  - Pre-populates family token from current user's profile
  - Automatically logs in newly created user
  - Redirects to family members list after creation

---

## Transactions Management Pages

### 10. **Transactions List Page** (`/transactions/` or `/transactions/transaction_list`)
- **Purpose:** View all financial transactions with filtering and batch operations
- **URL:** `/transactions/`, `/transactions/transaction_list`
- **Template:** `transactions/templates/transaction_list.html`
- **Elements:**
  - Date range filter inputs (From/To dates with type="date")
  - "Filter" button to apply date range
  - "Download CSV" link (includes current date filter)
  - Report period display showing applied date range
  - Transaction table with columns:
    - Checkbox (for batch selection)
    - Date (clickable to edit)
    - Account
    - Amount
    - Currency
    - Category
  - "Select All" checkbox to select/deselect all rows
  - "Delete selected" button with confirmation dialog
- **Functionality:**
  - Displays transactions for current user's family
  - Defaults to current month if no date range specified
  - Filters transactions by date range via GET parameters (start, end)
  - Highlights income transactions in green, expenses in red (via CSS classes)
  - Allows batch deletion with confirmation
  - Exports filtered transactions to CSV format (Date, Account, Amount, Currency, Category, Remark)
  - Row colors differentiate income (positive amount) from expenses (negative amount)
  - Individual transaction editing accessible via date link

---

### 11. **Create Income Transaction Page** (`/transactions/transaction_create/income`)
- **Purpose:** Record a new income transaction
- **URL:** `/transactions/transaction_create/income`
- **Template:** `transactions/templates/transaction_create_income.html`
- **Elements:**
  - Date input field (default: today)
  - Currency dropdown (filtered by available currencies)
  - Account dropdown (filtered by currency selection)
  - "Add account" link for quick account creation
  - Amount input field with currency info display
  - Category dropdown (filtered to income-only categories)
  - "Add category" link for quick category creation
  - Remark text field (optional)
  - "Save" button
  - Link to "Upload by CSV" for bulk import
- **Functionality:**
  - Creates transaction with positive amount (income sign convention)
  - Updates account balance by adding the transaction amount
  - Restricts to categories marked as usable for income
  - Currency dropdown dynamically populates account dropdown
  - Quick-add links for account and category creation without page navigation
  - Validates amount field with error display
  - Form-level validation prevents submission with missing required fields

---

### 12. **Create Expense Transaction Page** (`/transactions/transaction_create/expense`)
- **Purpose:** Record a new expense transaction
- **URL:** `/transactions/transaction_create/expense`
- **Template:** `transactions/templates/transaction_create_expense.html`
- **Elements:**
  - Date input field (default: today)
  - Currency dropdown
  - Account dropdown (filtered by currency)
  - "Add account" link
  - Amount input field with currency info display
  - Category dropdown (filtered to expense-only categories)
  - "Add category" link
  - Remark text field (optional)
  - "Save" button
  - Link to "Upload by CSV"
- **Functionality:**
  - Creates transaction with negative amount (expense sign convention)
  - Updates account balance by subtracting the transaction amount
  - Restricts to categories marked as usable for expenses
  - Currency-aware account filtering via AJAX
  - Validates amount field
  - Identical form layout to income page for consistency

---

### 13. **Edit Transaction Page** (`/transactions/transaction_edit/<id>`)
- **Purpose:** Modify existing transaction details or delete transaction
- **URL:** `/transactions/transaction_edit/<id>`
- **Template:** `transactions/templates/transaction_edit.html`
- **Elements:**
  - Date field (pre-filled)
  - Currency field (pre-filled)
  - Account field (pre-filled)
  - Amount field (pre-filled, currency info displayed)
  - Category field (pre-filled)
  - Remark field (pre-filled)
  - "Save" button
  - "Delete" button
  - "Cancel" button
- **Functionality:**
  - Loads existing transaction details
  - Automatically determines transaction type (income/expense) based on amount sign
  - Updates transaction on save
  - Adjusts account balances if amount or account changed
  - Reverts account balance from old transaction amount before applying new amount
  - Deletes transaction with account balance adjustment
  - Cancel button returns to transaction list without saving

---

### 14. **Upload Transactions Page** (`/transactions/transaction_upload`)
- **Purpose:** Bulk import transactions from CSV file
- **URL:** `/transactions/transaction_upload`
- **Template:** `transactions/templates/transaction_upload.html`
- **Elements:**
  - File input field for CSV upload
  - "Upload CSV" button
  - Example CSV format displayed with columns:
    - date (YYYY-MM-DD format)
    - account_name
    - amount (positive for income, negative for expenses)
    - currency_code
    - category_name
    - remark
  - Example data rows shown for reference
- **Functionality:**
  - Accepts multipart/form-data CSV file upload
  - Parses CSV and creates Transaction records
  - Maps account names and categories to database IDs
  - Updates account balances for each imported transaction
  - Displays success or error messages after import

---

## Accounts Management Pages

### 15. **Accounts List Page** (`/transactions/account_list`)
- **Purpose:** View all financial accounts with filtering and sorting
- **URL:** `/transactions/account_list`
- **Template:** `transactions/templates/account_list.html`
- **Elements:**
  - Currency filter dropdown (with "All" option)
  - "Filter" button
  - Sortable table with columns:
    - Account (sortable, clickable to edit)
    - Balance (sortable)
    - Currency (sortable)
- **Functionality:**
  - Lists all accounts for current user's family
  - Filters by currency via GET parameter
  - Sorts by account name, balance, or currency code
  - Account names are clickable links to edit page
  - Displays current balance for each account
  - Persists sort parameter when filtering by currency

---

### 16. **Create Account Page** (`/transactions/account_create`)
- **Purpose:** Add a new financial account
- **URL:** `/transactions/account_create`
- **Template:** `transactions/templates/account_create.html`
- **Elements:**
  - Account name input field
  - Initial balance input field (numerical)
  - Currency dropdown
  - "Save" button
  - Link to "Upload by CSV" for bulk import
- **Functionality:**
  - Creates new Account record
  - Associates with current user's family
  - Sets initial balance (defaults to 0 if not specified)
  - Requires currency selection
  - Links to currency_create for quick currency addition
  - Form validation prevents blank account names

---

### 17. **Edit Account Page** (`/transactions/account_edit/<id>`)
- **Purpose:** Modify account details or delete account
- **URL:** `/transactions/account_edit/<id>`
- **Template:** `transactions/templates/account_edit.html`
- **Elements:**
  - Account name field (pre-filled, editable)
  - Balance field (pre-filled, editable)
  - Currency field (pre-filled, editable)
  - "Save" button
  - "Delete" button
  - "Cancel" button
- **Functionality:**
  - Loads existing account data
  - Updates account name, balance, and currency
  - Deletes account (with protection against deletion if used in transactions)
  - Shows error message if deletion fails due to transaction dependencies
  - Cancel returns to account list

---

### 18. **Upload Accounts Page** (`/transactions/account_upload`)
- **Purpose:** Bulk import accounts from CSV file
- **URL:** `/transactions/account_upload`
- **Template:** `transactions/templates/account_upload.html`
- **Elements:**
  - File input field for CSV upload
  - "Upload CSV" button
  - Example CSV format with columns:
    - name
    - balance
    - currency_code
    - currency_description
  - Example data rows for reference
- **Functionality:**
  - Accepts multipart/form-data CSV file upload
  - Parses CSV and creates Account records
  - Creates Currency records if not already present
  - Associates accounts with current user's family

---

## Currency Management Pages

### 19. **Currencies List Page** (`/transactions/currency_list`)
- **Purpose:** View all available currencies
- **URL:** `/transactions/currency_list`
- **Template:** `transactions/templates/currency_list.html`
- **Elements:**
  - Table with columns:
    - Code (clickable to edit)
    - Description
- **Functionality:**
  - Lists all Currency records for current user's family
  - Currency codes are clickable links to edit page
  - Read-only view (no inline editing)

---

### 20. **Create Currency Page** (`/transactions/currency_create`)
- **Purpose:** Add a new currency to the system
- **URL:** `/transactions/currency_create`
- **Template:** `transactions/templates/currency_create.html`
- **Elements:**
  - Currency code input field (e.g., USD, EUR)
  - Currency description input field
  - "Save" button
  - Link to "Upload by CSV" (note: links to category_upload, likely a bug)
- **Functionality:**
  - Creates new Currency record
  - Associates with current user's family
  - Code typically 3-letter currency code
  - Description provides human-readable name

---

### 21. **Edit Currency Page** (`/transactions/currency_edit/<id>`)
- **Purpose:** Modify currency details or delete currency
- **URL:** `/transactions/currency_edit/<id>`
- **Template:** `transactions/templates/currency_edit.html`
- **Elements:**
  - Currency code field (pre-filled, editable)
  - Currency description field (pre-filled, editable)
  - "Save" button
  - "Delete" button
  - "Cancel" button
- **Functionality:**
  - Loads existing currency data
  - Updates currency code and description
  - Deletes currency (with protection against deletion if used in accounts)
  - Shows error if deletion fails due to account dependencies
  - Cancel returns to currency list

---

## Category Management Pages

### 22. **Categories List Page** (`/transactions/category_list`)
- **Purpose:** View all income and expense categories
- **URL:** `/transactions/category_list`
- **Template:** `transactions/templates/category_list.html`
- **Elements:**
  - Table with columns:
    - Name (clickable to edit)
    - Use for income? (boolean display)
    - Use for expense? (boolean display)
- **Functionality:**
  - Lists all Category records for current user's family
  - Category names are clickable links to edit page
  - Shows which categories are designated for income use
  - Shows which categories are designated for expense use
  - Categories can be configured for both income and expense (e.g., transfers)

---

### 23. **Create Category Page** (`/transactions/category_create`)
- **Purpose:** Add a new transaction category
- **URL:** `/transactions/category_create`
- **Template:** `transactions/templates/category_create.html`
- **Elements:**
  - Category name input field
  - "Use it for income?" checkbox
  - "Use it for expense?" checkbox
  - "Save" button
  - Link to "Upload by CSV"
- **Functionality:**
  - Creates new Category record
  - Associates with current user's family
  - Allows marking category for income transactions
  - Allows marking category for expense transactions
  - A category can serve both purposes (e.g., "Transfers between accounts")
  - At least one flag must be selected for meaningful use

---

### 24. **Edit Category Page** (`/transactions/category_edit/<id>`)
- **Purpose:** Modify category details or delete category
- **URL:** `/transactions/category_edit/<id>`
- **Template:** `transactions/templates/category_edit.html`
- **Elements:**
  - Category name field (pre-filled, editable)
  - "Use it for income?" checkbox (pre-filled)
  - "Use it for expense?" checkbox (pre-filled)
  - "Save" button
  - "Delete" button
  - "Cancel" button
- **Functionality:**
  - Loads existing category data
  - Updates category name and usage flags
  - Deletes category (with protection against deletion if used in transactions)
  - Shows error if deletion fails due to transaction dependencies
  - Cancel returns to category list

---

### 25. **Upload Categories Page** (`/transactions/category_upload`)
- **Purpose:** Bulk import categories from CSV file
- **URL:** `/transactions/category_upload`
- **Template:** Not visible in search results (likely uses standard form similar to other upload pages)
- **Elements:**
  - File input field for CSV upload
  - "Upload CSV" button
- **Functionality:**
  - Accepts multipart/form-data CSV file upload
  - Parses CSV and creates Category records
  - Associates categories with current user's family

---

## Global Layout & Navigation

### 26. **Layout Template** (`layout.html`)
- **Purpose:** Base template for all application pages
- **Template:** `family_acc/templates/layout.html`
- **Global Elements:**
  - **Header Section:**
    - Logout form (if authenticated) showing "You authorized as [username]" with logout link
    - User profile link (username clickable)
    - Login/Registration links (if not authenticated)
    - Language selector dropdown (English, Czech, Ukrainian)
  - **Navigation Menu (Collapsible):**
    - **TRANSACTIONS** section:
      - Transaction List
      - New Expense
      - New Income
    - **CURRENCY** section:
      - List
      - New
    - **ACCOUNTS** section:
      - List
      - New
    - **CATEGORIES** section:
      - (Navigation likely continues below, truncated in template view)
  - **Content Block:** Dynamic block for page-specific content
  - **CSS & JavaScript:**
    - `global.css` - Global styling
    - `ai_chat.css` - AI chat styling
    - `listeners.js` - Event listeners

- **Functionality:**
  - Provides consistent navigation across all pages
  - User authentication state display
  - Multi-language support with dropdown selector
  - Collapsible menu sections for organization
  - Grid-based layout with header, menu, and content areas

---

## Error Pages

### 27. **404 Not Found Page** (`404.html`)
- **Purpose:** Display when requested resource does not exist
- **Template:** `family_acc/templates/404.html`
- **Elements:**
  - Heading: "404"
  - Message: "Hm...Looks like there is nothing to see..."
- **Functionality:**
  - Extends base layout template
  - Provides user-friendly error message

---

## Additional Pages (Mentioned in Routes)

### 28. **Home/Main Page** (`/`)
- **Purpose:** Landing page for the application
- **URL:** `/`
- **Template:** `main.html`
- **Functionality:** Not visible in detail, likely serves as entry point or dashboard

---

### 29. **AI Chat Page** (`/ai/chat/`)
- **Purpose:** AI-powered financial advisor/assistant chat
- **URL:** `/ai/chat/`
- **Functionality:** Loads `ai_chat.css` and associated JavaScript, uses Groq AI library for responses
- **Note:** AI functionality is not detailed in this UI document (integration with Groq API backend)

---

## Data Relationships & Sign Conventions

### Transaction Amount Sign Convention
- **Income transactions:** Positive amounts (e.g., +5000)
- **Expense transactions:** Negative amounts (e.g., -50.12)
- This allows unified reporting and filtering by amount sign

### Account Balance Updates
- **On income creation:** `balance += amount` (positive)
- **On expense creation:** `balance -= |amount|` (subtracts absolute value)
- **On deletion:** Reverses the original transaction's impact

---

## Multi-Language Support

All UI pages support translation with Django's i18n framework:
- **Languages Supported:** English, Czech, Ukrainian
- **Implementation:** Using `{% trans %}` and `{% blocktrans %}` template tags
- **Language Selector:** Available in header for switching languages
- **Fallback:** English is the default language

---

## Summary Table of Pages

| Page | URL | Template | Purpose |
|------|-----|----------|---------|
| Login | `/accounts/login/` | `registration/login.html` | User authentication |
| Registration | `/members/register/` | `members/templates/register.html` | New user signup |
| Password Reset | `/accounts/password_reset/` | `registration/password_reset_form.html` | Password recovery initiation |
| Password Reset Confirm | `/accounts/password_reset_confirm/` | Django default | Password change via token |
| Password Reset Complete | `/accounts/password_reset_complete/` | `registration/password_reset_complete.html` | Password reset confirmation |
| Family Members List | `/members/` | `members/templates/all_members.html` | View family members |
| Member Edit | `/members/<uuid>/` | `members/templates/member_edit.html` | Edit member details |
| Member Create | `/members/member_create/` | `members/templates/register.html` | Create new family member |
| Transactions List | `/transactions/` | `transactions/templates/transaction_list.html` | View all transactions |
| Create Income | `/transactions/transaction_create/income` | `transactions/templates/transaction_create_income.html` | Add income transaction |
| Create Expense | `/transactions/transaction_create/expense` | `transactions/templates/transaction_create_expense.html` | Add expense transaction |
| Edit Transaction | `/transactions/transaction_edit/<id>` | `transactions/templates/transaction_edit.html` | Modify transaction |
| Upload Transactions | `/transactions/transaction_upload` | `transactions/templates/transaction_upload.html` | Bulk import transactions |
| Accounts List | `/transactions/account_list` | `transactions/templates/account_list.html` | View accounts |
| Create Account | `/transactions/account_create` | `transactions/templates/account_create.html` | Add new account |
| Edit Account | `/transactions/account_edit/<id>` | `transactions/templates/account_edit.html` | Modify account |
| Upload Accounts | `/transactions/account_upload` | `transactions/templates/account_upload.html` | Bulk import accounts |
| Currencies List | `/transactions/currency_list` | `transactions/templates/currency_list.html` | View currencies |
| Create Currency | `/transactions/currency_create` | `transactions/templates/currency_create.html` | Add new currency |
| Edit Currency | `/transactions/currency_edit/<id>` | `transactions/templates/currency_edit.html` | Modify currency |
| Categories List | `/transactions/category_list` | `transactions/templates/category_list.html` | View categories |
| Create Category | `/transactions/category_create` | `transactions/templates/category_create.html` | Add new category |
| Edit Category | `/transactions/category_edit/<id>` | `transactions/templates/category_edit.html` | Modify category |
| Upload Categories | `/transactions/category_upload` | (Dynamic) | Bulk import categories |
| 404 Error | (Any invalid URL) | `404.html` | Not found error |

---

This comprehensive UI documentation describes all user-facing pages and their functionality, excluding API endpoints. The application is organized around family-based financial management with multi-currency support, transaction categorization, and account management capabilities.
