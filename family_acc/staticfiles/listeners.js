document.addEventListener("DOMContentLoaded", function () {

        const currencyField = document.getElementById("id_currency");
        const accountField = document.getElementById("id_account");
        const currencyInfo = document.getElementById("currency-info");
        
        function loadAccountByCurrency() {
            const currencyId = currencyField.value;
            accountField.innerHTML = "<option value=''>------------</option>";
            currencyInfo.textContent = "";
            accountField.disabled = true;

            if(!currencyId) return;

            fetch(`/transactions/ajax/account-by-currency/?currency=${currencyId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(acc => {
                        accountField.innerHTML +=
                            `<option value="${acc.id}">${acc.name}</option>`;
                    });
                    accountField.disabled = false;
                });
        }
            
        function updateCurrencyInfo(){
            const accountId = accountField.value;
            if (!accountId) return;

            fetch(`/transactions/ajax/account/${accountId}/currency/`)
                .then(response => response.json())
                .then(data => {
                    currencyInfo.textContent =  data.currency;
                });
        }

        currencyField?.addEventListener("change", loadAccountByCurrency);
        accountField.addEventListener("change", updateCurrencyInfo);

        // Initial update (for edit forms)
        // loadAccountByCurrency();
    });