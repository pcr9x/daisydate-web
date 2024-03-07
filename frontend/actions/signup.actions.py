from js import document, console

# Initialize an empty dictionary to store form data
form_data = {}

def show_step(step):
    # Hide all steps
    steps = document.querySelectorAll(".flow-base-page")
    for step_element in steps:
        step_element.style.display = 'none'
    
    # Show the specified step
    document.querySelector(f"#step-{step}").style.display = 'block'

def collect_data(step):
    # Collecting data from each step
    if step == 1:
        email = Element("email-input").element.value
        password = document.querySelector("password-input").value
        form_data['email'] = email
        form_data['password'] = password
        
        Element('test-output').element.innerHTML = f"Email: {email}, Password: {password}"
    # Include conditions for other steps, collect respective data
    

    # After collecting data, show the next step
    next_step = step + 1
    show_step(next_step)

def finish_signup():
    # Collect data from the final step if any and perform the final action
    print("Form Data:", form_data)
    # Implement the final action, such as making an API call

# Show the first step on initial load
show_step(1)
