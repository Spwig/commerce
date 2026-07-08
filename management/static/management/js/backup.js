/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    "use strict";

    var backupId = null;

    function readConfig() {
        var el = document.getElementById("backup-config");
        return el ? el.dataset : {};
    }

    function pollBackupProgress() {
        if (!backupId) return;
        var config = readConfig();
        var url = config.progressUrl ? config.progressUrl.replace("0", backupId) : null;
        if (!url) return;
        fetch(url)
            .then(function (r) { return r.json(); })
            .then(function (data) {
                document.getElementById("progress-bar").style.width = data.progress_percent + "%";
                document.getElementById("progress-percent").textContent = data.progress_percent + "%";
                document.getElementById("progress-step").textContent = data.current_step || "";
                if (data.status === "completed") {
                    AdminModal.toast(config.msgCompleted || "Backup completed successfully!", "success");
                    window.location.href = config.dashboardUrl || "/";
                } else if (data.status === "failed") {
                    AdminModal.alert({message: (config.msgFailed || "Backup failed") + ": " + (data.error_message || config.msgUnknown || "Unknown error"), type: "error"});
                    window.location.href = config.dashboardUrl || "/";
                } else { setTimeout(pollBackupProgress, 2000); }
            })
            .catch(function (error) {
                console.error("Error polling progress:", error);
                setTimeout(pollBackupProgress, 5000);
            });
    }

    document.addEventListener("click", function (e) {
        var cardEl = e.target.closest(".backup-type-card");
        if (cardEl) {
            document.querySelectorAll(".backup-type-card").forEach(function (c) { c.classList.remove("selected"); });
            cardEl.classList.add("selected");
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        var config = readConfig();

        var backupForm = document.getElementById("backup-form");
        if (backupForm) {
            backupForm.addEventListener("submit", function (e) {
                e.preventDefault();
                var btn = document.getElementById("backup-btn");
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (config.msgStarting || "Starting...");
                document.getElementById("backup-progress").classList.add("active");
                var formData = new FormData(this);
                fetch(config.backupUrl, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": AdminUtils.getCsrfToken(),
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: formData
                })
                    .then(function (r) { return r.json(); })
                    .then(function (data) {
                        if (data.success) { backupId = data.backup_id; pollBackupProgress(); }
                        else {
                            AdminModal.alert({message: (config.msgFailedStart || "Failed to start backup") + ": " + (data.error || config.msgUnknown || "Unknown error"), type: "error"});
                            document.getElementById("backup-progress").classList.remove("active");
                            btn.disabled = false;
                            btn.innerHTML = '<i class="fas fa-save"></i> ' + (config.msgStartBackup || "Start Backup");
                        }
                    })
                    .catch(function (error) {
                        console.error("Error:", error);
                        AdminModal.alert({message: config.msgFailedStart || "Failed to start backup", type: "error"});
                        document.getElementById("backup-progress").classList.remove("active");
                        btn.disabled = false;
                        btn.innerHTML = '<i class="fas fa-save"></i> ' + (config.msgStartBackup || "Start Backup");
                    });
            });
        }
    });
})();
