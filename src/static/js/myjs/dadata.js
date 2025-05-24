function bicSearch(btn, element_id, prefix){
document.addEventListener("DOMContentLoaded", function () {
    let findBybicButton = document.getElementById(btn);

    if (findBybicButton) {
        findBybicButton.addEventListener("click", function () {
            let bicInput = document.getElementById(element_id);
            if (!bicInput) return;

            let bic = bicInput.value.trim();
            if (!bic) {
                alert("Введите БИК");
                return;
            }

            fetch(`/find-bank/?bic=${bic}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let bankName = document.getElementById(prefix + "-name");
                        let bankLocation = document.getElementById(prefix + "-address");
                        let correspondentAccount = document.getElementById(prefix + "-correspondent_account");

                        if (bankName) bankName.value = data.bank_name;
                        if (bankLocation) bankLocation.value = data.address;
                        if (correspondentAccount) correspondentAccount.value = data.correspondent_account;
                    } else {
                        alert("Банк не найден");
                    }
                })
                .catch(error => console.error("Ошибка при запросе данных:", error));
        });
    }
});
}

bicSearch("findBybicBank", "id_organization_bank-bic","id_organization_bank")
bicSearch("findBybicBankCoun", "id_buyer_bank-bic","id_buyer_bank")

