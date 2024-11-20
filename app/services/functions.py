from .zeno_pay import make_payment
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# def get_mission_info(mission_name):
#     missions = {
#         "Mtwara Outreach": {
#             "date": "February 2025",
#             "description": "An upcoming mission to spread the gospel and engage with the community in Mtwara.",
#             "gallery": "link for the gallery",
#             "fund_raised": get_mission_gallery(mission_name="Mtwara Outreach"),
        
#         },
#         "Simiyu Mission": {
#             "date": "July 2024",
#             "description": "A collaborative outreach with USCF ARDHI that resulted in many lives being saved.",
#             "gallery": "link for the gallery",
#             "fund_raised": get_mission_gallery(mission_name="Simiyu Mission"),
#         }
#     }
#     return missions.get(mission_name,( "Mtwara Outreach"+"\n"+"Simiyu Mission"))


def provide_payment_instructions(payment_method):
    """
    Provides payment instructions based on the payment method and prompts the user for details.

    Args:
        payment_method (str): The chosen payment method.

    Returns:
        str: Payment instructions and prompts for user input if required.
    """
    instructions = {
        "mobile money": "Send your donation to USCF CCT TAKWIMU ZENO PAY (YOU WILL BE PROMPTED TO ENTER THE AMOUNT YOU WANT TO DONATE).",
        "bank transfer": "Account Name: USCF CCT TAKWIMU, Account Number: 20810039672, Bank: NMB.",
        "cash": "You can donate in person at our office or at any of our partner churches.",
        "lipa namba": "USCF CCT TAKWIMU, lipa namba: 19691543",
        "Vodacom": "USCF CCT TAKWIMU, Vodacom: 0755 327 135",
    }

    payment_instruction = instructions.get(payment_method, "Payment method not recognized.")
    if payment_instruction == "Payment method not recognized.":
        return payment_instruction

    # Prompt the user for missing details
    return (
        f"Here are the payment instructions for {payment_method}:\n\n{payment_instruction}\n\n"
        "To proceed with the donation, please provide the following details:\n"
        "- Your Name\n"
        "- Your Phone Number\n"
        "- The Amount You Wish to Donate\n\n"
        "You can reply with:\n"
        "`Name: [Your Name], Phone: [Your Phone Number], Amount: [Donation Amount]`\n"
        "Once we have these details, we will process your donation."
    )

def process_donation(donor_details, payment_method):
    """
    Processes the donation based on user-provided details.

    Args:
        donor_details (str): User-provided string containing name, phone, and amount.
        payment_method (str): The chosen payment method.

    Returns:
        str: Confirmation message or error if details are incomplete.
    """
    try:
        # Parse donor details
        donor_info = {}
        for part in donor_details.split(","):
            key, value = part.strip().split(":")
            donor_info[key.strip().lower()] = value.strip()

        # Validate required fields
        required_fields = ["name", "phone", "amount"]
        missing_fields = [field for field in required_fields if field not in donor_info]
        if missing_fields:
            return f"Missing details: {', '.join(missing_fields)}. Please provide all the required details."

        # Extract details
        donor_name = donor_info["name"]
        wa_id = donor_info["phone"]
        amount = float(donor_info["amount"])

        # Handle mobile money payments
        if payment_method == "mobile money":
            asyncio.run(make_payment(amount, wa_id, donor_name))
            return f"Thank you {donor_name} for your generous donation of {amount} via {payment_method}!"

        # Handle other payment methods
        return (
            f"Thank you {donor_name} for your generous heart for the Kingdom of God!\n\n"
            f"We would like to get confirmation from you if you preferred to donate via **{payment_method}**.\n\n"
            f"Please confirm by contacting:\n\n"
            f"**Phone:** +255686971266\n"
            f"**Name:** Jelius Heneriko\n"
            f"**Position:** Treasurer, USCF CCT TAKWIMU"
        )

    except ValueError as e:
        logging.error(f"Error parsing donation details: {e}")
        return "Invalid input format. Please provide your details as:\n" \
               "`Name: [Your Name], Phone: [Your Phone Number], Amount: [Donation Amount]`."

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "An error occurred while processing your donation. Please try again later."
def get_mission_progress(mission_name):
    progress = {
        "Mtwara Outreach": {"funds_to_raise": " 20,000,000 Tsh (Twenty million Tanzania shillings) till now funds rised are 5,000,000/= Ths(Five million Tanzania Shillings)", "volunteers": 50},
        "Simiyu Mission": {"funds_raised": 2000000, "volunteers": "{94} were volunteer students from Takwimu ,Ardhi and surrounding campuses such as UDDSM,MAJI and INSTITUTE IF SOCIAL WORK while atleast 200 people were saved and made to follow Christ"},
    }
    return progress.get(mission_name, "Mission progress not found.")

# def list_saved_lives(mission_name):
#     saved_lives = {
#         "Simiyu Mission": {"total_saved": f"{200}\nhere are some of the events {https://drive.google.com/drive/folders/1fqDeB5mxvCnyBbohH8ou7Fci_bUZmOPQ}", "testimonies": ["We are glad the school called BUDEKWA SECOMARY wheree went to volunteer in teachin during mission almost all of them passed they final exams", "Also we conducted charity to the loccal hospital ,and near by schools includig BUDEKWA SECOMARY ,primary school and the one nursery school in the village "]},
#     }
#     return saved_lives.get(mission_name,"Siimiyu Mission")

# def get_mission_gallery(mission_name):
#     gallery = {
#         "Simiyu Mission": "please click this to view the events happened at simiyu mission in the village of BUDEKWA\n{https://drive.google.com/drive/folders/1fqDeB5mxvCnyBbohH8ou7Fci_bUZmOPQ}",
#     }
#     return gallery.get(mission_name, "Simiyu Mission")

