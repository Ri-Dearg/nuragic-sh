"""Stripe API data for spoofing tests."""
# ruff: noqa: E501

PAYMENT_INTENT_FAILED = """{
  "api_version": "2020-08-27",
  "data": {
    "object": {
        "id": "pi_3RBQQ4KgztVVywsM1DAJETfZ",
        "object": "payment_intent",
        "am ount": 12699,
        "amount_capturable": 0,
        "amount_details": {"tip": {}},
        "amount_received": 0,
        "application": null,
        "application_fee_amount": null,
        "automatic_payment_methods": {
            "allow_redirects": "always",
            "enabled": true
        },
        "canceled_at": null,
        "cancellation_reason": null,
        "capture_method": "automatic_async",
        "charges": {
            "object": "list",
            "data": [
                {
                    "id": "ch_3RBQQ4KgztVVywsM1ff3xR9i",
                    "object": "charge",
                    "amount": 12699,
                    "amount_captured": 0,
                    "amount_refunded": 0,
                    "application": null,
                    "application_fee": null,
                    "application_fee_amount": null,
                    "balance_transaction": null,
                    "billing_details": {
                        "address": {
                            "city": "Location",
                            "country": "IT",
                            "line1": "location at place",
                            "line2": "Other place",
                            "postal_code": "99999",
                            "state": "CA"
                        },
                        "email": "test@test.com",
                        "name": "Jeremy Fisher",
                        "phone": "+353891111111"
                    },
                    "calculated_statement_descriptor": "NURAGICSHAMANICHEALING",
                    "captured": false,
                    "created": 1744073635,
                    "currency": "eur",
                    "customer": null,
                    "description": null,
                    "destination": null,
                    "dispute": null,
                    "disputed": false,
                    "failure_balance_transaction": null,
                    "failure_code": "card_declined",
                    "failure_message": "Your card was declined.",
                    "fraud_details": {},
                    "invoice": null,
                    "livemode": false,
                    "metadata": {
                    "cart": "{\\"1\\": 1, \\"2\\": 1}",
                        "delivery": "6.99",
                        "lang": "en",
                        "save_info": "false",
                        "user": "testuser"
                    },
                    "on_behalf_of": null,
                    "order": null,
                    "outcome": {
                        "advice_code": "try_again_later",
                        "network_advice_code": null,
                        "network_decline_code": null,
                        "network_status": "declined_by_network",
                        "reason": "generic_decline",
                        "risk_level": "normal",
                        "risk_score": 51,
                        "seller_message": "The bank did not return any further details with this decline.",
                        "type": "issuer_declined"
                    },
                    "paid": false,
                    "payment_intent": "pi_3RBQQ4KgztVVywsM1DAJETfZ",
                    "payment_method": "pm_1RBQQIKgztVVywsMGeUwm7Df",
                    "payment_method_details": {
                        "card": {
                            "amount_authorized": null,
                            "authorization_code": null,
                            "brand": "visa",
                            "checks": {
                                "address_line1_check": "pass",
                                "address_postal_code_check": "pass",
                                "cvc_check": "pass"
                            },
                            "country": "US",
                            "exp_month": 3,
                            "exp_year": 2043,
                            "extended_authorization": {"status": "disabled"},
                            "fingerprint": "cwPXg9IW96njtlPU",
                            "funding": "credit",
                            "incremental_authorization": {
                                "status": "unavailable"
                            },
                            "installments": null,
                            "last4": "0002",
                            "mandate": null,
                            "multicapture": {"status": "unavailable"},
                            "network": "visa",
                            "network_token": {"used": false},
                            "network_transaction_id": "991198088103577",
                            "overcapture": {
                                "maximum_amount_capturable": 12699,
                                "status": "unavailable"
                            },
                            "regulated_status": "unregulated",
                            "three_d_secure": null,
                            "wallet": null
                        },
                        "type": "card"
                    },
                    "radar_options": {},
                    "receipt_email": null,
                    "receipt_number": null,
                    "receipt_url": null,
                    "refunded": false,
                    "refunds": {
                        "object": "list",
                        "data": [],
                        "has_more": false,
                        "total_count": 0,
                        "url": "/v1/charges/ch_3RBQQ4KgztVVywsM1ff3xR9i/refunds"
                    },
                    "review": null,
                    "shipping": {
                        "address": {
                            "city": "Location",
                            "country": "IT",
                            "line1": "location at place",
                            "line2": "Other place",
                            "postal_code": "99999",
                            "state": "CA"
                        },
                        "carrier": null,
                        "name": "Jeremy Fisher",
                        "phone": "+353891111111",
                        "tracking_number": null
                    },
                    "source": null,
                    "source_transfer": null,
                    "statement_descriptor": null,
                    "statement_descriptor_suffix": null,
                    "status": "failed",
                    "transfer_data": null,
                    "transfer_group": null
                }
            ],
            "has_more": false,
            "total_count": 1,
            "url": "/v1/charges?payment_intent=pi_3RBQQ4KgztVVywsM1DAJETfZ"
        },
        "client_secret": "pi_3RBQQ4KgztVVywsM1DAJETfZ_secret_WGITDxCitxrslauoT2DU5lUZO",
        "confirmation_method": "automatic",
        "created": 1744073620,
        "currency": "eur",
        "customer": null,
        "description": null,
        "invoice": null,
        "last_payment_error": {
            "advice_code": "try_again_later",
            "charge": "ch_3RBQQ4KgztVVywsM1ff3xR9i",
            "code": "card_declined",
            "decline_code": "generic_decline",
            "doc_url": "https://stripe.com/docs/error-codes/card-declined",
            "message": "Your card was declined.",
            "payment_method": {
                "id": "pm_1RBQQIKgztVVywsMGeUwm7Df",
                "object": "payment_method",
                "allow_redisplay": "unspecified",
                "billing_details": {
                    "address": {
                        "city": "Location",
                        "country": "IT",
                        "line1": "location at place",
                        "line2": "Other place",
                        "postal_code": "99999",
                        "state": "CA"
                    },
                    "email": "test@test.com",
                    "name": "Jeremy Fisher",
                    "phone": "+353891111111"
                },
                "card": {
                    "brand": "visa",
                    "checks": {
                        "address_line1_check": "pass",
                        "address_postal_code_check": "pass",
                        "cvc_check": "pass"
                    },
                    "country": "US",
                    "display_brand": "visa",
                    "exp_month": 3,
                    "exp_year": 2043,
                    "fingerprint": "cwPXg9IW96njtlPU",
                    "funding": "credit",
                    "generated_from": null,
                    "last4": "0002",
                    "networks": {"available": ["visa"], "preferred": null},
                    "regulated_status": "unregulated",
                    "three_d_secure_usage": {"supported": true},
                    "wallet": null
                },
                "created": 1744073634,
                "customer": null,
                "livemode": false,
                "metadata": {},
                "type": "card"
            },
            "type": "card_error"
        },
        "latest_charge": "ch_3RBQQ4KgztVVywsM1ff3xR9i",
        "livemode": false,
        "metadata": {
            "cart": "{\\"1\\": 1, \\"2\\": 1}",
            "delivery": "6.99",
            "lang": "en",
            "save_info": "false",
            "user": "testuser"
        },
        "next_action": null,
        "on_behalf_of": null,
        "payment_method": null,
        "payment_method_configuration_details": {
            "id": "pmc_1KSqIjKgztVVywsMTaYyk769",
            "parent": null
        },
        "payment_method_options": {
            "alipay": {},
            "bancontact": {"preferred_language": "en"},
            "card": {
                "installments": null,
                "mandate_options": null,
                "network": null,
                "request_three_d_secure": "automatic"
            },
            "eps": {},
            "giropay": {},
            "ideal": {},
            "klarna": {"preferred_locale": null},
            "link": {"persistent_token": null},
            "multibanco": {},
            "p24": {},
            "sepa_debit": {},
            "sofort": {"preferred_language": null},
            "wechat_pay": {"app_id": null, "client": null}
        },
        "payment_method_types": [
            "card",
            "bancontact",
            "eps",
            "giropay",
            "ideal",
            "p24",
            "sepa_debit",
            "sofort",
            "alipay",
            "klarna",
            "multibanco",
            "wechat_pay",
            "link"
        ],
        "processing": null,
        "receipt_email": null,
        "review": null,
        "setup_future_usage": null,
        "shipping": {
            "address": {
                "city": "Location",
                "country": "IT",
                "line1": "location at place",
                "line2": "Other place",
                "postal_code": "99999",
                "state": "CA"
            },
            "carrier": null,
            "name": "Jeremy Fisher",
            "phone": "+353891111111",
            "tracking_number": null
        },
        "source": null,
        "statement_descriptor": null,
        "statement_descriptor_suffix": null,
        "status": "requires_payment_method",
        "transfer_data": null,
        "transfer_group": null
    },
    "previous_attributes": null
  },
  "type": "payment_intent.payment_failed"
}"""

PAYMENT_INTENT_SUCCEEDED = """{
    "id": "evt_3RKL02KgztVVywsM1a73yl5e",
    "object": "event",
    "api_version": "2020-08-27",
    "data": {
        "object": {
            "id": "pi_3RKL02KgztVVywsM1FGJFkp0",
            "object": "payment_intent",
            "amount": 12699,
            "amount_capturable": 0,
            "amount_details": {
                "tip": {}
            },
            "amount_received": 12699,
            "application": null,
            "application_fee_amount": null,
            "automatic_payment_methods": {
                "allow_redirects": "always",
                "enabled": true
            },
            "canceled_at": null,
            "cancellation_reason": null,
            "capture_method": "automatic_async",
            "charges": {
                "object": "list",
                "data": [
                    {
                        "id": "ch_3RKL02KgztVVywsM1IN7OAzI",
                        "object": "charge",
                        "amount": 12699,
                        "amount_captured": 12699,
                        "amount_refunded": 0,
                        "application": null,
                        "application_fee": null,
                        "application_fee_amount": null,
                        "balance_transaction": null,
                        "billing_details": {
                            "address": {
                                "city": "Town",
                                "country": "IT",
                                "line1": "Location 1",
                                "line2": "100",
                                "postal_code": "24242",
                                "state": "CA"
                            },
                            "email": "email@email.com",
                            "name": "Test user 1",
                            "phone": "+395555555555",
                            "tax_id": null
                        },
                        "calculated_statement_descriptor": "NURAGICSHAMANICHEALING",
                        "captured": true,
                        "created": 1746197756,
                        "currency": "eur",
                        "customer": null,
                        "description": null,
                        "destination": null,
                        "dispute": null,
                        "disputed": false,
                        "failure_balance_transaction": null,
                        "failure_code": null,
                        "failure_message": null,
                        "fraud_details": {},
                        "invoice": null,
                        "livemode": false,
                        "metadata": {
                            "cart": "{\\"1\\": 1, \\"2\\": 1}",
                            "delivery": "6.99",
                            "lang": "en",
                            "save_info": "false",
                            "user": "rory"
                        },
                        "on_behalf_of": null,
                        "order": null,
                        "outcome": {
                            "advice_code": null,
                            "network_advice_code": null,
                            "network_decline_code": null,
                            "network_status": "approved_by_network",
                            "reason": null,
                            "risk_level": "normal",
                            "risk_score": 52,
                            "seller_message": "Payment complete.",
                            "type": "authorized"
                        },
                        "paid": true,
                        "payment_intent": "pi_3RKL02KgztVVywsM1FGJFkp0",
                        "payment_method": "pm_1RKL0KKgztVVywsMdCWNpj78",
                        "payment_method_details": {
                            "card": {
                                "amount_authorized": 12699,
                                "authorization_code": null,
                                "brand": "visa",
                                "checks": {
                                    "address_line1_check": "pass",
                                    "address_postal_code_check": "pass",
                                    "cvc_check": "pass"
                                },
                                "country": "US",
                                "exp_month": 4,
                                "exp_year": 2026,
                                "extended_authorization": {
                                    "status": "disabled"
                                },
                                "fingerprint": "aTqilsZxzZefygD0",
                                "funding": "credit",
                                "incremental_authorization": {
                                    "status": "unavailable"
                                },
                                "installments": null,
                                "last4": "4242",
                                "mandate": null,
                                "multicapture": {
                                    "status": "unavailable"
                                },
                                "network": "visa",
                                "network_token": {
                                    "used": false
                                },
                                "network_transaction_id": "978411310510811",
                                "overcapture": {
                                    "maximum_amount_capturable": 12699,
                                    "status": "unavailable"
                                },
                                "regulated_status": "unregulated",
                                "three_d_secure": null,
                                "wallet": null
                            },
                            "type": "card"
                        },
                        "radar_options": {},
                        "receipt_email": null,
                        "receipt_number": null,
                        "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xSWRjTm5LZ3p0VlZ5d3NNKPy508AGMgaPo_LR8_g6LBYGpgwz7XUnx2RBprtBoUueOG9kF2kaM2FCpRWbwFstYBtUYKJCbOVDqz2H",
                        "refunded": false,
                        "refunds": {
                            "object": "list",
                            "data": [],
                            "has_more": false,
                            "total_count": 0,
                            "url": "/v1/charges/ch_3RKL02KgztVVywsM1IN7OAzI/refunds"
                        },
                        "review": null,
                        "shipping": {
                            "address": {
                                "city": "Town",
                                "country": "IT",
                                "line1": "Location 1",
                                "line2": "100",
                                "postal_code": "24242",
                                "state": "CA"
                            },
                            "carrier": null,
                            "name": "Test user 1",
                            "phone": "+395555555555",
                            "tracking_number": null
                        },
                        "source": null,
                        "source_transfer": null,
                        "statement_descriptor": null,
                        "statement_descriptor_suffix": null,
                        "status": "succeeded",
                        "transfer_data": null,
                        "transfer_group": null
                    }
                ],
                "has_more": false,
                "total_count": 1,
                "url": "/v1/charges?payment_intent=pi_3RKL02KgztVVywsM1FGJFkp0"
            },
            "client_secret": "pi_3RKL02KgztVVywsM1FGJFkp0_secret_TZFyc9EtmNb6S9HG9idI64D6Q",
            "confirmation_method": "automatic",
            "created": 1746197738,
            "currency": "eur",
            "customer": null,
            "description": null,
            "invoice": null,
            "last_payment_error": null,
            "latest_charge": "ch_3RKL02KgztVVywsM1IN7OAzI",
            "livemode": false,
            "metadata": {
                "cart": "{\\"1\\": 1, \\"2\\": 1}",
                "delivery": "6.99",
                "lang": "en",
                "save_info": "false",
                "user": "rory"
            },
            "next_action": null,
            "on_behalf_of": null,
            "payment_method": "pm_1RKL0KKgztVVywsMdCWNpj78",
            "payment_method_configuration_details": {
                "id": "pmc_1KSqIjKgztVVywsMTaYyk769",
                "parent": null
            },
            "payment_method_options": {
                "alipay": {},
                "bancontact": {
                    "preferred_language": "en"
                },
                "card": {
                    "installments": null,
                    "mandate_options": null,
                    "network": null,
                    "request_three_d_secure": "automatic"
                },
                "eps": {},
                "giropay": {},
                "ideal": {},
                "klarna": {
                    "preferred_locale": null
                },
                "link": {
                    "persistent_token": null
                },
                "multibanco": {},
                "p24": {},
                "sepa_debit": {},
                "sofort": {
                    "preferred_language": null
                },
                "wechat_pay": {
                    "app_id": null,
                    "client": null
                }
            },
            "payment_method_types": [
                "card",
                "bancontact",
                "eps",
                "giropay",
                "ideal",
                "p24",
                "sepa_debit",
                "sofort",
                "alipay",
                "klarna",
                "multibanco",
                "wechat_pay",
                "link"
            ],
            "processing": null,
            "receipt_email": null,
            "review": null,
            "setup_future_usage": null,
            "shipping": {
                "address": {
                    "city": "Town",
                    "country": "IT",
                    "line1": "Location 1",
                    "line2": "100",
                    "postal_code": "24242",
                    "state": "CA"
                },
                "carrier": null,
                "name": "Test user 1",
                "phone": "+395555555555",
                "tracking_number": null
            },
            "source": null,
            "statement_descriptor": null,
            "statement_descriptor_suffix": null,
            "status": "succeeded",
            "transfer_data": null,
            "transfer_group": null
        },
        "previous_attributes": null
    },
    "type": "payment_intent.succeeded"
}"""
