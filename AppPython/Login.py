import customtkinter as ctk
import tkinter as tk
import Register as rg
import Patient as pt
import Doctor as dt
from eth_account.messages import encode_defunct
from hexbytes import HexBytes

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
            
        self.FRAME0 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.FRAME0.pack_propagate(True)
        self.FRAME0.pack(pady=(5, 5), expand=1, fill="both", padx=(5, 0), side="left")
        self.LABEL19 = ctk.CTkLabel(master=self.FRAME0, text="", anchor="w", text_color=("gray10", "#FFFFFF"), font=ctk.CTkFont(size=15) )
        self.LABEL19.pack(pady=(20, 0), fill="x", padx=(20, 0))
        self.LABEL18 = ctk.CTkLabel(master=self.FRAME0, text="Welcome\nBack !", justify="left", anchor="w", text_color=("gray10", "#FFFFFF"), font=ctk.CTkFont(size=82))
        self.LABEL18.pack(padx=(30, 0), expand=1, fill="x")
        self.FRAME2_copy = ctk.CTkFrame(master=self)
        self.FRAME2_copy.pack_propagate(False)
        self.FRAME2_copy.pack(pady=(20, 20), expand=1, fill="both", padx=(5, 20), side="left")
        self.FRAME2 = ctk.CTkFrame(master=self.FRAME2_copy, width=565, height=500, fg_color="transparent")
        self.FRAME2.pack(expand=1, padx=50, pady=50)
        self.LABEL3 = ctk.CTkLabel(master=self.FRAME2, text="Login", anchor="w", text_color=("gray10", "#FFFFFF"), font=ctk.CTkFont(size=39))
        self.LABEL3.pack(fill="x")
        self.LABEL5_copy = ctk.CTkLabel(master=self.FRAME2, text="Welcome Back! Please login to your account", anchor="w", text_color=("gray10", "#b4b4b4"), wraplength=332, justify="left", font=ctk.CTkFont(size=14))
        self.LABEL5_copy.pack(pady=(10, 10), fill="x")
        self.FRAME5 = ctk.CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME5.pack(pady=(20, 20), fill="x")
        self.LABEL8_copy = ctk.CTkLabel(master=self.FRAME5, text="Account Address", anchor="w", text_color=("gray10", "#FFFFFF"), font=ctk.CTkFont(size=15))
        self.LABEL8_copy.pack(fill="x")
        self.ENTRY9 = ctk.CTkEntry(master=self.FRAME5, placeholder_text="0x"+40*"0", height=35, corner_radius=3, text_color=("gray10", "#FFFFFF"), width=222)
        self.ENTRY9.pack(fill="x")
        self.BUTTON16 = ctk.CTkButton(master=self.FRAME2, text="Login", height=35, text_color=("gray98", "#FFFFFF"), fg_color=("#8651ff", "#8651ff"), hover_color=("#6940c9", "#6940c9"), width=500, corner_radius=3, command=self.login)
        self.BUTTON16.pack(fill="x")
        self.FRAME17 = ctk.CTkFrame(master=self.FRAME2, fg_color="transparent")
        self.FRAME17.pack(pady=(10, 0), fill="x")
        self.LABEL18 = ctk.CTkLabel(master=self.FRAME17, text="New User?", text_color=("gray10", "#FFFFFF"))
        self.LABEL18.pack(side="left")
        self.BUTTON19 = ctk.CTkButton(master=self.FRAME17, text="Sign Up", width=70, fg_color="transparent", hover=False, height=0, text_color=("#000000", "#FFFFFF"), command=lambda:self.controller.show_main_frame(rg.RegisterFrame))
        self.BUTTON19.pack(side="left")

        self.web3 = self.controller.web3
        self.doctor_contract = self.controller.doctor_contract
        self.patient_contract = self.controller.patient_contract
        self.role_contract = self.controller.role_contract
        
    def login(self):
        address = self.ENTRY9.get()
        if not self.web3.is_address(address):
            tk.messagebox.showerror('Error', "Invalid address. Please enter a valid Ethereum address.")
            return
       
        try:
            
                self.web3.account = self.web3.to_checksum_address(address.lower())
                print(f"Calling checkRole with address: {self.web3.account}") #ajout
                print(f"Role contract address: {self.role_contract.address}") #ajout
                
                role = self.role_contract.functions.checkRole(self.web3.account).call()
                print(f"Role returned: {role}")#ajout
                if role == 0:
                    tk.messagebox.showerror('Error', "Account not registered. Please register first.")
                    self.controller.show_main_frame(rg.RegisterFrame)
                    return
                elif role == 1:
                    self.controller.frames[dt.DoctorFrame].update_doctor_frame()
                    self.ENTRY9.delete(0, tk.END)
                    self.controller.show_main_frame(dt.DoctorFrame)
                    return
                elif role == 2:
                    self.controller.frames[pt.PatientFrame].update_patient_frame()
                    self.ENTRY9.delete(0, tk.END)
                    self.controller.show_main_frame(pt.PatientFrame)
                    return
                
                tk.messagebox.showerror('Error', "Account not registered. Please register first.")
                self.controller.show_main_frame(rg.RegisterFrame)
           
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return

