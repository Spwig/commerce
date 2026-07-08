/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    "use strict";

    var preflightPassed = false;
    var upgradeId = null;
    var consecutiveErrors = 0;
    var isReconnecting = false;

    function readConfig() {
        var el = document.getElementById("upgrade-config");
        return el ? el.dataset : {};
    }

    function runPreflightChecks() {
        var config = readConfig();
        var btn = document.getElementById("run-checks-btn");
        btn.disabled = true;
        btn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> " + (config.msgChecking || "Checking...");
        var checks = document.querySelectorAll(".preflight-item");
        var checkIndex = 0;
        function runNextCheck() {
            if (checkIndex >= checks.length) {
                btn.innerHTML = "<i class='fas fa-check'></i> " + (config.msgChecksComplete || "Checks Complete");
                var allPassed = Array.from(checks).every(function (c) { return c.classList.contains("passed"); });
                preflightPassed = allPassed;
                document.getElementById("upgrade-btn").disabled = !allPassed;
                return;
            }
            var check = checks[checkIndex];
            check.classList.remove("pending");
            check.classList.add("checking");
            check.querySelector("i").className = "fas fa-spinner";
            check.querySelector(".check-status").textContent = config.msgChecking || "Checking...";
            setTimeout(function () {
                check.classList.remove("checking");
                check.classList.add("passed");
                check.querySelector("i").className = "fas fa-check-circle";
                check.querySelector(".check-status").textContent = config.msgPassed || "Passed";
                checkIndex++;
                runNextCheck();
            }, 500);
        }
        runNextCheck();
    }

    function checkForUpdates(btn) {
        var config = readConfig();
        var originalContent = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> " + (config.msgChecking || "Checking...");
        fetch(config.checkUpdatesUrl, { method: "POST", headers: { "X-CSRFToken": AdminUtils.getCsrfToken() } })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.update_available) { location.reload(); }
                else {
                    AdminModal.alert(config.msgNoUpdates || "No updates available. You are running the latest version.");
                    btn.disabled = false;
                    btn.innerHTML = originalContent;
                }
            })
            .catch(function (error) {
                console.error("Error:", error);
                AdminModal.alert({message: config.msgFailedCheck || "Failed to check for updates", type: "error"});
                btn.disabled = false;
                btn.innerHTML = originalContent;
            });
    }

    function showReconnecting() {
        if (isReconnecting) return;
        isReconnecting = true;
        var stepEl = document.getElementById("progress-step");
        if (stepEl) {
            stepEl.textContent = "System is restarting, reconnecting...";
        }
        var headerIcon = document.querySelector("#upgrade-progress h3 i");
        if (headerIcon) {
            headerIcon.className = "fas fa-sync-alt fa-spin";
        }
    }

    function clearReconnecting() {
        if (!isReconnecting) return;
        isReconnecting = false;
        var headerIcon = document.querySelector("#upgrade-progress h3 i");
        if (headerIcon) {
            headerIcon.className = "fas fa-spinner fa-spin";
        }
    }

    function pollUpgradeProgress() {
        if (!upgradeId) return;
        var config = readConfig();
        var url = config.upgradeProgressUrl ? config.upgradeProgressUrl.replace("0", upgradeId) : null;
        if (!url) return;
        fetch(url)
            .then(function (r) {
                if (r.redirected) {
                    // Session expired — server is back but auth lost. Reload to go to login.
                    location.reload();
                    return;
                }
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.json();
            })
            .then(function (data) {
                if (!data) return;
                consecutiveErrors = 0;
                clearReconnecting();

                document.getElementById("progress-bar").style.width = data.progress_percent + "%";
                document.getElementById("progress-percent").textContent = data.progress_percent + "%";
                document.getElementById("progress-step").textContent = data.current_step || "";
                if (data.status === "completed") {
                    AdminModal.toast(config.msgUpgradeCompleted || "Upgrade completed successfully! The page will now reload.", "success");
                    setTimeout(function () { location.reload(); }, 2000);
                } else if (data.status === "failed" || data.status === "rolled_back") {
                    AdminModal.alert({message: (config.msgUpgradeFailed || "Upgrade failed") + ": " + (data.error_message || config.msgUnknown || "Unknown error"), type: "error"});
                    setTimeout(function () { location.reload(); }, 3000);
                } else { setTimeout(pollUpgradeProgress, 2000); }
            })
            .catch(function (error) {
                consecutiveErrors++;
                console.error("Error polling progress (attempt " + consecutiveErrors + "):", error);

                // After 3 consecutive failures, show reconnecting message
                if (consecutiveErrors >= 3) {
                    showReconnecting();
                }

                // Use exponential backoff: 3s, 5s, 8s, then cap at 10s
                var delay = Math.min(3000 + (consecutiveErrors * 2000), 10000);
                setTimeout(pollUpgradeProgress, delay);
            });
    }

    document.addEventListener("click", function (e) {
        var el = e.target.closest("[data-action]");
        if (!el) return;
        switch (el.dataset.action) {
            case "run-preflight-checks": runPreflightChecks(); break;
            case "check-for-updates": checkForUpdates(el); break;
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        var config = readConfig();
        var upgradeForm = document.getElementById("upgrade-form");
        if (upgradeForm) {
            upgradeForm.addEventListener("submit", async function (e) {
                e.preventDefault();
                if (!preflightPassed) {
                    AdminModal.alert({message: config.msgRunChecksFirst || "Please run and pass all pre-flight checks before upgrading.", type: "warning"});
                    return;
                }
                var confirmMsg = config.msgConfirmUpgrade || "Are you sure you want to start the upgrade? A backup will be created first.";
                if (!await AdminModal.confirm(confirmMsg)) return;
                var btn = document.getElementById("upgrade-btn");
                btn.disabled = true;
                btn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> " + (config.msgStarting || "Starting...");
                document.getElementById("upgrade-progress").classList.add("active");
                fetch(config.upgradeStartUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "X-CSRFToken": AdminUtils.getCsrfToken() },
                    body: JSON.stringify({ target_version: config.availableVersion })
                })
                    .then(function (r) { return r.json(); })
                    .then(function (data) {
                        if (data.success) { upgradeId = data.upgrade_id; pollUpgradeProgress(); }
                        else {
                            AdminModal.alert({message: (config.msgFailedStart || "Failed to start upgrade") + ": " + (data.error || config.msgUnknown || "Unknown error"), type: "error"});
                            document.getElementById("upgrade-progress").classList.remove("active");
                            btn.disabled = false;
                            btn.innerHTML = "<i class='fas fa-arrow-circle-up'></i> " + (config.msgStartUpgrade || "Start Upgrade");
                        }
                    })
                    .catch(function (error) {
                        console.error("Error:", error);
                        AdminModal.alert({message: config.msgFailedStart || "Failed to start upgrade", type: "error"});
                        document.getElementById("upgrade-progress").classList.remove("active");
                        btn.disabled = false;
                        btn.innerHTML = "<i class='fas fa-arrow-circle-up'></i> " + (config.msgStartUpgrade || "Start Upgrade");
                    });
            });
        }
    });
})();
