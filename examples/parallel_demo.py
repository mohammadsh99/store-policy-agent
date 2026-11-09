from concurrent.futures import ThreadPoolExecutor
from time import sleep, perf_counter


def get_return_policy():
    sleep(2)
    return "Products can be returned within 14 days of delivery."


def get_shipping_fee():
    sleep(2)
    return "Delivery to Sakhnin costs 20 NIS."


#start = perf_counter()

#with ThreadPoolExecutor(max_workers=2) as executor:
 #   return_task = executor.submit(get_return_policy)
  #  shipping_task = executor.submit(get_shipping_fee)

 #   return_policy = return_task.result()
  #  shipping_fee = shipping_task.result()

#elapsed = perf_counter() - start

#print(return_policy)
#print(shipping_fee)
#print(f"Elapsed: {elapsed:.2f} seconds")


start = perf_counter()

return_policy = get_return_policy()
shipping_fee = get_shipping_fee()

elapsed = perf_counter() - start

print(return_policy)
print(shipping_fee)
print(f"Elapsed: {elapsed:.2f} seconds")