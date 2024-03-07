# import js
# from pyscript import document

# class CurrencyConverter:
#     def __init__(self):
#         self.container = document.getElementById("container")
#         self.input_amount = document.createElement("input")
#         self.input_amount.type = "number"
#         self.input_amount.placeholder = "Enter amount"
        
#         self.radio_thb_to_usd = document.createElement("input")
#         self.radio_thb_to_usd.type = "radio"
#         self.radio_thb_to_usd.name = "conversion"
#         self.radio_thb_to_usd.value = "thb_to_usd"
#         self.radio_thb_to_usd.id = "thb_to_usd"
#         self.label_thb_to_usd = document.createElement("label")
#         self.label_thb_to_usd.htmlFor = "thb_to_usd"
#         self.label_thb_to_usd.textContent = "THB to USD"

#         self.radio_usd_to_thb = document.createElement("input")
#         self.radio_usd_to_thb.type = "radio"
#         self.radio_usd_to_thb.name = "conversion"
#         self.radio_usd_to_thb.value = "usd_to_thb"
#         self.radio_usd_to_thb.id = "usd_to_thb"
#         self.label_usd_to_thb = document.createElement("label")
#         self.label_usd_to_thb.htmlFor = "usd_to_thb"
#         self.label_usd_to_thb.textContent = "USD to THB"
        
#         self.convert_button = document.createElement("button")
#         self.convert_button.textContent = "Convert"
#         self.convert_button.onclick = self.convert_currency
        
#     def convert_currency(self, event):
#         try:
#             amount = float(self.input_amount.value)
#             conversion_rate = 30  # 1 USD = 30 THB
#             if self.radio_usd_to_thb.checked:
#                 converted_amount = amount * conversion_rate
#             else:
#                 converted_amount = amount / conversion_rate
                
#             js.alert(f"Converted amount: {converted_amount:.2f}")
#         except ValueError:
#             js.alert("Please enter a valid amount")
            
#     def render(self):
#         self.container.appendChild(self.input_amount)
#         self.container.appendChild(self.radio_thb_to_usd)
#         self.container.appendChild(self.label_thb_to_usd)
#         self.container.appendChild(self.radio_usd_to_thb)
#         self.container.appendChild(self.label_usd_to_thb)
#         self.container.appendChild(self.convert_button)
        
# if __name__ == "__main__":
#     converter = CurrencyConverter()
#     converter.render()
