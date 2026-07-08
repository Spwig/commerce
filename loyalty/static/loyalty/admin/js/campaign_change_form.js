/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function init() {
        var journeyStepsField = document.getElementById('id_journey_steps');
        var actionsField = document.getElementById('id_actions');
        var triggerConditionsField = document.getElementById('id_trigger_conditions');
        var isJourneyCheckbox = document.getElementById('id_is_journey');

        if (typeof CampaignBuilder !== 'undefined') {
            new CampaignBuilder({
                journeyStepsField: journeyStepsField,
                actionsField: actionsField,
                triggerConditionsField: triggerConditionsField,
                isJourneyCheckbox: isJourneyCheckbox
            });
        }

        if (isJourneyCheckbox) {
            isJourneyCheckbox.addEventListener('change', toggleJourneyBuilder);
            toggleJourneyBuilder();
        }
    }

    function toggleJourneyBuilder() {
        var isJourneyCheckbox = document.getElementById('id_is_journey');
        var journeyContainer = document.getElementById('journey-builder-container');
        var actionContainer = document.getElementById('action-builder-container');

        if (!isJourneyCheckbox) { return; }

        if (isJourneyCheckbox.checked) {
            if (journeyContainer) { journeyContainer.style.display = 'block'; }
            if (actionContainer) { actionContainer.style.display = 'none'; }
        } else {
            if (journeyContainer) { journeyContainer.style.display = 'none'; }
            if (actionContainer) { actionContainer.style.display = 'block'; }
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
