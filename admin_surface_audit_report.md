# Admin Surface Audit — Assessment

_Capabilities declared in `admin.py` but missing from the rendered admin UI._

- **Scanned:** 281 ModelAdmins
- **Gaps (high/medium):** 119
- **Method:** static template analysis + rendered-DOM checks, as an existing superuser. Actions-bar findings are decided from the template source (robust to empty tables). Field/inline findings compare the ModelAdmin's declared form fields/inlines against the rendered HTML.
- **Re-run:** `./manage.py audit_admin_surfaces [--app X] [--json] [--fail-on-gaps]`

## Priority 1 — Admin pages that crash (500)

| Model | URL | Error |
|---|---|---|
| `cart.shippingmethod` | /en/admin/cart/shippingmethod/  (add or change form) | change form crashes (HTTP 500) |
| `pos_app.receipttemplate` | /en/admin/pos_app/receipttemplate/  (add or change form) | change form crashes (HTTP 500) |
| `referrals.referralattribution` | /en/admin/referrals/referralattribution/ | changelist crashes (HTTP 500) |

## Priority 2 — Registered domain actions with no UI (29)

These changelists override the default template and drop the Django actions bar, so the listed bulk actions are unreachable. **Fix type** tells you which pattern each is.

| Model | Changelist URL | Fix type | Template | Unreachable domain actions |
|---|---|---|---|---|
| `accounts.communicationpreference` | /en/admin/accounts/communicationpreference/ | no bulk UI at all | `admin/accounts/communicationpreference/change_list.html` | bulk_verify_email, bulk_unsubscribe_marketing, export_preferences_csv, export_preferences_json |
| `affiliate.affiliate` | /en/admin/affiliate/affiliate/ | no bulk UI at all | `admin/affiliate/affiliate/change_list.html` | approve_affiliates, suspend_affiliates, activate_affiliates |
| `affiliate.affiliateprogrammembership` | /en/admin/affiliate/affiliateprogrammembership/ | no bulk UI at all | `admin/affiliate/affiliateprogrammembership/change_list.html` | approve_memberships, reject_memberships |
| `affiliate.program` | /en/admin/affiliate/program/ | no bulk UI at all | `admin/affiliate/program/change_list.html` | activate_programs, pause_programs, archive_programs |
| `blog.blogpost` | /en/admin/blog/blogpost/ | custom bar (missing Django actions) | `admin/blog/blogpost/change_list.html` | make_published, make_draft, make_featured, remove_featured |
| `blog.socialconnectoraccount` | /en/admin/blog/socialconnectoraccount/ | no bulk UI at all | `admin/blog/socialconnectoraccount/change_list.html` | refresh_tokens, disconnect_accounts |
| `catalog.booking` | /en/admin/catalog/booking/ | calendar UI | `admin/catalog/booking/change_list.html` | mark_confirmed, mark_completed, mark_no_show, mark_cancelled |
| `catalog.product` | /en/admin/catalog/product/ | custom bar (missing Django actions) | `admin/catalog/product/change_list.html` | mark_international_ready, export_customs_data, restore_selected_products |
| `email_system.emailaccount` | /en/admin/email_system/emailaccount/ | custom bar (missing Django actions) | `email_system/admin/emailaccount_changelist.html` | regenerate_dkim_keys |
| `email_system.emailoutbox` | /en/admin/email_system/emailoutbox/ | no bulk UI at all | `admin/email_system/emailoutbox/change_list.html` | release_held_emails_action |
| `geoip.businessrule` | /en/admin/geoip/businessrule/ | no bulk UI at all | `admin/geoip/businessrule/change_list.html` | test_rule, reset_statistics |
| `geoip.geoipprovider` | /en/admin/geoip/geoipprovider/ | checkboxes present, no form/bar | `admin/geoip/geoipprovider/change_list.html` | update_database, test_provider |
| `loyalty.loyaltycampaign` | /en/admin/loyalty/loyaltycampaign/ | no bulk UI at all | `admin/loyalty/loyaltycampaign/change_list.html` | activate_campaigns, pause_campaigns |
| `loyalty.loyaltymember` | /en/admin/loyalty/loyaltymember/ | no bulk UI at all | `admin/loyalty/loyaltymember/change_list.html` | activate_members, deactivate_members, export_to_csv |
| `loyalty.loyaltyredemption` | /en/admin/loyalty/loyaltyredemption/ | no bulk UI at all | `admin/loyalty/loyaltyredemption/change_list.html` | mark_fulfilled, cancel_redemptions |
| `loyalty.loyaltyreward` | /en/admin/loyalty/loyaltyreward/ | no bulk UI at all | `admin/loyalty/loyaltyreward/change_list.html` | activate_rewards, deactivate_rewards, feature_rewards, unfeature_rewards |
| `loyalty.loyaltyrule` | /en/admin/loyalty/loyaltyrule/ | no bulk UI at all | `admin/loyalty/loyaltyrule/change_list.html` | activate_rules, deactivate_rules, duplicate_rules |
| `loyalty.loyaltysegment` | /en/admin/loyalty/loyaltysegment/ | no bulk UI at all | `admin/loyalty/loyaltysegment/change_list.html` | refresh_memberships |
| `media_library.imagesizepreset` | /en/admin/media_library/imagesizepreset/ | no bulk UI at all | `admin/media_library/imagesizepreset/change_list.html` | regenerate_thumbnails |
| `orders.order` | /en/admin/orders/order/ | no bulk UI at all | `admin/orders/order/change_list.html` | mark_as_processing, mark_as_shipped, mark_as_delivered, mark_as_cancelled, mark_as_paid, mark_as_unpaid, mark_payment_pending, generate_licenses_now, generate_packing_slips, generate_commercial_invoices, generate_customs_forms |
| `orders.returnrequest` | /en/admin/orders/returnrequest/ | no bulk UI at all | `admin/orders/returnrequest/change_list.html` | approve_returns, reject_returns, mark_label_sent, mark_received, cancel_returns |
| `pos_app.posterminal` | /en/admin/pos_app/posterminal/ | no bulk UI at all | `admin/pos_app/posterminal/change_list.html` | regenerate_pairing_codes, remote_unlock_terminals |
| `pos_app.posterminalprovider` | /en/admin/pos_app/posterminalprovider/ | no bulk UI at all | `admin/pos_app/posterminalprovider/change_list.html` | test_provider_connection |
| `pos_app.posterminalreader` | /en/admin/pos_app/posterminalreader/ | no bulk UI at all | `admin/pos_app/posterminalreader/change_list.html` | regenerate_splash_screen |
| `referrals.referralattribution` | /en/admin/referrals/referralattribution/ | no bulk UI at all | `admin/referrals/referralattribution/change_list.html` | approve_attributions, reject_attributions |
| `referrals.referralreward` | /en/admin/referrals/referralreward/ | no bulk UI at all | `admin/referrals/referralreward/change_list.html` | issue_rewards, revoke_rewards |
| `shipping.shipment` | /en/admin/shipping/shipment/ | no bulk UI at all | `admin/shipping/shipment/change_list.html` | purchase_labels, generate_packing_slips, generate_commercial_invoices, generate_customs_forms |
| `vouchers.vouchercode` | /en/admin/vouchers/vouchercode/ | no bulk UI at all | `admin/vouchers/vouchercode/change_list.html` | activate_vouchers, deactivate_vouchers, export_vouchers, export_vouchers_xlsx, clone_vouchers |
| `webhooks.webhookendpoint` | /en/admin/webhooks/webhookendpoint/ | no bulk UI at all | `admin/webhooks/webhookendpoint/change_list.html` | enable_endpoints, disable_endpoints, reset_failures_action |

## Field candidates — declared form field not rendered (33)

_Lower confidence: a few may be conditionally-rendered-by-type tabs rather than true omissions. Verify per field._

| Model | Field | Change-form template |
|---|---|---|
| `catalog.product` | `tags` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `is_preorder` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `preorder_release_date` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `preorder_message` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `preferred_shipping_package` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `page_template` | `admin/catalog/product/change_form.html` |
| `catalog.product` | `requires_shipping` | `admin/catalog/product/change_form.html` |
| `core.sitesettings` | `supported_currencies` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `translations` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `community_merchant_id` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `community_client_secret` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `community_registered_at` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `staff_2fa_enforcement_date` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `enable_double_opt_in` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `default_marketing_opt_in` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `preference_center_enabled` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `require_sms_verification` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `show_unsubscribe_reasons` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `low_stock_alert_frequency` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `allow_backorders_by_default` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `default_reorder_lead_days` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `safety_stock_multiplier` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `velocity_calculation_window_days` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `tax_id` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `invoice_footer_text` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `packing_slip_footer_text` | `admin/core/sitesettings/change_form.html` |
| `core.sitesettings` | `document_logo_width` | `admin/core/sitesettings/change_form.html` |
| `pos_app.storegroup` | `settings` | `admin/pos_app/storegroup/change_form.html` |
| `staff_roles.staffrole` | `is_predefined` | `admin/staff_roles/staffrole/change_form.html` |
| `subscriptions.customersubscription` | `billing_cycle_count` | `admin/subscriptions/customersubscription/change_form.html` |
| `subscriptions.customersubscription` | `last_billing_date` | `admin/subscriptions/customersubscription/change_form.html` |
| `subscriptions.customersubscription` | `last_billing_status` | `admin/subscriptions/customersubscription/change_form.html` |
| `vouchers.vouchercode` | `attribution_campaign` | `admin/vouchers/vouchercode/change_form.html` |

## Inline candidates — declared inline not rendered (10)

| Model | Inline (prefix) |
|---|---|
| `affiliate.affiliate` | Link (prefix=links) |
| `affiliate.affiliate` | Commission (prefix=commissions) |
| `affiliate.program` | AffiliateProgramMembership (prefix=affiliateprogrammembership_set) |
| `catalog.productattribute` | AttributeValue (prefix=values) |
| `loyalty.loyaltymember` | LoyaltyBalance (prefix=balance) |
| `loyalty.loyaltymember` | LoyaltyMemberBadge (prefix=badges_earned) |
| `subscriptions.customersubscription` | BillingCycleLog (prefix=billing_logs) |
| `subscriptions.customersubscription` | CustomerSubscriptionAddon (prefix=active_addons) |
| `vouchers.vouchercode` | VoucherRestriction (prefix=restrictions) |
| `vouchers.vouchercode` | VoucherUsage (prefix=uses) |

## Likely-intentional — `delete_selected`-only, no bulk UI (44)

_Card changelists that omit only the default bulk-delete. Usually deliberate; listed for completeness._

`accounts.preferencechangelog`, `accounts.staffmember`, `announcements.announcement`, `cart.shippingmethod`, `cart.taxrate`, `design.menu`, `developer_portal.submissionreview`, `exchange_rates.exchangerateprovideraccount`, `exchange_rates.manualexchangerate`, `form_builder.form`, `form_builder.formresponse`, `geoip.countrymapping`, `geoip.geolocation`, `geoip.visitorlocation`, `loyalty.loyaltybadge`, `loyalty.loyaltytier`, `media_library.mediaasset`, `migration.migrationjob`, `migration.syncjob`, `page_builder.element`, `payment_providers.paymentprovideraccount`, `pos_app.posshift`, `pos_app.promoslide`, `pos_app.receipttemplate`, `pos_app.storegroup`, `product_feeds.feedprovideraccount`, `product_feeds.feedsynclog`, `referrals.referralevent`, `referrals.referralidentity`, `search.searchengine`, `search.searchquery`, `search.searchredirect`, `search.synonym`, `seo_generator.seoprovideraccount`, `shipping.carrierpreset`, `shipping.provideraccount`, `shipping.shippingpackage`, `shipping.shippingpromotion`, `shipping.shippingzone`, `shipping.webhooklog`, `sms_system.smsoutbox`, `sms_system.smsprovideraccount`, `sms_system.smstemplate`, `staff_roles.staffrole`

## Caveats

- **Custom bars:** a few models (e.g. `catalog.product`) have a bespoke bulk bar wired to a custom endpoint that covers *some* actions; the Django-registered ones remain unreachable. Marked as `custom bar` above.
- **Calendar/bespoke UIs:** e.g. `catalog.booking` is a calendar — a standard bulk bar is an awkward fit; per-item actions may be the right call.
- **Field/inline candidates** need a per-item glance (conditional tabs, intentional read-only).
- Findings are **as an active superuser**; per-permission visibility isn't modelled.