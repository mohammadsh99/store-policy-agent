import requests
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


def ask_agent(agent_name, instructions, question):
    started_at = perf_counter()
    print(f"[{agent_name}] Started")

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": question},
            ],
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    #return response.json()["message"]["content"]
    answer = response.json()["message"]["content"]
    duration = perf_counter() - started_at
    print(f"[{agent_name}] Finished in {duration:.2f} seconds")
    return answer


start = perf_counter()
with ThreadPoolExecutor(max_workers=2) as executor:
    return_task = executor.submit(
        ask_agent,
        "Return agent",
        "You handle returns. Products can be returned within 14 days "
        "of delivery. Compare the elapsed days with 14. "
        "If elapsed days are at most 14, the product is within the "
        "return window. Otherwise, it is outside the window. "
        "Use only this policy and answer in one sentence.",
        "I received my product 15 days ago. Can I return it?",
    )
    shipping_task = executor.submit(
        ask_agent,
        "Shipping agent",
        "You handle shipping questions. Delivery to Sakhnin costs 20 NIS. "
        "Use only this policy and answer in one sentence.",
        "How much does shipping to Sakhnin cost?",
    )
    return_answer = return_task.result()
    shipping_answer = shipping_task.result()
elapsed = perf_counter() - start
print("Return agent:", return_answer)
print("Shipping agent:", shipping_answer)
print(f"Elapsed: {elapsed:.2f} seconds")