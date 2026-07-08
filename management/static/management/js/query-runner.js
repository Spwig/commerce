/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    "use strict";

    function displayResults(data) {
        var container = document.getElementById('results-container');
        var html = '<div class="results-header">Query Results</div>';
        html += '<table class="results-table"><thead><tr>';
        data.columns.forEach(function (col) { html += '<th>' + col + '</th>'; });
        html += '</tr></thead><tbody>';
        data.rows.forEach(function (row) {
            html += '<tr>';
            row.forEach(function (cell) {
                var cellValue = cell === null ? '<em>NULL</em>' : String(cell);
                html += '<td>' + cellValue + '</td>';
            });
            html += '</tr>';
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    }
    function clearQuery() {
        document.getElementById("query-input").value = "";
        document.getElementById("results-container").innerHTML = "";
        document.getElementById("query-meta").innerHTML = "";
    }

    function loadQuery(element) {
        document.getElementById("query-input").value = element.getAttribute("data-query");
    }

    document.addEventListener("click", function (e) {
        var el = e.target.closest("[data-action]");
        if (!el) return;
        switch (el.dataset.action) {
            case "execute-query": executeQuery(); break;
            case "clear-query": clearQuery(); break;
            case "load-query": loadQuery(el); break;
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        var queryInput = document.getElementById("query-input");
        if (queryInput) {
            queryInput.addEventListener("keydown", function (e) {
                if (e.ctrlKey && e.key === "Enter") { executeQuery(); }
            });
        }
    });
})();
