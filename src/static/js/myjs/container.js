function updateFields(labels) {
    $('#new_fields_container').empty();

    labels.forEach(function(label) {
        var fieldHtml = `
            <div class="form-group">
                <label for="dop_id_${label.id}">${label.name}</label>
                <input type="text" name="${label.code}" id="dop_id_${label.id}" class="form-control w-md-50">
            </div>
        `;
        $('#new_fields_container').append(fieldHtml);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const formsetBody = document.getElementById("formset-body");
    const ndsInput = document.getElementById("id_vat_rate");
    const discountInpu = document.getElementById("id_discount");

    function calculateTotalSum() {
        let ndsRate = 0;
        if (ndsInput) {
            ndsRate = parseFloat(ndsInput.value) || 0;
        }
        let total = 0;
        let totalNds = 0;

        const amountInputs = document.querySelectorAll('.amount input');


        amountInputs.forEach(input => {
            if (input.value) {
                total += parseFloat(input.value) || 0;

                if (ndsRate > 0) {
                const nds = input.value * ndsRate / (100 + ndsRate);
                totalNds += nds;
            }
            }
        });


        if (document.getElementById('total-sum')) {
            document.getElementById('total-sum').textContent = total.toFixed(2);
        }
        if (document.getElementById('total-nds')) {
            document.getElementById('total-nds').textContent = totalNds.toFixed(2);
        }
    }

    function calculateRowSum(row) {
        const quantity = parseFloat(row.querySelector(".quantity input").value) || 0;
        const price = parseFloat(row.querySelector(".price input").value) || 0;
        const discountInput = row.querySelector(".discount input");
        //const discount = parseFloat(discountInpu.value) || 0;

        let discount = discountInpu.value;

        if (discount.endsWith('%')) { 
            discount = discount.slice(0, -1); 
            discount = parseFloat(discount) || 0
            discount = (discount / 100) * (quantity * price); 
        } else {
            discount = parseFloat(discount) || 0; 
        }

        let ndsValue = 0;
        if (ndsInput) {
            ndsValue = parseFloat(ndsInput.value) || 0;
        }

        const amount = quantity * price - discount;
        let nds;
        if (ndsValue == -1) {
            nds = 0;
        }
        else {
            nds = amount * ndsValue * 0.01;
        }

        const amountInput = row.querySelector(".amount input");
        if (amountInput) {
            amountInput.value = (amount + nds).toFixed(2);
        }
    }

    function recalculateAllRows() {
        document.querySelectorAll(".form-row").forEach(row => calculateRowSum(row));
    }

    formsetBody.addEventListener("input", function (event) {
        const input = event.target;
        const row = input.closest(".form-row");

        if (row && (input.matches(".quantity input") || input.matches(".price input") || input.matches(".discount input"))) {
            calculateRowSum(row);
            calculateTotalSum();
        }
    });

    if (ndsInput) {
        $(ndsInput).on('change', function() {
            recalculateAllRows();
        });
    }

    if (discountInpu) {
        $(discountInpu).on('change', function() {
            recalculateAllRows();
        });
    }

});


document.addEventListener("DOMContentLoaded", function () {
    const formsetBody = document.getElementById("formset-body");
    const duplicateLastRow = document.getElementById('duplicate-last-row');

    function updateRowNumbers() {
        document.querySelectorAll("#formset-body .row-number").forEach((cell, index) => {
            cell.textContent = index + 1;
        });
    }

    formsetBody.addEventListener("click", function (event) {
        if (event.target.closest(".add-row") || event.target.closest(".remove-row")) {
            setTimeout(updateRowNumbers, 100);
        }
    });

    duplicateLastRow.addEventListener("click", function (event) {
       setTimeout(updateRowNumbers, 100);
    });

    updateRowNumbers();
});


document.addEventListener('DOMContentLoaded', function () {
    ndsInput = document.getElementById("id_nds");

    calculateTotalSum();

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-row')) {
            var rowCount = document.querySelectorAll('#formset-body tr').length;
            if (rowCount > 1) {
                var row = event.target.closest('tr');
                row.remove();
                updateManagementForm();
            }
        }

        if (event.target.classList.contains('add-new-last-row')) {
            const lastRow = document.querySelector('#formset-body tr:last-child');
            const lastAddButton = lastRow.querySelector('.add-row');
            lastAddButton.click();
        }

        if (event.target.classList.contains('add-row')) {
            addNewRow(event.target);
        }
    });

    function calculateTotalSum() {
        let ndsRate = 0;

        if (ndsInput) {
            ndsRate = parseFloat(ndsInput.value) || 0;
        }

        let total = 0;
        let totalNds = 0;

        const amountInputs = document.querySelectorAll('.amount input');


        amountInputs.forEach(input => {
            if (input.value) {
                total += parseFloat(input.value) || 0;

                if (ndsRate > 0) {
                const nds = input.value * ndsRate / (100 + ndsRate);
                totalNds += nds;
            }
            }
        });

        if (document.getElementById('total-sum')) {
            document.getElementById('total-sum').textContent = total.toFixed(2);
        }
        if (document.getElementById('total-nds')) {
            document.getElementById('total-nds').textContent = totalNds.toFixed(2);
        }

    }

    function addNewRow(button) {
        var formsetBody = document.getElementById('formset-body');
        var firstRow = formsetBody.querySelector('tr');
        var newRow = firstRow.cloneNode(true);

        var currentRow = button.closest('tr');

        var inputs = newRow.querySelectorAll('input');
        inputs.forEach(function (input) {
            input.value = '';
        });

        var textareas = newRow.querySelectorAll('textarea');
        textareas.forEach(function (textarea) {
            textarea.value = '';
        });

        currentRow.insertAdjacentElement('afterend', newRow);
        updateManagementForm();
    }

    function updateManagementForm() {
        var totalForms = document.getElementById('id_form-TOTAL_FORMS');
        var formCount = document.querySelectorAll('#formset-body tr').length;
        totalForms.value = formCount;

        var rows = document.querySelectorAll('#formset-body tr');
        rows.forEach(function (row, index) {
            var inputs = row.querySelectorAll('input');
            inputs.forEach(function (input) {
                var name = input.name;
                if (name) {
                    var updatedName = name.replace(/-\d+-/, '-' + index + '-');
                    input.name = updatedName;
                }
            });

            var textareas = row.querySelectorAll('textarea');
            textareas.forEach(function (textarea) {
                var name = textarea.name;
                if (name) {
                    var updatedName = name.replace(/-\d+-/, '-' + index + '-');
                    textarea.name = updatedName;
                }
            });

            // Убедимся, что у каждой строки есть кнопка "Добавить строку"
            var addButton = row.querySelector('.add-row');
            if (!addButton) {
                var newAddButton = document.createElement('button');
                newAddButton.textContent = 'Добавить строку';
                newAddButton.classList.add('add-row');
                row.appendChild(newAddButton);
            }
        });

        const codeToUnitMap = {
    // Штучные единицы
    '796': 'шт',    // Штука
    '839': 'пар',   // Пара (2 шт)
    '778': 'упак',  // Упаковка

    // Весовые единицы
    '166': 'кг',    // Килограмм
    '168': 'т',     // Тонна
    '163': 'г',     // Грамм

    // Объемные единицы
    '112': 'л',     // Литр
    '137': 'м3',    // Кубический метр

    // Длина
    '006': 'м',     // Метр
    '039': 'км',    // Километр
    '041': 'мм',    // Миллиметр

    // Технические единицы
    '055': 'м2',    // Квадратный метр
    '111': 'см3',   // Кубический сантиметр

    // Тара
    '114': 'бут',   // Бутылка
    '116': 'банк',  // Банка
    '131': 'фл',    // Флакон

    // Для жидкостей
    '122': 'бал',   // Баллон
    '132': 'туб',   // Тюбик

    // Популярные в торговле
    '250': 'рул',   // Рулон
    '356': 'час',   // Час
    '366': 'сут',   // Сутки
    '536': 'компл', // Комплект
    '831': 'лист',  // Лист
    };

    document.querySelectorAll('.code_unit input').forEach(input => {
        const datalist = document.createElement('datalist');
        datalist.id = `datalist-${Math.random().toString(36).substr(2, 9)}`;

        Object.entries(codeToUnitMap).forEach(([code, unit]) => {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${code} - ${unit}`;
            datalist.appendChild(option);
        });

        document.body.appendChild(datalist);
        input.setAttribute('list', datalist.id);

        input.addEventListener('change', function() {
            const code = this.value;
            const unit = codeToUnitMap[code];

            if (unit) {
                const row = this.closest('tr');
                const unitInput = row.querySelector('.unit_of_measurement input');
                if (unitInput) {
                    unitInput.value = unit;
                }
            }
        });
    });

        setTimeout(calculateTotalSum, 100);
    }

    if (ndsInput) {
        $(ndsInput).on('change', function() {
           setTimeout(calculateTotalSum, 100);
        });
    }

    document.getElementById('duplicate-last-row')?.addEventListener('click', function() {
        duplicateLastRow();
    });

    function duplicateLastRow() {
        var formsetBody = document.getElementById('formset-body');
        var rows = formsetBody.querySelectorAll('tr');
        if (rows.length === 0) return;

        var lastRow = rows[rows.length - 1];
        var newRow = lastRow.cloneNode(true);

        var idInput = newRow.querySelector('input[name$="-id"]');
        if (idInput) idInput.value = '';

        var inputs = lastRow.querySelectorAll('input:not([name$="-id"])');
        var newInputs = newRow.querySelectorAll('input:not([name$="-id"])');

        inputs.forEach(function(input, index) {
            if (input.type !== 'button' && input.type !== 'submit' && !input.classList.contains('add-row') && !input.classList.contains('remove-row')) {
                newInputs[index].value = input.value;
            }
        });

        formsetBody.appendChild(newRow);

        updateManagementForm();
    }
});



document.addEventListener('DOMContentLoaded', function() {
    const codeToUnitMap = {
    // Штучные единицы
    '796': 'шт',    // Штука
    '839': 'пар',   // Пара (2 шт)
    '778': 'упак',  // Упаковка

    // Весовые единицы
    '166': 'кг',    // Килограмм
    '168': 'т',     // Тонна
    '163': 'г',     // Грамм

    // Объемные единицы
    '112': 'л',     // Литр
    '137': 'м3',    // Кубический метр

    // Длина
    '006': 'м',     // Метр
    '039': 'км',    // Километр
    '041': 'мм',    // Миллиметр

    // Технические единицы
    '055': 'м2',    // Квадратный метр
    '111': 'см3',   // Кубический сантиметр

    // Тара
    '114': 'бут',   // Бутылка
    '116': 'банк',  // Банка
    '131': 'фл',    // Флакон

    // Для жидкостей
    '122': 'бал',   // Баллон
    '132': 'туб',   // Тюбик

    // Популярные в торговле
    '250': 'рул',   // Рулон
    '356': 'час',   // Час
    '366': 'сут',   // Сутки
    '536': 'компл', // Комплект
    '831': 'лист',  // Лист
    };

    document.querySelectorAll('.code_unit input').forEach(input => {
        const datalist = document.createElement('datalist');
        datalist.id = `datalist-${Math.random().toString(36).substr(2, 9)}`;

        Object.entries(codeToUnitMap).forEach(([code, unit]) => {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${code} - ${unit}`;
            datalist.appendChild(option);
        });

        document.body.appendChild(datalist);
        input.setAttribute('list', datalist.id);

        input.addEventListener('change', function() {
            const code = this.value;
            const unit = codeToUnitMap[code];

            if (unit) {
                const row = this.closest('tr');
                const unitInput = row.querySelector('.unit_of_measurement input');
                if (unitInput) {
                    unitInput.value = unit;
                }
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {

    new Sortable(document.getElementById('formset-body'), {
        handle: '.drag-handle',
        animation: 150,
        ghostClass: 'bg-light',
        onEnd: function() {
            updateRowNumbers();
        }
    });

    function updateRowNumbers() {
        document.querySelectorAll("#formset-body .row-number").forEach((cell, index) => {
            cell.textContent = index + 1;
        });
    }
});