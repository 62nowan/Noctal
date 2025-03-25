import customtkinter as ctk
from tkinter import ttk
import os
import json
import subprocess
from PIL import Image
from Blockchain.Backend.util.util import decode_base58

class NoctalUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")
        
        self.title("Noctal Core")
        self.geometry("900x550")

        self.wallet_addresses = []
        self.utxos = {}
        
        self.create_sidebar()
        self.create_main_layout()
        

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")
        
        self.tabs_dict = {
            "Home": self.show_home,
            "Mine": self.show_mine,
            "Send": self.show_send,
            "Receive": self.show_receive,
            "Transactions": self.show_transactions
        }

        for tab_name, command in self.tabs_dict.items():
            btn = ctk.CTkButton(self.sidebar, text=tab_name, command=command, corner_radius=10)
            btn.pack(fill="x", pady=5, padx=10)

    def create_main_layout(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(expand=True, fill="both")
        self.show_home()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
    def show_home(self):
        self.clear_content()
        
        balance_frame = ctk.CTkFrame(self.content_frame)
        balance_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(balance_frame, text="Wallet Balance", font=("Arial", 18)).pack()
   
        if self.wallet_addresses:
            public_address = self.wallet_addresses[1]["PublicAddress"] #Main address
            balance = self.calculate_balance(public_address)
            ctk.CTkLabel(balance_frame, text=f"Available: {balance:.8f} NOC", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(balance_frame, text="Pending: 0.00 NOC", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(balance_frame, text=f"Total: {balance:.8f} NOC", font=("Arial", 14)).pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(balance_frame, text="No wallet address found.", font=("Arial", 14)).pack(anchor="w", padx=10)
        
        transactions_frame = ctk.CTkFrame(self.content_frame)
        transactions_frame.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(transactions_frame, text="Recent Transactions", font=("Arial", 16)).pack()
        
        transactions = [
            {"date": "2025-03-20", "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", "amount": 0.005},
            {"date": "2025-03-19", "address": "bc1pqxy8kdyrstzq2n0yrf2493p83kkfjhx0xyz", "amount": -0.002},
        ]
        
        for transaction in transactions:
            transaction_entry = ctk.CTkFrame(transactions_frame)
            transaction_entry.pack(fill="x", padx=10, pady=5)
            
            img_filename = "receive-money.png" if transaction["amount"] > 0 else "send-money.png"
            img_path = os.path.join(os.path.dirname(__file__), "image", img_filename)

            if os.path.exists(img_path):
                img = ctk.CTkImage(light_image=Image.open(img_path), size=(30, 30))
                img_label = ctk.CTkLabel(transaction_entry, image=img, text="")
                img_label.image = img  
                img_label.pack(side="left", padx=5)
            else:
                print(f"⚠️ Image non trouvée : {img_path}")
            
            details_frame = ctk.CTkFrame(transaction_entry)
            details_frame.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(details_frame, text=f"Date: {transaction['date']}").pack(anchor="w")
            ctk.CTkLabel(details_frame, text=f"Address: {transaction['address']}").pack(anchor="w")
            
            amount_color = "green" if transaction["amount"] > 0 else "red"
            ctk.CTkLabel(transaction_entry, text=f"{transaction['amount']} NOC", text_color=amount_color).pack(side="right", padx=5)

    def show_receive(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Your Noctal Address(es):", font=("Arial", 18)).pack(pady=10)
        
        self.address_frame = ctk.CTkFrame(self.content_frame)
        self.address_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        generate_button = ctk.CTkButton(self.content_frame, text="Generate New Address", command=self.generate_new_address)
        generate_button.pack(pady=10)
        
        self.load_addresses()

    def generate_new_address(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",".."))
        account_script = os.path.join(base_dir, "Blockchain", "Client", "account.py")
        subprocess.run(["python", account_script])
        self.load_addresses()

    def load_addresses(self):
        for widget in self.address_frame.winfo_children():
            widget.destroy()
        
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..")) 
        file_path = os.path.join(base_dir, "data", "account")
        
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    self.wallet_addresses = json.load(file)
                    for wallet in self.wallet_addresses:
                        self.display_wallet_address(wallet)
                except json.JSONDecodeError:
                    print("⚠️ Erreur: Fichier JSON invalide.")
        else:
            print(f"⚠️ Fichier non trouvé : {file_path}")
            self.wallet_addresses = []

    def display_wallet_address(self, wallet):
        address_entry = ctk.CTkFrame(self.address_frame)
        address_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(address_entry, text=wallet["PublicAddress"], font=("Arial", 14)).pack(side="left", padx=5)
        
        show_button = ctk.CTkButton(address_entry, text="Show Private", command=lambda: self.show_private_key(wallet))
        show_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(address_entry, text="Delete", fg_color="red", command=lambda: self.delete_wallet(wallet))
        delete_button.pack(side="left", padx=5)

    def show_private_key(self, wallet):
        ctk.CTkLabel(self.content_frame, text=f"Private Key: {wallet['privateKey']}", font=("Arial", 14)).pack(pady=5)

    def delete_wallet(self, wallet):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",".."))
        file_path = os.path.join(base_dir, "data", "account")

        if not os.path.exists(file_path):
            print(f"⚠️ Fichier non trouvé : {file_path}")
            return

        with open(file_path, "r") as file:
            try:
                data = json.load(file)  
                if not isinstance(data, list):
                    print("⚠️ Le fichier ne contient pas une liste valide.")
                    return
            except json.JSONDecodeError:
                print("⚠️ Erreur de décodage JSON.")
                return
            
        data = [w for w in data if w["PublicAddress"] != wallet["PublicAddress"]]
        with open(file_path, "w") as file:
            json.dump(data, file) 

        self.load_addresses()


    def show_mine(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Noctal Mining", font=("Arial", 16)).pack(pady=10)
        mine_status = ttk.Label(self.content_frame, text="Mining Status: Idle")
        mine_status.pack(pady=5)
        start_mining_button = ttk.Button(self.content_frame, text="Start Mining")
        start_mining_button.pack(pady=10)

    def show_send(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Send Noctal", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.content_frame, text="Recipient Address").pack()
        ttk.Entry(self.content_frame).pack(pady=5)
        ttk.Label(self.content_frame, text="Amount (NOC)").pack()
        ttk.Entry(self.content_frame).pack(pady=5)
        send_button = ttk.Button(self.content_frame, text="Send")
        send_button.pack(pady=10)

    def show_transactions(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Transaction History", font=("Arial", 16)).pack(pady=10)
        transactions_tree = ttk.Treeview(self.content_frame, columns=("Date", "Amount", "Status"), show="headings")
        transactions_tree.heading("Date", text="Date")
        transactions_tree.heading("Amount", text="Amount")
        transactions_tree.heading("Status", text="Status")
        transactions_tree.pack(pady=10)

    def calculate_balance(self, public_address):
        if self.utxos and len(public_address) < 35 and public_address[:1] == "1":
            h160 = decode_base58(public_address) 
            amount = 0
            utxos_dict = dict(self.utxos)

            for txid in utxos_dict:
                for tx_out in utxos_dict[txid].tx_outs:
                    if tx_out.script_pubkey.cmds[2] == h160:  
                        amount += tx_out.amount  
            return amount / 100000000  
        else:
            return 0



def mainGui(utxos, mempool, port):
    app = NoctalUI()
    app.utxos = utxos  
    app.mempool = mempool  
    app.mainloop()
    
