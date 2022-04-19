from brownie import config, FundMe, accounts, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is: {network.show_active()}")
        print("Deploying Mocks")
        if len(MockV3Aggregator) <= 0:
            mock_aggregator = MockV3Aggregator.deploy(
                DECIMALS, STARTING_PRICE, {"from": account}
            )
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks Deployed!")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"contract deployed to :{fund_me.address}")
    return fund_me


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_fund_me()
