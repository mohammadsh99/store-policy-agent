
import requests
from policy_search import search_policy

"""
def search_policy(query):
    if "sakhnin" in query:
        results.append("The delivery fee specifically for Sakhnin is 20 NIS.")

    return "No matching policy found."
"""
#def search_policy(query):
    #query = query.lower()
    #results = []

    #if "return" in query:
     #   results.append("You can return products within 14 days of delivery.")

    #if "sakhnin" in query:
    #    results.append("We deliver to Sakhnin. The delivery fee is 20 NIS.")

    #if results:
     #   return " ".join(results)

    #return "No matching policy found."


#result = search_policy("shipping to Sakhnin")
#print(result)
tool = {
    "type": "function",
    "function": {
        "name": "search_policy",
        "description": "Look up return rules and shipping fees in the store policy.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    },
}
"""
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1:8b",
        "messages": [
            {
                "role": "user",
                "content": "Use the store policy to find the shipping fee to Sakhnin.",
            }
        ],
        "tools": [tool],
        "stream": False,
    },
    timeout=120,
)
response.raise_for_status()
message = response.json()["message"]
#print(message.get("tool_calls", []))

tool_calls = message.get("tool_calls", [])
if tool_calls:
    function = tool_calls[0]["function"]

    if function["name"] == "search_policy":
        query = function["arguments"]["query"]
        result = search_policy(query)
        print("Tool result:", result)
        messages = [
            {
                "role": "user",
                "content": "Use the store policy to find the shipping fee to Sakhnin.",
            },
            message,
            {
                "role": "tool",
                "tool_name": "search_policy",
                "content": result,
            },
        ]
        final_response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.1:8b",
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )
        final_response.raise_for_status()
        answer = final_response.json()["message"]["content"]
        print("Final answer:", answer)
    else:
        print("Unknown tool:", function["name"])
else:
    print("The model did not request a tool.")
"""

messages = [
    {
    "role": "system",
    "content": (
        "For store policy questions, use the search_policy tool. "
        "Base your answer only on the tool results. "
        "If a detail is missing, say the policy does not specify it. "
        "Keep your answer brief."
        " Report policy facts directly and preserve their meaning. "
        "State the return window and the delivery fee separately."
        " If a tool reports an error, explain that the lookup failed. "
        "Only claim a detail is missing from the policy when a successful lookup supports that."
        "End each sentence that states a policy fact with the ID of the passage that supports it. "
        "Answer every part of the user's question directly. "
"If the user provides the number of days since delivery, say whether it is within the return window. "
    ),
},
    {
        "role": "user",
        "content": (
            "Use the store policy to answer both questions. "
            "I received a product 10 days ago. Can I return it, "
            "and how much does shipping to Sakhnin cost?"
        ),
    }
]

max_rounds = 5
policy_cache = {}
for round_number in range(1, max_rounds + 1):
    print(f"Round {round_number}")
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.1:8b",
                "messages": messages,
                "tools": [tool],
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("Ollama took too long to respond.")
        break

    except requests.exceptions.ConnectionError:
        print("Could not connect to Ollama. Make sure it is running.")
        break

    except requests.exceptions.HTTPError as error:
        print(f"Ollama returned HTTP {error.response.status_code}.")
        print(error.response.text)
        break
    
  #  response = requests.post(
        #"http://localhost:11434/api/chat",
     #   json={
           ##   "messages": messages,
        #    "tools": [tool],
           # "stream": False,
      #  },
     #   timeout=120,
   # )
   # response.raise_for_status()

    message = response.json()["message"]
    messages.append(message)
    tool_calls = message.get("tool_calls", [])

    if not tool_calls:
        print("Final answer:", message["content"])
        break

    for call in tool_calls:
        function = call["function"]
        name = function["name"]
        """
   #     if name == "search_policy":
    #        query = function["arguments"]["query"]
     #       print("Tool query:", query)
      #      #result = search_policy(query)
       #     key = query.strip().lower()
        #    if key in policy_cache:
         #    print("Using cached result.")
          #   result = policy_cache[key]
           # else:
        ##     result = search_policy(query)
          #   policy_cache[key] = result
           #  """
        if name == "search_policy":
            arguments = function.get("arguments", {})

            if isinstance(arguments, dict):
                query = arguments.get("query")
            else:
                query = None
            #query = 123   for test
            if not isinstance(query, str) or not query.strip():
                result = "Invalid query. Provide a non-empty string."
            else:
                print("Tool query:", query)
                key = query.strip().lower()

                if key in policy_cache:
                    print("Using cached result.")
                    result = policy_cache[key]
                else:
                    result = search_policy(query)
                    policy_cache[key] = result
          
        else:
            result = f"Unknown tool: {name}"

        print("Tool result:", result)
        messages.append({
            "role": "tool",
            "tool_name": name,
            "content": result,
        })
else:
    print("Stopped after reaching the maximum number of rounds.")

