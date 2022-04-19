from brownie import accounts, FundMe, network
from scripts.deploy import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fees = fund_me.getEntranceFee()
    print(f"Entrance fees is: {entrance_fees}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fees})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
