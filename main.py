from web3 import Web3, HTTPProvider, Account
import random
from requests import Session
import time
from Bera_Swap_Stg import swap as swap1
from Swap_STG_HONEY import swap2 as swap2
from Mint_Domain import mint_domain as mint
from Supply_Honey_Bend import supply_honey_bend as supply
from Withdraw_HONEY_bend import withdraw_bend as withdraw_bend
from Deposit_Honey_Berps_Vault import deposit_honey_berps as deposit_honey_berps
from Withdraw_HONEY_berps import withdraw2 as withdraw_berps
from config import STG_USDC, AHONEY_ADDRESS, approve_abi

sess = Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                     'Accept': '*/*'})

class MyHTTPProvider(HTTPProvider):
    def __init__(self, endpoint_uri, session=None, request_kwargs=None):
        super().__init__(endpoint_uri, session, request_kwargs)
        self.session = session

    def set_proxy(self, proxy):
        self.session.proxies.update({'http': proxy, 'https': proxy})

    def make_request(self, method, params):
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        request_data = self.encode_rpc_request(method, params)

        response = self.session.post(
            self.endpoint_uri,
            headers=self.get_request_headers(),
            data=request_data,
        )
        response.raise_for_status()

        return self.decode_rpc_response(response.content)


def get_proxies():
    with open("proxies.txt", 'r') as f:
        return [line.strip() for line in f]


def honey_approve(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    contract = w3.eth.contract(AHONEY_ADDRESS, abi=approve_abi)

    transaction = contract.functions.approve(address, 2 ** 256 - 1).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 100000,
        'from': address,
        'nonce': nonce,
        'value': 0

    })
    transaction.update({'maxFeePerGas': w3.eth.fee_history(w3.eth.get_block_number(), 'latest')['baseFeePerGas'][-1] + w3.eth.max_priority_fee})
    transaction.update({'maxPriorityFeePerGas': w3.eth.max_priority_fee})

    signed_swap_txn = w3.eth.account.sign_transaction(transaction, account.key)
    transaction_hash_approve_honey = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
    return transaction_hash_approve_honey

def stg_approve(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    contract = w3.eth.contract(STG_USDC, abi=approve_abi)

    transaction = contract.functions.approve(address, 2 ** 256 - 1).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 100000,
        'from': address,
        'nonce': nonce,
        'value': 0

    })
    transaction.update({'maxFeePerGas': w3.eth.fee_history(w3.eth.get_block_number(), 'latest')['baseFeePerGas'][-1] + w3.eth.max_priority_fee})
    transaction.update({'maxPriorityFeePerGas': w3.eth.max_priority_fee})

    signed_swap_txn = w3.eth.account.sign_transaction(transaction, account.key)
    transaction_hash_approve_stg = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
    return transaction_hash_approve_stg

def bera_swap(account, proxy, num_swaps):
    provider.set_proxy(proxy)  # Устанавливаем прокси
    for i in range(num_swaps):
        transaction_hash = swap1(account)
        print(f'Транзакция свапа: https://artio.beratrail.io//tx/{transaction_hash.hex()}')
        if i < num_swaps - 1:
            delay = random.randint(300, 420)
            print(f"Ждем {delay} секунд перед следующим свапом...")
            time.sleep(delay)

def honey_swap(account, proxy, num_swaps):
    provider.set_proxy(proxy)
    transaction_hash_approve_stg = stg_approve(account)
    print(f'Монета STG-USDC аппрувается, подождите 120 секунд')
    print(f'Транзакция аппрува: https://artio.beratrail.io//tx/{transaction_hash_approve_stg.hex()}')
    time.sleep(120)
    for i in range(num_swaps):
        transaction_hash = swap2(account)
        print(f'Транзакция свапа: https://artio.beratrail.io//tx/{transaction_hash.hex()}')
        if i < num_swaps - 1:
            delay = random.randint(300, 420)
            print(f"Ждем {delay} секунд перед следующим свапом...")
            time.sleep(delay)

def mint_domain(account, proxy, num_mints):
    provider.set_proxy(proxy)  # Устанавливаем прокси
    for i in range(num_mints):
        transaction_hash = mint(account)
        print(f'Транзакция минта домена: https://artio.beratrail.io//tx/{transaction_hash.hex()}')
        if i < num_mints - 1:
            delay = random.randint(300, 420)
            print(f"Ждем {delay} секунд перед следующим миентом...")
            time.sleep(delay)

def supply_honey_bend(account, proxy):
    provider.set_proxy(proxy)
    transaction_hash_approve_honey = honey_approve(account)
    print(f'Монета HONEY аппрувается, подождите 120 секунд')
    print(f'Транзакция аппрува: https://artio.beratrail.io//tx/{transaction_hash_approve_honey.hex()}')
    time.sleep(120)
    transaction_hash = supply(account)
    print(f'Транзакция ввода HONEY: https://artio.beratrail.io//tx/{transaction_hash.hex()}')

def withdraw_honey_bend(account, proxy):
    provider.set_proxy(proxy)
    transaction_hash = withdraw_bend(account)
    print(f'Транзакция вывода: https://artio.beratrail.io//tx/{transaction_hash.hex()}')

def deposit_honey_berps_vault(account, proxy):
    provider.set_proxy(proxy)
    transaction_hash_approve_honey = honey_approve(account)
    print(f'Монета HONEY аппрувается, подождите 120 секунд')
    print(f'Транзакция аппрува: https://artio.beratrail.io//tx/{transaction_hash_approve_honey.hex()}')
    time.sleep(120)
    transaction_hash = deposit_honey_berps(account)
    print(f'Транзакция депозита HONEY в Berps Vault: https://artio.beratrail.io//tx/{transaction_hash.hex()}')

def withdraw_honey_berps(account, proxy):
    provider.set_proxy(proxy)
    transaction_hash_approve_honey = honey_approve(account)
    print(f'Монета HONEY аппрувается, подождите 120 секунд')
    print(f'Транзакция аппрува: https://artio.beratrail.io//tx/{transaction_hash_approve_honey.hex()}')
    time.sleep(120)
    transaction_hash = withdraw_berps(account)
    print(f'Транзакция вывода HONEY из Berps Vault: https://artio.beratrail.io//tx/{transaction_hash.hex()}')

def get_bera_balance(account):
    return w3.eth.get_balance(account.address)

def main():
    while True:
        print("\nВыберите, что сделать:")
        print("1. Свап 0.001-0.002 Bera -> STG")
        print("2. Свап 0.01-0.05 STGUSDC -> HONEY")
        print("3. Минт домена")
        print("4. Добавление Honey в Bend")
        print("5. Вывод HONEY из Bend")
        print("6. Депозит HONEY в Berps Vault")
        print("7. Вывод HONEY из Berps Vault")
        print("8. Проверить баланс BERA")
        print("0. Выход")

        choice = input("Введите цифру: ")

        if choice == "1":
            num_swaps = int(input("Введите количество свапов (от 1 до 20): "))
            if num_swaps < 1:
                num_swaps = 1
            elif num_swaps > 20:
                num_swaps = 20

            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    bera_swap(account, proxy, num_swaps)

        elif choice == "2":
            num_swaps = int(input("Введите количество свапов (от 1 до 20): "))
            if num_swaps < 1:
                num_swaps = 1
            elif num_swaps > 20:
                num_swaps = 20

            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    honey_swap(account, proxy, num_swaps)

        elif choice == "3":
            num_mints = int(input("Введите количество доменов для минта (от 1 до 20): "))
            if num_mints < 1:
                num_mints = 1
            elif num_mints > 20:
                num_mints = 20

            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    mint_domain(account, proxy, num_mints)

        elif choice == "4":
            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    supply_honey_bend(account, proxy)

        elif choice == "5":
            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    withdraw_honey_bend(account, proxy)

        elif choice == "6":
            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    deposit_honey_berps_vault(account, proxy)

        elif choice == "7":
            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                proxies = get_proxies()
                for account, proxy in zip(accounts, proxies):
                    withdraw_honey_berps(account, proxy)

        elif choice == "8":
            txt = 'privates.txt'
            with open(txt, 'r', encoding='utf-8') as keys_file:
                accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
                for account in accounts:
                    balance = get_bera_balance(account)
                    print(f'Баланс BERA на аккаунте {account.address}: {balance / 10 ** 18:.5f} BERA')

        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")


proxies = get_proxies()

w3 = Web3(MyHTTPProvider('https://artio.rpc.berachain.com', session=sess))
provider = w3.provider

if __name__ == "__main__":
    main()
