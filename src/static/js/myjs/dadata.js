function innSearch(btn, element_id, prefix){
document.getElementById(btn).addEventListener("click", function() {
    let innInput = document.getElementById(element_id);
    console.log(innInput)
    let inn = innInput.value.trim();
    console.log(inn)

    fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById(prefix + "-name").value = "";
            document.getElementById(prefix + "-kpp").value = "";
            document.getElementById(prefix + "-ogrn").value = "";
            document.getElementById(prefix + "-address").value = "";
            document.getElementById(prefix + "-director_position").value = "";
            document.getElementById(prefix + "-director_name").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById(prefix + "-name").value = data.name;
                    document.getElementById(prefix + "-kpp").value = data.kpp;
                    document.getElementById(prefix + "-ogrn").value = data.ogrn;
                    document.getElementById(prefix + "-address").value = data.address;
                    document.getElementById(prefix + "-director_position").value = data.position_at_work;
                    document.getElementById(prefix + "-director_name").value = data.supervisor;
                    document.getElementById(prefix + "-is_ip").checked = false;
                    //const type_selection = document.getElementById("type_selection");
                    //if (type_selection) {
                    //    document.getElementById("type_selection").value = "ogrn";
                    //}
                }
                else {
                    document.getElementById(prefix + "-name").value = data.name;
                    document.getElementById(prefix + "-ogrn").value = data.ogrn;
                    document.getElementById(prefix + "-address").value = data.address;
                    document.getElementById(prefix + "-is_ip").checked = true;
                    //const type_selection = document.getElementById("type_selection");
                   // if (type_selection) {
                    //    document.getElementById("type_selection").value = "ogrnip";
                    //}
                }

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});
}

innSearch("findByINN","id_seller-inn", "id_seller")
innSearch("BuyerfindByINN","id_buyer-inn", "id_buyer")
innSearch("ConsigneefindByINN","id_consignee-inn", "id_consignee")

function bikSearch(btn, element_id, prefix){
document.addEventListener("DOMContentLoaded", function () {
    let findByBIKButton = document.getElementById(btn);

    if (findByBIKButton) {
        findByBIKButton.addEventListener("click", function () {
            let bikInput = document.getElementById(element_id);
            if (!bikInput) return;

            let bik = bikInput.value.trim();
            if (!bik) {
                alert("Введите БИК");
                return;
            }

            fetch(`/find-bank/?bik=${bik}`)
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

bikSearch("findByBIKBank", "id_organization_bank-bik","id_organization_bank")
bikSearch("findByBIKBankCoun", "id_buyer_bank-bik","id_buyer_bank")

