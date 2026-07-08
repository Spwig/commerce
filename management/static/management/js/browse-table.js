/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    "use strict";

    function exportTable() {
        var table = document.getElementById("dataTable");
        if (!table) return;
        var csv = "";
        var headers = Array.from(table.querySelectorAll("thead th")).map(function (th) { return th.textContent; });
        csv += headers.join(",") + "\n";
        var rows = table.querySelectorAll("tbody tr");
        rows.forEach(function (row) {
            var cells = Array.from(row.querySelectorAll("td")).map(function (td) {
                var text = td.textContent.trim();
                if (text === "NULL") text = "";
                if (text.indexOf(",") !== -1 || text.indexOf('"') !== -1) {
                    text = '"' + text.replace(/"/g, '""') + '"';
                }
                return text;
            });
            csv += cells.join(",") + "\n";
        });
        var blob = new Blob([csv], { type: "text/csv" });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        var configEl = document.getElementById("browse-table-config");
        var tableName = configEl ? configEl.dataset.tableName : "table";
        var page = configEl ? configEl.dataset.page : "1";
        a.download = tableName + "_page_" + page + ".csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    document.addEventListener("click", function (e) {
        var el = e.target.closest("[data-action]");
        if (!el) return;
        if (el.dataset.action === "export-table") { exportTable(); }
    });

    document.addEventListener("keydown", function (e) {
        var configEl = document.getElementById("browse-table-config");
        if (!configEl) return;
        var hasPrevious = configEl.dataset.hasPrevious === "true";
        var hasNext = configEl.dataset.hasNext === "true";
        var previousPage = configEl.dataset.previousPage;
        var nextPage = configEl.dataset.nextPage;
        if (e.key === "ArrowLeft" && e.ctrlKey && hasPrevious) {
            window.location.href = "?page=" + previousPage;
        }
        if (e.key === "ArrowRight" && e.ctrlKey && hasNext) {
            window.location.href = "?page=" + nextPage;
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        var cells = document.querySelectorAll(".data-table td");
        cells.forEach(function (cell) {
            if (cell.scrollWidth > cell.clientWidth) { cell.title = cell.textContent; }
        });
    });
})();
