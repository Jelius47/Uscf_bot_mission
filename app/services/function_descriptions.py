# eastc_functions = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_contact_info",
#             "description": "Provide contact information for EASTC.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "department": {
#                         "type": "string",
#                         "description": "The specific department to get contact info for (e.g., 'admissions', 'finance')."
#                     }
#                 },
#                 "required": ["department"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "process_payment",
#             "description": "Process a payment with specified details.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "amount": {
#                         "type": "number",
#                         "description": "The amount to be paid."
#                     },
#                     "currency": {
#                         "type": "string",
#                         "description": "The currency in which the payment is made (e.g., 'USD', 'EUR')."
#                     },
#                     "method": {
#                         "type": "string",
#                         "description": "The payment method to use, e.g., 'credit card', 'bank transfer'."
#                     }
#                 },
#                 "required": ["amount", "currency", "method"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "check_payment_status",
#             "description": "Check the status of a specific payment.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "transaction_id": {
#                         "type": "string",
#                         "description": "The transaction ID of the payment to check."
#                     }
#                 },
#                 "required": ["transaction_id"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "provide_payment_instructions",
#             "description": "Provide instructions for making a payment.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "method": {
#                         "type": "string",
#                         "description": "The method of payment, e.g., 'credit card', 'bank transfer'."
#                     }
#                 },
#                 "required": ["method"]
#             }
#         }
#     }
# ]
uscf_functions = [
                # {
                # "name": "get_mission_info",
                # "description": "Retrieve details about upcoming or past mission outreaches.",
                # "parameters": {
                #     "type": "object",
                #     "properties": {
                #     "mission_name": {
                #         "type": "string",
                #         "description": "The name or location of the mission, e.g., 'Mtwara Outreach' or 'Simiyu Mission'."
                #     }
                #     },
                #     "required": ["mission_name"]
                # }
                # },
                # {
                #     "name": "provide_welcome_message",
                #     "description": "Generate and provide a dynamic welcome message introducing the assistant's capabilities and available services.",
                #     "parameters": {
                #         "type": "object",
                #         "properties": {
                #             "user_name": {
                #                 "type": "string",
                #                 "description": "The name of the user, if available, to personalize the welcome message.",
                #             }
                #         },
                #         "required": []
                #     }
                #     },
                    {
                        "name": "provide_payment_instructions",
                        "description": "Provide instructions on how to make a donation.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "payment_method": {
                                "type": "string",
                                "description": "The preferred payment method, e.g., 'mobile money', 'bank transfer'."
                            }
                            },
                            "required": ["payment_method"]
                        }
                        }
,
                    {
                        "name": "get_mission_progress",
                        "description": "Track progress of mission outreach, including funds raised and people involved.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "mission_name": {
                                "type": "string",
                                "description": "The name or location of the mission outreach, e.g., 'Mtwara Outreach'."
                            }
                            },
                            "required": ["mission_name"]
                        }
                        },
                        # {
                        #     "name": "list_saved_lives",
                        #     "description": "Provide details about the number of lives saved during a mission and their stories.",
                        #     "parameters": {
                        #         "type": "object",
                        #         "properties": {
                        #         "mission_name": {
                        #             "type": "string",
                        #             "description": "The name or location of the mission, e.g., 'Simiyu Mission'."
                        #         }
                        #         },
                        #         "required": ["mission_name"]
                        #     }
                        # },
                        # {
                        # "name": "get_mission_gallery",
                        # "description": "Retrieve pictures and highlights from a specific mission event.",
                        # "parameters": {
                        #     "type": "object",
                        #     "properties": {
                        #     "mission_name": {
                        #         "type": "string",
                        #         "description": "The name or location of the mission, e.g., 'Simiyu Mission'."
                        #     }
                        #     },
                        #     "required": ["mission_name"]
                        # }
                        # },
                        {
                        "name": "process_donation",
                        "description": "Handle donations for mission fundraising.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "donor_name": {
                                "type": "string",
                                "description": "The name of the person making the donation."
                            },
                            "amount": {
                                "type": "number",
                                "description": "The amount donated."
                            },
                            "payment_method": {
                                "type": "string",
                                "description": "The method of payment, e.g., 'mobile money', 'bank transfer'."
                            }
                            },
                            "required": ["donor_name", "amount", "payment_method"]
                        }
                        },






                    ]