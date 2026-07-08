/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    "use strict";

    function filterTables() {
        var searchTerm = document.getElementById("tableSearch").value.toLowerCase();
        var tableCards = document.querySelectorAll(".table-card");
        tableCards.forEach(function (card) {
            var tableName = card.getAttribute("data-table-name");
            if (tableName) {
                card.classList.toggle("mgmt-hidden", !tableName.includes(searchTerm));
            }
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        var tableSearchEl = document.getElementById("tableSearch");
        if (tableSearchEl) {
            tableSearchEl.addEventListener("keyup", filterTables);
        }
        var tableCount = document.querySelector(".table-count");
        if (tableCount) {
            var count = 0;
            var target = parseInt(tableCount.textContent, 10);
            var increment = Math.ceil(target / 20);
            var timer = setInterval(function () {
                count += increment;
                if (count >= target) { count = target; clearInterval(timer); }
                tableCount.textContent = count;
            }, 50);
        }
    });
})();
