import json
import requests
import time

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

start = time.time()

algod_address = 'https://node.algoexplorerapi.io'

public_key = "AAAAAAAAAAAAAAAAAAAAAAAAAAA" #insert public key here
mnemonic_phrase = "boat house tree ..." #insert mnemonic here
account_private_key = mnemonic.to_private_key(mnemonic_phrase)

algodclient = algod.AlgodClient('', algod_address, '')

frogBotID = 482470189 # 666 supply
frogBot2ID = 554633277 # 420 supply
swapKeyID = 1168852642 # 1000 supply

yarnHoldersList = {}
yarnHolders = []

#sets up lists for individual collections
knitHeads = [] 
knockOffs = []
knith3Ds = []
lilknits = []
snails = []
pixelHeads = []

wallets = ['45LDVA6A44QD2PNWNAPGGDQESXNOY36HJC6UZXZNMIAYLXUYD4DGRAMNNA','FROGOHZ3D5GHBKPDDQWKT5RWABZGY3VD6D3UNG7YLTABKDDLJJD4E257HA','KH3DSVFR6I3IXJ7OYV2QQXGER7QUKCS6F6H3BCNB536XZHEATHXASUW24Q','FROGJWNVWICMFTAGNCLGAI5UNXJEEFCUDNPBD2U6VWTATXANHXB6BHRW2M','SNAILSURAATOMSYJ36S7ZVZ3OD5USXU7BHHZFEB5QOXEDDTQH2MOO3REAI', 'PIXYN3736RN7XS7ZA354R33RTDUTPRAZ2YMGU3V72I3EVDY62O3TDK43X4']

#fills up individual collection lists with asset IDs
count = 0
for wallet in wallets: 
    url = "https://mainnet-idx.algonode.cloud/v2/accounts/" + wallet + "?include-all=false&exclude=assets,apps-local-state,created-apps"
    answer = requests.get(url)
    if answer.status_code != 200:
        print("Error retrieving data on CREATOR wallet: " + wallet)
        print('It took ', time.time()-start, ' seconds.')
        exit()
    res = answer.json()['account']
    createdassets = res['created-assets']
    for asset in createdassets:
        if count == 0:
            try:
                first2 = asset['params']['unit-name'][:2]
                if first2 == "KH":
                    knitHeads.append(asset['index'])
            except Exception as e:
                pass
        elif count == 1:
            knockOffs.append(asset['index'])
        elif count == 2:
            knith3Ds.append(asset['index'])
        elif count == 3:
            lilknits.append(asset['index'])
        elif count == 4:
            snails.append(asset['index'])
        elif count == 5:
            pixelHeads.append(asset['index'])
    count+=1

# builds list of every YARN holder
url = "https://mainnet-idx.algonode.cloud/v2/assets/878951062/balances?include-all=false"
answer = requests.get(url)
if answer.status_code != 200:
    print("Error retrieving data on YARN balances")
    print('It took ', time.time()-start, ' seconds.')
    exit()
res = answer.json()['balances']

for balance in res:
    if balance['amount'] != 0:
        yarnHoldersList[balance['address']] = balance['amount']
yarnHoldersList = dict(sorted(yarnHoldersList.items(), key=lambda item: item[1], reverse=True))
yarnHolders = yarnHoldersList.keys()

txcount = 0

# go through every YARN holder, check every one of their asset to see if they belong to one of the collection
for wallet in yarnHolders:
    url = "https://mainnet-idx.algonode.cloud/v2/accounts/"+ wallet +"?include-all=false&exclude=created-assets,apps-local-state,created-apps"
    answer = requests.get(url)
    if answer.status_code != 200:
        print("\nError retrieving user data. Trying again in 5s...")
        time.sleep(5)
        answer = requests.get(url)
        if answer.status_code != 200:
            print("Error retrieving USER assets on wallet: " + wallet + "\n")
            continue

    res = answer.json()['account']['assets']

    amtLilknits = 0
    amtSnails = 0
    amtKnithead = 0
    amtKnith3D = 0
    amtPixelhead = 0
    amtKnockOff = 0
    amtFrogBot = 0

    yarn = 0
    note = ""

    for asset in res:
        assetID = asset['asset-id']
        amount = asset['amount']
        if assetID in lilknits:
            if amount > 0:
                amtLilknits+=1
                lilknits.remove(assetID)
        elif assetID in snails:
            if amount > 0:
                amtSnails+=1
                snails.remove(assetID)
        elif assetID in knith3Ds:
            if amount > 0:
                amtKnith3D+=1
                knith3Ds.remove(assetID)
        elif assetID in knitHeads  and assetID != swapKeyID:
            if amount > 0:
                amtKnithead+=1
                knitHeads.remove(assetID)
        elif assetID in pixelHeads:
            if amount > 0:
                amtPixelhead+=1
                pixelHeads.remove(assetID)
        elif assetID in knockOffs:
            if amount > 0:
                amtKnockOff+=1
                knockOffs.remove(assetID)
        elif assetID == frogBotID or assetID == frogBot2ID:
            if amount > 0:
                amtFrogBot += amount

    # calculate amount of YARN to send
    if amtLilknits == 0 and amtSnails == 0 and amtKnithead == 0 and amtKnith3D == 0 and amtPixelhead == 0 and amtKnockOff == 0:
        pass
    else:
        yarn = amtKnithead * 420 + amtKnockOff * 333 + amtKnith3D * 209 + amtLilknits * 69 + amtPixelhead * 55 + amtSnails * 55 + amtFrogBot * 5
        if amtKnithead > 0:
            note += "Knithead: " + str(amtKnithead) + " x420   "
        if amtKnockOff > 0:
            note += "KnockOff: " + str(amtKnockOff) + " x333   "
        if amtKnith3D > 0:
            note += "KnitH3D: " + str(amtKnith3D) + " x209   "
        if amtLilknits > 0:
            note += "LilKnit: " + str(amtLilknits) + " x69   "
        if amtPixelhead > 0:
            note += "PixelHead: " + str(amtPixelhead) + " x55   "
        if amtSnails > 0:
            note += "Snail: " + str(amtSnails) + " x55   "
        if amtFrogBot > 0:
            note += "FrogBot: " + str(amtFrogBot) + " x5   "
        note = note[:-3]
    
    if yarn > 0:
        print("wallet: " + wallet + ", YARN to send: " + str(yarn))

        params = algodclient.suggested_params()

        gh = params.gh
        first_valid_round = params.first
        last_valid_round = params.last
        fee = params.min_fee
        send_amount = yarn
        index = 878951062 #YARN asset ID

        send_to_address = wallet

        tx = transaction.AssetTransferTxn(
            sender=public_key,
            sp=params,
            receiver=send_to_address,
            amt=send_amount,
            index=index,
        )

        signed_tx = tx.sign(account_private_key)
        txcount +=1

        try:
            tx_confirm = algodclient.send_transaction(signed_tx)
            print('Transaction sent with ID', signed_tx.transaction.get_txid())
        except Exception as e:
            print(e)

print(len(knitHeads))
print(len(lilknits))
print(len(knith3Ds))
print(len(snails))
print(len(pixelHeads))
print(len(knockOffs))

print('It took ', time.time()-start, ' seconds.')
print('txs sent: ' + str(txcount))
exit()