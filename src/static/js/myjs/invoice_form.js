document.getElementById("findByINN").addEventListener("click", function() {
    let innInput = document.getElementById("id_organization-inn");
    let inn = innInput.value.trim();

    if (!inn) {
        alert("Введите ИНН");
        return;
    }

    fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("id_organization-name").value = "";
            document.getElementById("id_organization-kpp").value = "";
            document.getElementById("id_organization-ogrn").value = "";
            document.getElementById("id_organization-address").value = "";
            document.getElementById("id_organization-director_position").value = "";
            document.getElementById("id_organization-director_name").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById("id_organization-name").value = data.name;
                    document.getElementById("id_organization-kpp").value = data.kpp;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("id_organization-director_position").value = data.position_at_work;
                    document.getElementById("id_organization-director_name").value = data.supervisor;
                    document.getElementById("id_organization-is_ip").checked = false;
                }
                else {
                    document.getElementById("id_organization-name").value = data.name;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("id_organization-is_ip").checked = true;
                }

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});



