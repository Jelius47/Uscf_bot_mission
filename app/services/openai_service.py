import logging
import shelve
import os
import json
import time
from dotenv import load_dotenv
import openai
from .functions import *  # Import function implementations
from .function_descriptions import uscf_functions
from langdetect import detect
from threading import Lock
# def detect_language(message):
#     """Detect the language of a given message."""
#     try:
#         return detect(message)
#     except Exception:
#         return "en"  # Default to English if detection fails

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables and set up OpenAI client
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("Missing OpenAI API Key.")
    raise ValueError("Set OPENAI_API_KEY in environment variables.")
client = openai.OpenAI(api_key=OPENAI_API_KEY)


# # Constants
THREAD_DB_FILE = "threads_db"
VECTOR_STORE_META_FILE = "vector_store_meta.json"
SYSTEM_PROMPT= """You are names are Elisha Daudi, Daniel Wandwi, Elipendo Millanton,Make sure you introduce yourself , Responsible to provide engaging, organized, and informative conversations to users required to share updates about missions, encourage participation, and simplify donation processes. Respond in an enthusiastic, empathetic, and professional manner, ensuring every interaction feels personal and valuable.
USE THE LANGUAGE OF THE USER TO RESPOND TO THEM.
Your primary goals are to:

Inform: Provide detailed and accurate information about USCF missions, updates, and services.
Engage: Create conversations that are interesting, respectful, and captivating, motivating users to stay engaged.
Encourage Donations: Smoothly guide users toward contributing financially or volunteering for mission outreach programs.
Be Accessible: Answer questions clearly and reduce confusion, offering complete responses to prevent unnecessary back-and-forth exchanges.
Use the following tone and principles in your conversations:

Warm and welcoming to make users feel valued.
Clear and concise when providing instructions or answering queries.
Encouraging and inspirational to motivate participation in missions or donations.
Respectful and considerate when addressing concerns or hesitations.
When responding to users:

Personalize the response if the user provides their name.
Always reference ongoing and past missions, emphasizing their impact.
Proactively share relevant details (e.g., gallery links, mission timelines, or donation instructions) without waiting for additional questions.
Continuously highlight the value of user contributions, whether financial or through volunteering.
Template for Responses:
When responding, use the following structured approach:

1. Warm Greeting:
"I'm here to help with mission updates, donations, or any questions you have."
🌟 **Missions Zetu:**

**Mtwara Outreach (Feb 15-22, 2025):** Tutakuwa tukieneza injili na kushiriki na jamii ya Mtwara ili kuleta athari ya kiroho ya kudumu. Hii ni fursa nzuri ya kushiriki upendo wa Kristo na kufanya tofauti!

**Simiyu Mission (Februari 2024):** Hii ni outreach yenye mabadiliko makubwa, kwa kushirikiana na USCF ARDHI. Zaidi ya maisha 200 yaliponywa, na shughuli zenye athari zilifanyika.Tazamapicha hapa :https://drive.google.com/drive/folders/1fqDeB5mxvCnyBbohH8ou7Fci_bUZmOPQ

🤝 **Ninavyoweza Kusaidia:**
- Kushiriki taarifa za misheni na updates ili kukuweka informed.
- Kutoa maelekezo ya kuchangia fedha kupitia Mobile Money, Bank Transfers, au njia nyingine.
- Kukusaidia kujiunga na ushirika wetu au kuwa volunteer kwa ajili ya misheni zijazo.

💖 **Msaada Wako Unafanya Tofauti!** Kila mchango, iwe ni kwa maombi, kujitolea, au donation ya kifedha, inatufanya tufikie malengo yetu ya misheni. Ikiwa unataka kujua jinsi ya kutoa au jinsi ya kujitolea, nijulishe tu!

📞 **Wasiliana na Viongozi:**
- **Treasurer:** +255686971266 (Jelius Heneriko)
- **Coordinators:** +255 693 827 599, +255 623 546 663.

Nijulishe jinsi ninavyoweza kusaidia zaidi! Pamoja, tunabadilisha maisha kwa ajili ya Kristo. TILL THE WHOLE WORLD KNOWS 😊
Mfano:
" Mimi ni Elipendo Millanton, niko hapa kukupa taarifa kuhusu misheni yetu ya USCF na jinsi unavyoweza kusaidia. 😊"
2. Toa Taarifa Muhimu Kuhusu Misheni
Taja misheni zinazoendelea na zilizopita, ukielezea athari zake.

Mfano:
"🌟 Misheni Zetu:\n"
"- Mtwara Outreach (Februari 15-22, 2025): Mpaka Ulimwengu Wote Ujue – MARKO 16:15. Tutashiriki injili na kushirikiana na jamii ya Mtwara kwa athari ya kiroho ya kudumu.\n"
"- Misheni ya Simiyu (Februari 2024): Zaidi ya watu 200 waliokolewa kupitia ushirikiano na USCF ARDHI. Tazama picha hapa.\n"
3. Eleza Msaada Unaoweza Kutoa
Fafanua jinsi unavyoweza kuwasaidia watumiaji.

Mfano:
"🤝 Jinsi Ninavyoweza Kukusaidia:\n"
"- Kutoa taarifa zaidi kuhusu misheni na masasisho.\n"
"- Kukuelekeza jinsi ya kuchangia kupitia Mobile Money, Benki, au njia nyingine.\n"
"- Kukusaidia kujiunga na ushirika wetu au kujitolea kwa misheni zijazo.\n"
"- Kushiriki ushuhuda wa kusisimua na picha kutoka misheni zilizopita.\n"
4. Kuhamasisha Michango
Wahimize watumiaji kuchangia kwa kusisitiza umuhimu wa msaada wao.

Mfano:
"💖 Msaada Wako Una Maana Kubwa:\n"
"Kila mchango, iwe ni maombi, kujitolea, au msaada wa kifedha, unatusaidia kufanikisha malengo ya misheni yetu. Je, ungependa kuchangia leo au kujiunga na timu yetu ya misheni?"
5. Toa Maelezo ya Jinsi ya Kuchangia
Eleza hatua za wazi za kutoa michango.

Mfano:
"💰 Njia za Michango:\n"
"- Mobile Money: USCF CCT TAKWIMU Utahitajika kuweka kiasi).\n"
"- Benki:\n"
" Jina la Akaunti: USCF CCT TAKWIMU\n"
" Namba ya Akaunti: 20810039672\n"
" Benki: NMB\n"
"- Lipa Namba: 19691543\n"
"- Vodacom: 0755 327 135\n"
6. Taja Mawasiliano Muhimu
Toa mawasiliano ya viongozi wa USCF.

Mfano:
"📞 Mawasiliano ya Viongozi:\n"
"- Mweka Hazina: +255686971266 (Jelius Heneriko)\n"
"- Waratibu: +255 693 827 599, +255 623 546 663\n"
7. Hitimisho la Kuhamasisha
Maliza kwa kuwahimiza kuchukua hatua na kutoa msaada wa ziada.

Mfano:
"Nijulishe jinsi ninavyoweza kukusaidia zaidi! Pamoja, tunaweza kubadilisha maisha kwa ajili ya Kristo. Mpaka Ulimwengu Wote Ujue! 😊"
Mfano wa Mazungumzo
Mteja: "Ningependa kujua kuhusu misheni ya Mtwara."

Bot (Elipendo Millanton):
"Ni furaha kukusikia! Mimi ni Elipendo Millanton, niko hapa kukupa taarifa kuhusu misheni yetu. 😊

🌟 Misheni Zetu:

Mtwara Outreach (Februari 15-22, 2025): Mpaka Ulimwengu Wote Ujue – MARKO 16:15. Tunatarajia kushiriki injili na kushirikiana na jamii ya Mtwara kwa athari ya kiroho ya kudumu.
Misheni ya Simiyu (Julai 2024): Zaidi ya watu 200 waliokolewa kupitia ushirikiano na USCF ARDHI. Tazama picha hapa!:https://drive.google.com/drive/folders/1fqDeB5mxvCnyBbohH8ou7Fci_bUZmOPQ
🤝 Jinsi Ninavyoweza Kukusaidia:

Kutoa taarifa zaidi kuhusu misheni na masasisho.
Kukuelekeza jinsi ya kuchangia kupitia Mobile Money, Benki, au njia nyingine.
Kukusaidia kujiunga na ushirika wetu au kujitolea kwa misheni zijazo.
💖 Msaada Wako Una Maana Kubwa:
Je, ungependa kuchangia leo au kujiunga na timu ya misheni ya Mtwara?

💰 Njia za Michango:

Mobile Money: USCF CCT TAKWIMU 
Benki:
Jina la Akaunti: USCF CCT TAKWIMU
Namba ya Akaunti: 20810039672
Benki: NMB
Lipa Namba: 19691543
Vodacom: 0755 327 135
📞 Mawasiliano ya Viongozi:

Mweka Hazina: +255686971266 (Jelius Heneriko)
Waratibu: +255 693 827 599, +255 623 546 663
Nijulishe jinsi ninavyoweza kukusaidia zaidi! Pamoja, tunaweza kubadilisha maisha kwa ajili ya Kristo. Mpaka Ulimwengu Wote Ujue! 😊

 
    """


VECTOR_STORE_NAME = "Takwimu_USCF_Vector_Store"
FILE_PATHS = ["../Hybrid_whatsap_bot/app/Bot_Data/USCF.txt","../Hybrid_whatsap_bot/app/Bot_Data/MISSION SURVEY.pdf","../Hybrid_whatsap_bot/app/Bot_Data/RISALA MAHAFALI YA 3.pdf"]



# Constants
VECTOR_STORE_META_FILE = "vector_store_metadata.json"

def load_metadata(file_path):
    """Load metadata from a JSON file."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)

def save_metadata(file_path, data):
    """Save metadata to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def upload_file_with_vector_store(file_paths, vector_store_name="DefaultVectorStore"):
    """
    Upload files to OpenAI and associate them with a vector store, checking for existing metadata.

    Args:
        file_paths (list of str): Paths of files to upload.
        vector_store_name (str): The name of the vector store.

    Returns:
        dict: Metadata about the vector store and uploaded files.
    """
    try:
        # Load existing metadata
        metadata = load_metadata(VECTOR_STORE_META_FILE)
        if metadata:
            logging.info(f"Loaded existing metadata: {metadata}")

            # Check if the vector store and files match
            if (
                metadata.get("vector_store_name") == vector_store_name
                and set(metadata.get("uploaded_files", [])) == set(file_paths)
            ):
                logging.info(f"Vector store '{vector_store_name}' and files already uploaded.")
                return metadata

        # No matching metadata; proceed with upload
        logging.info(f"Creating vector store: {vector_store_name}")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        logging.info(f"Vector store created with ID: {vector_store.id}")

        # Prepare file streams
        file_streams = [open(path, "rb") for path in file_paths]
        logging.info(f"Uploading files to vector store '{vector_store_name}'...")

        # Upload files and associate them with the vector store
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )

        # Safely extract file counts if available
        file_counts = {}
        if hasattr(file_batch, 'file_counts'):
            file_counts = {
                "processed_files": getattr(file_batch.file_counts, 'processed', None),
                "failed_files": getattr(file_batch.file_counts, 'failed', None),
                "pending_files": getattr(file_batch.file_counts, 'pending', None),
            }

        # Close file streams
        for stream in file_streams:
            stream.close()

        # Prepare and save metadata
        metadata = {
            "vector_store_name": vector_store_name,
            "vector_store_id": vector_store.id,
            "file_batch_status": file_batch.status,
            "file_counts": file_counts,
            "uploaded_files": file_paths,
        }
        save_metadata(VECTOR_STORE_META_FILE, metadata)

        # Log the result
        logging.info(f"File batch upload completed with status: {file_batch.status}")
        logging.info(f"File counts: {file_counts}")

        return metadata

    except Exception as e:
        logging.error(f"Error uploading files to vector store: {e}")
        raise RuntimeError("Failed to upload files to vector store.")

# Metadata File for Assistants
ASSISTANT_META_FILE = "assistants_meta.json"

def load_assistant_metadata():
    """Load assistant metadata from a local file."""
    if os.path.exists(ASSISTANT_META_FILE):
        with open(ASSISTANT_META_FILE, "r") as f:
            return json.load(f)
    return {}

def save_assistant_metadata(data):
    """Save assistant metadata to a local file."""
    with open(ASSISTANT_META_FILE, "w") as f:
        json.dump(data, f)




#  Main assistant function to handle user input and function calling
# def run_assistant(thread_id, name, message_body,wa_id):
#     try:
#         logging.info(f"Running assistant for thread: {thread_id}")
        
#         # Initialize conversation history with system instructions
#         conversation_history = [
#             {'role': 'system', 'content': f"You are having a conversation with the client named {name}. Instructions: {SYSTEM_PROMPT}"},
#             {'role': 'user', 'content': message_body}
#         ]

#         # Continuously handle responses until no function call is pending
#         while True:
#             # Send the message and get the response
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=conversation_history,
#                 functions=uscf_functions,
#                 function_call="auto"
#             )

#             # Check if choices and message content exist
#             if not response.choices or not response.choices[0].message:
#                 logging.error("No response choices or message content from assistant.")
#                 return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

#             # Retrieve the message from the response
#             response_message = response.choices[0].message

#             # Process function call if available
#             if hasattr(response_message, "function_call") and response_message.function_call:
#                 function_called = response_message.function_call.name
#                 function_args = json.loads(response_message.function_call.arguments)

#                 # Map function names to actual implementations
#                 available_functions = {
#                       "get_mission_info": get_mission_info,
#                       "provide_payment_instructions": provide_payment_instructions,
#                       "get_mission_progress": get_mission_progress,
#                       "list_saved_lives": list_saved_lives,
#                       "process_donation": process_donation,
#                       "get_mission_gallery": get_mission_gallery,


#                         }

#                 # Call the function and store result if function exists
#                 if function_called in available_functions:
#                     function_to_call = available_functions[function_called]

#                     # Call the function and store the result if it exists
#                     function_result = function_to_call(**function_args)
#                     logging.info(f"Function {function_called} executed with result: {function_result}")

#                     # Ensure the result is a string before appending to the conversation history
#                     if isinstance(function_result, list):
#                         function_result_str = "\n".join([f"{item['title']}: {item['description']}" for item in function_result])
#                     else:
#                         function_result_str = str(function_result)

#                     # Append function result as assistant's response in conversation history
#                     conversation_history.append({"role": "assistant", "content": function_result_str})
#                 else:
#                     logging.error(f"Function {function_called} not found.")
#                     return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

#             else:
#                 # If no function call is detected, break with final response content
#                 return response_message.content

#     except Exception as e:
#         logging.error(f"Error running assistant: {str(e)}")
#         return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

def run_assistant(thread_id, name, message_body, wa_id):
    """
    Runs the assistant, handles function calls, and dynamically matches parameters.

    Args:
        thread_id (str): The thread ID for the conversation.
        name (str): The user's name.
        message_body (str): The user's message.
        wa_id (str): The WhatsApp ID of the user.

    Returns:
        str: The assistant's response or an error message.
    """
    try:
        logging.info(f"Running assistant for thread: {thread_id}")

        # Initialize conversation history
        conversation_history = [
            {'role': 'system', 'content': f"You are having a conversation with the client named {name}. Instructions: {SYSTEM_PROMPT}"},
            {'role': 'user', 'content': message_body}
        ]

        # Send the user's input and get the response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            functions=uscf_functions,
            function_call="auto"
        )

        if not response.choices or not response.choices[0].message:
            logging.error("No response choices or message content from assistant.")
            return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

        response_message = response.choices[0].message

        # Check if the assistant requested a function call
        if hasattr(response_message, "function_call") and response_message.function_call:
            function_called = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)

            # Available function mapping
            available_functions = {
                "provide_payment_instructions": provide_payment_instructions,
                "get_mission_progress": get_mission_progress,
                "process_donation": process_donation,
                # "provide_welcome_message": provide_welcome_message,
            }

            if function_called in available_functions:
                function_to_call = available_functions[function_called]
                try:
                    # Match function arguments dynamically
                    # Provide default values for missing arguments
                    required_args = function_to_call.__code__.co_varnames
                    args_with_defaults = {
                        key: function_args.get(key, name if key == "name" else None)
                        for key in required_args
                    }
                    
                    # Call the function with matched arguments
                    result = function_to_call(**args_with_defaults)
                    logging.info(f"Function '{function_called}' executed successfully.")
                except TypeError as e:
                    logging.error(f"Argument mismatch for '{function_called}': {e}")
                    return "Samahani, kuna tatizo katika kupokea taarifa zako. Tafadhali jaribu tena."

                # Append the result to conversation history
                if isinstance(result, str):
                    conversation_history.append({"role": "assistant", "content": result})
                    return result
                else:
                    logging.error(f"Unexpected return type from '{function_called}': {type(result)}")
                    return "Samahani, kuna tatizo. Tafadhali jaribu tena."

            else:
                logging.error(f"Function '{function_called}' not found.")
                return "Samahani, huduma unayoomba haipatikani kwa sasa. Tafadhali jaribu tena."

        # If no function call is requested, return the assistant's response
        return f"{response_message.content} **{name}**"

    except Exception as e:
        logging.error(f"Error running assistant: {str(e)}")
        return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."


'''
Dealing with the retrieval assistant
'''


def get_or_create_retrieval_assistant(vector_store_id):
    """Retrieve or create a retrieval assistant."""
    metadata = load_assistant_metadata()
    if "retrieval_assistant_id" in metadata:
        logging.info(f"Using existing Retrieval Assistant ID: {metadata['retrieval_assistant_id']}")
        return metadata["retrieval_assistant_id"]

    try:
        # Create the retrieval assistant
        assistant = client.beta.assistants.create(
            name="RetrievalAssistant",
            instructions=SYSTEM_PROMPT,
            model="gpt-4o-mini",
            tools=[{"type": "file_search"}],
        )
        updated_assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        logging.info(f"Retrieval assistant created successfully with ID: {updated_assistant.id}")

        # Save the assistant ID
        metadata["retrieval_assistant_id"] = updated_assistant.id
        save_assistant_metadata(metadata)
        return updated_assistant.id

    except Exception as e:
        logging.error(f"Failed to create retrieval assistant: {e}")
        raise RuntimeError("Failed to create the retrieval assistant.")

# Initialize Assistants
def initialize_assistants():
    """Initialize vector store and assistants."""
    # Check if metadata for vector store exists and matches files
    metadata = upload_file_with_vector_store(FILE_PATHS, VECTOR_STORE_NAME)
    vector_store_id = metadata["vector_store_id"]

    # Retrieve or create the retrieval assistant
    retrieval_assistant_id = get_or_create_retrieval_assistant(vector_store_id)

    logging.info(f"Retrieval Assistant ID: {retrieval_assistant_id}")
    return retrieval_assistant_id



#Initialize assistants
retrieval_assistant_id = initialize_assistants()

# Define routing keywords and determine assistant type
function_call_keywords = [
    "donate", "payment", "instructions", "mobile money", "bank account", "lipa namba", 
    "how to donate", "donation method", "mission progress", "fundraising", "status", 
    "update", "mission details","funds raised", "volunteers","confirm donation", 
    "make donation", "send money", "donate now", "process payment","start", "help", "about us"
]

def determine_assistant(message_body):
    """Determines the appropriate assistant based on message content."""
    if any(keyword in message_body.lower() for keyword in function_call_keywords):
        return "function"
    return "retrieval"

# Thread management for user interactions
def get_or_create_thread(wa_id):
    with shelve.open(THREAD_DB_FILE, writeback=True) as threads_shelf:
        thread_id = threads_shelf.get(wa_id)
        if not thread_id:
            try:
                thread = client.beta.threads.create()
                threads_shelf[wa_id] = thread.id
                logging.info(f"New thread created for wa_id '{wa_id}' with thread ID: {thread.id}")
                return thread.id
            except Exception as e:
                logging.error(f"Error creating new thread: {e}")
                raise RuntimeError("Failed to create thread.")
        return thread_id



# Thread lock for concurrency
# processed_messages = {}
# message_lock = Lock()

processed_messages = set()  # Store processed WhatsApp message IDs


def run_retrieval_assistant(thread_id, name, message_body, assistant_id):
    """Run retrieval assistant and get a response."""
    try:
        # Add the user message to the thread
        user_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"{message_body},my name is {name}",
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Wait for the run to complete
        while run.status != "completed":
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
 # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant" and msg.content:
                # Check if content is in a complex structure and extract text
                if isinstance(msg.content, list):
                    for content_block in msg.content:
                        if hasattr(content_block, "text") and hasattr(content_block.text, "value"):
                            logging.info(f"Assistant responded with: {content_block.text.value}")
                            return content_block.text.value
                elif isinstance(msg.content, str):
                    logging.info(f"Assistant responded with: {msg.content}")
                    return msg.content

        return "Sorry, no valid response received from the assistant."

    except Exception as e:
        logging.error(f"Error running retrieval assistant: {e}")
        return "Sorry, an error occurred. Please try again later."
    
def get_or_create_thread(wa_id):
    """Retrieve or create a thread for the user."""
    with shelve.open(THREAD_DB_FILE, writeback=True) as threads_shelf:
        thread_id = threads_shelf.get(wa_id)
        if thread_id:
            logging.info(f"Found existing thread ID for wa_id '{wa_id}': {thread_id}")
            return thread_id

        try:
            thread = client.beta.threads.create()
            threads_shelf[wa_id] = thread.id
            logging.info(f"New thread created for wa_id '{wa_id}' with thread ID: {thread.id}")
            return thread.id
        except Exception as e:
            logging.error(f"Error creating new thread: {e}")
            raise RuntimeError("Failed to create thread.")
# Generate response
def generate_response(message_body, wa_id, name):
    """Route the message to the appropriate assistant."""
    thread_id = get_or_create_thread(wa_id)

    # Determine assistant type based on the message content
    assistant_type = determine_assistant(message_body)
    if assistant_type == "function":
        logging.info("Routing to function assistant.")
        return run_assistant(thread_id, name, message_body,wa_id)
    else:
        logging.info("Routing to retrieval assistant.")
        return run_retrieval_assistant(thread_id, name, message_body, retrieval_assistant_id)
