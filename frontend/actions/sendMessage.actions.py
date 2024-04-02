from pyscript import Document

def init(event):
    m = Document.get_element_by_id("message-input")
    m.text = "sdasdasdas"
    
Document.get_element_by_id("send-button").on("click",init)