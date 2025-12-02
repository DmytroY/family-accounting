document.addEventListener("DOMContentLoaded", function () {

        const accountField = document.getElementById("id_account");
        const currencyInfo = document.getElementById("currency-info");

        function updateCurrency() {
            const accountId = accountField.value;
            if (!accountId) return;

            fetch(`/transactions/ajax/account/${accountId}/currency/`)
                .then(response => response.json())
                .then(data => {
                    currencyInfo.textContent =  data.currency;
                });
        }

        accountField.addEventListener("change", updateCurrency);

        // Initial update (for edit forms)
        updateCurrency();
    });